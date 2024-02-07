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
    return pt.Return(__pcg_rotation(
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
    ))


@pt.Subroutine(pt.TealType.uint64)
def __pcg_rotation(value, rot) -> pt.Expr:
    return pt.Return(
        # This needs to be uint32. Luckily, "value" is already uint32 and a right shift will maintain that invariant.
        pt.BitwiseOr(
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
    )


@pt.Subroutine(pt.TealType.uint64)
def __twos_complement(number) -> pt.Expr:
    return pt.Return(
        InlineAssembly(
            "addw; swap; pop;",
            pt.BitwiseNot(number),
            pt.Int(1),
            type=pt.TealType.uint64
        )
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
            "addw; swap; pop;",
            InlineAssembly(
                "mulw; swap; pop;",
                pt.ScratchLoad(None, pt.TealType.uint64, state_slot_index),
                PCG_DEFAULT_MULTIPLIER,
                type=pt.TealType.uint64
            ),
            PCG_DEFAULT_INCREMENT,
            type=pt.TealType.uint64
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


# If upper_bound is set, it's never included in the range.
# If upper_bound is not set, the highest value (2^32-1) is included in the range.
@pt.Subroutine(pt.TealType.bytes)
def pcg_random(state_slot_index, lower_bound, upper_bound, length) -> pt.Expr:
    result_length = pt.abi.make(pt.abi.Uint16)

    shifted_bound = pt.ScratchVar(pt.TealType.uint64)
    threshold = pt.ScratchVar(pt.TealType.uint64)
    result = pt.ScratchVar(pt.TealType.bytes)

    i = pt.ScratchVar(pt.TealType.uint64)
    r = pt.abi.make(pt.abi.Uint32)

    return pt.Seq(
        result_length.set(length),  # This is also used because it's an assert on "length" value.
        result.store(result_length.encode()),

        pt.If(pt.And(lower_bound == pt.Int(0), upper_bound == pt.Int(0)))
        .Then(pt.Seq(
            pt.For(
                i.store(pt.Int(0)),
                i.load() < length,
                i.store(i.load() + pt.Int(1))
            ).Do(pt.Seq(
                result.store(pt.Concat(
                    result.load(),
                    pt.Extract(pt.Itob(__pcg_random(state_slot_index)), pt.Int(4), pt.Int(4))
                ))
            ))
        ))
        .Else(pt.Seq(
            pt.If(upper_bound != pt.Int(0)).Then(pt.Seq(
                pt.Assert(upper_bound > pt.Int(1)),
                pt.Assert(upper_bound < pt.Int(2**32)),
                # The difference in bounds must be at least 2 because otherwise, the user is just asking
                #  for a list of "lower_bound".
                pt.Assert(lower_bound < upper_bound - pt.Int(1)),

                shifted_bound.store(upper_bound - lower_bound),
            )).Else(pt.Seq(
                # upper_bound == 0 means unbounded.
                # Must include 2^32-1 which means that lower_bound must be less than that.
                # Otherwise, we would be in the nonsensical situation where the user is asking for a list
                #  of "2^32-1".
                pt.Assert(lower_bound < pt.Int(2**32-1)),

                # At this point, this should be 2^32 - lower_bound == -lower_bound == lower_bound's two's complement.
                # But, we can afford to write 2^32 as a native uint64 so that's what we'll do.
                shifted_bound.store(pt.Int(2**32) - lower_bound),
            )),

            threshold.store(mask_to_uint32(__twos_complement(shifted_bound.load())) % (shifted_bound.load())),

            pt.For(
                i.store(pt.Int(0)),
                i.load() < length,
                i.store(i.load() + pt.Int(1))
            ).Do(pt.Seq(
                pt.While(pt.Int(1)).Do(pt.Seq(
                    r.set(__pcg_random(state_slot_index)),
                    pt.If(r.get() >= threshold.load()).Then(pt.Seq(
                        r.set((r.get() % shifted_bound.load()) + lower_bound),
                        result.store(pt.Concat(result.load(), r.encode())),
                        pt.Break()
                    ))
                ))
            )),
        )),

        pt.Return(result.load())
    )
