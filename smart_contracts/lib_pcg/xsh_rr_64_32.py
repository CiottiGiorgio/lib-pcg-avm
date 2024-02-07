from beaker.lib.inline import InlineAssembly
import pyteal as pt


PCG_DEFAULT_MULTIPLIER = pt.Int(6364136223846793005)
PCG_DEFAULT_INCREMENT = pt.Int(1442695040888963407)


def mask_to_uint32(uint64):
    return pt.BitwiseAnd(
        uint64,
        pt.Int(int.from_bytes(b"\x00\x00\x00\x00\xFF\xFF\xFF\xFF"))
    )


@pt.Subroutine(pt.TealType.uint64)
def __pcg_output(state) -> pt.Expr:
    return __pcg_rotation(
        # This needs to be uint32. We can't guarantee that at this point, so we cast it explicitly.
        mask_to_uint32(
            pt.ShiftRight(
                pt.BitwiseXor(
                    pt.ShiftRight(
                        state,
                        pt.Int(18)
                    ),
                    state
                ),
                pt.Int(27)
            ),
        ),
        pt.ShiftRight(
            state,
            pt.Int(59)
        ),
    )


@pt.Subroutine(pt.TealType.uint64)
def __pcg_rotation(value, rot) -> pt.Expr:
    # This needs to be uint32. Luckily, "value" is already uint32 and a right shift will maintain that invariant.
    return pt.BitwiseOr(
        pt.ShiftRight(
            value,
            rot
        ),
        # This needs to be uint32. Therefore, we mask out the higher bits because we can't guarantee
        #  that invariant with a left shift of "rot" two's complement.
        mask_to_uint32(
            pt.ShiftLeft(
                value,
                pt.BitwiseAnd(
                    __twos_complement(rot),
                    pt.Int(31)
                )
            ),
        )
    )


@pt.Subroutine(pt.TealType.uint64)
def __twos_complement(number) -> pt.Expr:
    return InlineAssembly(
        "addw; swap; pop;",
        pt.BitwiseNot(number),
        pt.Int(1),
        type=pt.TealType.uint64
    )


@pt.Subroutine(pt.TealType.none)
def pcg_init(state_slot_index, initial_state) -> pt.Expr:
    return pt.Seq(
        pt.ScratchStore(None, pt.Int(0), state_slot_index),

        __pcg_step(state_slot_index),

        pt.ScratchStore(
            None,
            pt.ScratchLoad(
                None,
                pt.TealType.uint64,
                state_slot_index
            ) + initial_state,
            state_slot_index
        ),

        __pcg_step(state_slot_index)
    )


@pt.Subroutine(pt.TealType.none)
def __pcg_step(state_slot_index) -> pt.Expr:

    # Equivalent to state = state * multiplier + increment
    # Considering that both operations could overflow and therefore the highest bits are discarded
    return pt.ScratchStore(
        None,
        InlineAssembly(
            "mulw; uncover 2; addw; uncover 3; swap;",
            PCG_DEFAULT_INCREMENT,
            PCG_DEFAULT_MULTIPLIER,
            pt.ScratchLoad(None, pt.TealType.uint64, state_slot_index),
            type=pt.TealType.anytype
        ),
        state_slot_index
    )


@pt.Subroutine(pt.TealType.uint64)
def __pcg_random(state_slot_index) -> pt.Expr:
    old_state = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        old_state.store(pt.ScratchLoad(None, pt.TealType.uint64, state_slot_index)),
        __pcg_step(state_slot_index),
        pt.Return(__pcg_output(old_state.load()))
    )


# NOTE: It _may_ be possible to split a 32bit pseudo random integer in 2 (or 4, depending on the required bit_size)
#  to obtain more than one smaller number instead of performing two __pcg_step.
#  This could dramatically improve the efficiency of the algorithm when operating at smaller bit_size.
#  However, I can't guarantee that this does not yield a statistically worse sequence.
#  Furthermore, the algorithm to advance multiple steps at once becomes complex.
#  To improve performance it doesn't make sense to reduce the size of the state because ultimately it still
#  would rely on the same uint64 opcodes.

# If upper_bound is set, it's never included in the range.
# If upper_bound is not set, the highest value (2^32-1) is included in the range.
@pt.Subroutine(pt.TealType.bytes)
def pcg_random(state_slot_index, bit_size, lower_bound, upper_bound, length) -> pt.Expr:
    result_length = pt.abi.make(pt.abi.Uint16)
    byte_size = pt.ScratchVar(pt.TealType.uint64)

    absolute_bound = pt.ScratchVar(pt.TealType.uint64)
    threshold = pt.ScratchVar(pt.TealType.uint64)
    result = pt.ScratchVar(pt.TealType.bytes)

    i = pt.ScratchVar(pt.TealType.uint64)
    candidate_bounded = pt.abi.make(pt.abi.Uint32)

    def __truncate_to_size(_n, _byte_size) -> pt.Expr:
        return pt.Extract(
            pt.Itob(_n),
            # 32bit == Extract(..., 8-4, 4); 16bit == Extract(..., 8-2, 2); 8bit == Extract(..., 8-1, 1)
            pt.Int(8) - _byte_size,
            _byte_size
        )

    return pt.Seq(
        result_length.set(length),  # This is also used because it's an assert on "length" value.
        result.store(result_length.encode()),
        pt.Assert(pt.Or(bit_size == pt.Int(8), bit_size == pt.Int(16), bit_size == pt.Int(32))),
        # num_bits -> num_bytes == num_bits / 8 == num_bits / 2^3 == num_bits >> 3
        byte_size.store(pt.ShiftRight(bit_size, pt.Int(3))),

        pt.If(pt.And(lower_bound == pt.Int(0), upper_bound == pt.Int(0)))
        .Then(pt.Seq(
            pt.For(
                i.store(pt.Int(0)),
                i.load() < length,
                i.store(i.load() + pt.Int(1))
            ).Do(pt.Seq(
                result.store(pt.Concat(
                    result.load(),
                    __truncate_to_size(__pcg_random(state_slot_index), byte_size.load()),
                ))
            ))
        ))
        .Else(pt.Seq(
            pt.If(upper_bound != pt.Int(0)).Then(pt.Seq(
                pt.Assert(upper_bound > pt.Int(1)),
                pt.Assert(upper_bound < pt.Exp(pt.Int(2), bit_size)),
                # The difference in bounds must be at least 2 because otherwise, the user is just asking
                #  for a list of "lower_bound".
                pt.Assert(lower_bound < upper_bound - pt.Int(1)),

                absolute_bound.store(upper_bound - lower_bound),
            )).Else(pt.Seq(
                # upper_bound == 0 means unbounded.
                # Must include 2^bit_size-1 which means that lower_bound must be less than that.
                # Otherwise, we would be in the nonsensical situation where the user is asking for a list
                #  of "2^bit_size-1".
                pt.Assert(lower_bound < pt.ShiftLeft(pt.Int(1), bit_size) - pt.Int(1)),

                absolute_bound.store(pt.ShiftLeft(pt.Int(1), bit_size) - lower_bound),
            )),

            threshold.store(mask_to_uint32(__twos_complement(absolute_bound.load())) % (absolute_bound.load())),

            pt.For(
                i.store(pt.Int(0)),
                i.load() < length,
                i.store(i.load() + pt.Int(1))
            ).Do(pt.Seq(
                pt.While(pt.Int(1)).Do(pt.Seq(
                    candidate_bounded.set(__pcg_random(state_slot_index)),
                    pt.If(candidate_bounded.get() >= threshold.load()).Then(pt.Seq(
                        result.store(pt.Concat(
                            result.load(),
                            __truncate_to_size(
                                (candidate_bounded.get() % absolute_bound.load()) + lower_bound,
                                byte_size.load()
                            ),
                        )),
                        pt.Break(),
                    ))
                ))
            )),
        )),

        pt.Return(result.load())
    )
