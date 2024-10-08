import pyteal as pt
from beaker.lib.inline import InlineAssembly

from lib_pcg.consts import PCG_FIRST_INCREMENT, PCG_MULTIPLIER


@pt.Subroutine(pt.TealType.none)
def pcg32_init(state_slot_index: pt.Expr, seed: pt.Expr) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        seed: pt.Bytes

    Returns:
        None
    """
    return pt.Seq(
        pt.Assert(pt.Len(seed) == pt.Int(8)),
        __pcg32_init(state_slot_index, pt.Btoi(seed), PCG_FIRST_INCREMENT),
    )


@pt.Subroutine(pt.TealType.none)
def pcg16_init(state_slot_index: pt.Expr, seed: pt.Expr) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        seed: pt.Bytes

    Returns:
        None
    """
    return pcg32_init(state_slot_index, seed)


@pt.Subroutine(pt.TealType.none)
def pcg8_init(state_slot_index: pt.Expr, seed: pt.Expr) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        seed: pt.Bytes

    Returns:
        None
    """
    return pcg32_init(state_slot_index, seed)


@pt.Subroutine(pt.TealType.bytes)
def pcg32_random(
    state_slot_index: pt.Expr,
    lower_bound: pt.Expr,
    upper_bound: pt.Expr,
    length: pt.Expr,
) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        lower_bound: pt.Int
        upper_bound: pt.Int
        length: pt.Int

    Returns:
        pt.Bytes
    """
    return __pcg32_bounded_sequence(
        state_slot_index, pt.Int(32), lower_bound, upper_bound, length
    )


@pt.Subroutine(pt.TealType.bytes)
def pcg16_random(
    state_slot_index: pt.Expr,
    lower_bound: pt.Expr,
    upper_bound: pt.Expr,
    length: pt.Expr,
) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        lower_bound: pt.Int
        upper_bound: pt.Int
        length: pt.Int

    Returns:
        pt.Bytes
    """
    return __pcg32_bounded_sequence(
        state_slot_index, pt.Int(16), lower_bound, upper_bound, length
    )


@pt.Subroutine(pt.TealType.bytes)
def pcg8_random(
    state_slot_index: pt.Expr,
    lower_bound: pt.Expr,
    upper_bound: pt.Expr,
    length: pt.Expr,
) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        lower_bound: pt.Int
        upper_bound: pt.Int
        length: pt.Int

    Returns:
        pt.Bytes
    """
    return __pcg32_bounded_sequence(
        state_slot_index, pt.Int(8), lower_bound, upper_bound, length
    )


def __pcg32_init(
    state_slot_index: pt.Expr, initial_state: pt.Expr, incr: pt.Expr
) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        initial_state: pt.Int
        incr: pt.Int

    Returns:
        None
    """
    return pt.Seq(
        pt.ScratchStore(None, pt.Int(0), state_slot_index),
        __pcg32_step(state_slot_index, incr),
        pt.ScratchStore(
            None,
            InlineAssembly(
                "\n".join(["addw", "bury 1"]),
                pt.ScratchLoad(None, pt.TealType.uint64, state_slot_index),
                initial_state,
                type=pt.TealType.uint64,
            ),
            state_slot_index,
        ),
        __pcg32_step(state_slot_index, incr),
    )


# NOTE: It _may_ be possible to split a 32bit pseudo random integer in 2 (or 4, depending on the required bit_size)
#  to obtain more than one smaller number instead of performing two __pcg_step.
#  This could dramatically improve the efficiency of the algorithm when operating at smaller bit_size.
#  However, I can't guarantee that this does not yield a statistically worse sequence.
#  Furthermore, the algorithm to advance multiple steps at once becomes complex.
#  To improve performance it doesn't make sense to reduce the size of the state because ultimately it still
#  would rely on the same uint64 opcodes.
@pt.Subroutine(pt.TealType.bytes)
def __pcg32_bounded_sequence(
    state_slot_index: pt.Expr,
    bit_size: pt.Expr,
    lower_bound: pt.Expr,
    upper_bound: pt.Expr,
    length: pt.Expr,
) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        bit_size: pt.Int
        lower_bound: pt.Int
        upper_bound: pt.Int
        length: pt.Int

    Returns:
        pt.Bytes
    """
    result_length = pt.abi.make(pt.abi.Uint16)
    byte_size = pt.ScratchVar(pt.TealType.uint64)

    absolute_bound = pt.ScratchVar(pt.TealType.uint64)
    threshold = pt.ScratchVar(pt.TealType.uint64)
    result = pt.ScratchVar(pt.TealType.bytes)

    truncate_cached_start = pt.ScratchVar(pt.TealType.uint64)

    i = pt.ScratchVar(pt.TealType.uint64)
    candidate = pt.ScratchVar(pt.TealType.uint64)

    def __truncate_to_size(
        _n: pt.Expr, _start: pt.Expr, _byte_size: pt.Expr
    ) -> pt.Expr:
        return pt.Extract(pt.Itob(_n), _start, _byte_size)

    return pt.Seq(
        result_length.set(
            length
        ),  # This is also used because it's an assert on "length" value.
        result.store(result_length.encode()),
        pt.Assert(
            pt.Or(bit_size == pt.Int(8), bit_size == pt.Int(16), bit_size == pt.Int(32))
        ),
        # num_bits -> num_bytes == num_bits / 8 == num_bits / 2^3 == num_bits >> 3
        byte_size.store(pt.ShiftRight(bit_size, pt.Int(3))),
        # 32bit == Extract(..., 8-4, 4); 16bit == Extract(..., 8-2, 2); 8bit == Extract(..., 8-1, 1)
        truncate_cached_start.store(pt.Int(8) - byte_size.load()),
        pt.If(pt.And(lower_bound == pt.Int(0), upper_bound == pt.Int(0)))
        .Then(
            pt.Seq(
                pt.For(
                    i.store(pt.Int(0)), i.load() < length, i.store(i.load() + pt.Int(1))
                ).Do(
                    pt.Seq(
                        result.store(
                            pt.Concat(
                                result.load(),
                                __truncate_to_size(
                                    __pcg32_unbounded_random(state_slot_index),
                                    truncate_cached_start.load(),
                                    byte_size.load(),
                                ),
                            )
                        )
                    )
                )
            )
        )
        .Else(
            pt.Seq(
                pt.If(upper_bound != pt.Int(0))
                .Then(
                    pt.Seq(
                        pt.Assert(upper_bound > pt.Int(1)),
                        pt.Assert(upper_bound < pt.ShiftLeft(pt.Int(1), bit_size)),
                        # The difference in bounds must be at least 2 because otherwise, the user is just asking
                        #  for a list of "lower_bound".
                        pt.Assert(lower_bound < upper_bound - pt.Int(1)),
                        absolute_bound.store(upper_bound - lower_bound),
                    )
                )
                .Else(
                    pt.Seq(
                        # upper_bound == 0 means unbounded.
                        # Must include 2^bit_size-1 which means that lower_bound must be less than that.
                        # Otherwise, we would be in the nonsensical situation where the user is asking for a list
                        #  of "2^bit_size-1".
                        pt.Assert(
                            lower_bound < pt.ShiftLeft(pt.Int(1), bit_size) - pt.Int(1)
                        ),
                        absolute_bound.store(
                            pt.ShiftLeft(pt.Int(1), bit_size) - lower_bound
                        ),
                    )
                ),
                threshold.store(
                    __uint32_twos(absolute_bound.load()) % absolute_bound.load()
                ),
                pt.For(
                    i.store(pt.Int(0)), i.load() < length, i.store(i.load() + pt.Int(1))
                ).Do(
                    pt.Seq(
                        candidate.store(__pcg32_unbounded_random(state_slot_index)),
                        pt.While(candidate.load() < threshold.load()).Do(
                            candidate.store(__pcg32_unbounded_random(state_slot_index))
                        ),
                        result.store(
                            pt.Concat(
                                result.load(),
                                __truncate_to_size(
                                    (candidate.load() % absolute_bound.load())
                                    + lower_bound,
                                    truncate_cached_start.load(),
                                    byte_size.load(),
                                ),
                            )
                        ),
                    )
                ),
            )
        ),
        pt.Return(result.load()),
    )


@pt.Subroutine(pt.TealType.uint64)
def __pcg32_unbounded_random(state_slot_index: pt.Expr) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int

    Returns:
        pt.Int
    """
    old_state = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        old_state.store(pt.ScratchLoad(None, pt.TealType.uint64, state_slot_index)),
        __pcg32_step(state_slot_index, PCG_FIRST_INCREMENT),
        pt.Return(__pcg32_output(old_state.load())),
    )


def __pcg32_step(state_slot_index: pt.Expr, incr: pt.Expr) -> pt.Expr:
    """
    Args:
        state_slot_index: pt.Int
        incr: pt.Int

    Returns:
        None
    """
    # Equivalent to state = state * multiplier + increment
    # Considering that both operations could overflow and therefore the highest bits are discarded
    return pt.ScratchStore(
        None,
        InlineAssembly(
            "\n".join(["mulw", "bury 1", "addw", "bury 1"]),
            incr,
            PCG_MULTIPLIER,
            pt.ScratchLoad(None, pt.TealType.uint64, state_slot_index),
            type=pt.TealType.none,
        ),
        state_slot_index,
    )


# Because __pcg_rotation is inlined into this function, if we were to write the arguments
#  as full pt.Expr that would be inlined inside that function each time the arguments are called.
# Instead, we manually cache them into slots so that inside __pcg_rotation loading an argument
#  is just a load opcode.
def __pcg32_output(state: pt.Expr) -> pt.Expr:
    """
    Args:
        state: pt.Int

    Returns:
        pt.Int
    """
    arg1 = pt.ScratchVar(pt.TealType.uint64)
    arg2 = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        # This needs to be uint32. We can't guarantee that at this point, so we cast it explicitly.
        arg1.store(
            __mask_to_uint32(
                pt.ShiftRight(
                    pt.BitwiseXor(pt.ShiftRight(state, pt.Int(18)), state), pt.Int(27)
                ),
            )
        ),
        arg2.store(pt.ShiftRight(state, pt.Int(59))),
        __pcg32_rotation(arg1.load(), arg2.load()),
    )


def __pcg32_rotation(value: pt.Expr, rot: pt.Expr) -> pt.Expr:
    """
    Args:
        value: pt.Int
        rot: pt.Int

    Returns:
        pt.Int
    """
    # This needs to be uint32. Luckily, "value" is already uint32 and a right shift will maintain that invariant.
    return pt.BitwiseOr(
        pt.ShiftRight(value, rot),
        # This needs to be uint32. Therefore, we mask out the higher bits because we can't guarantee
        #  that invariant with a left shift of "rot" two's complement.
        __mask_to_uint32(
            pt.ShiftLeft(value, pt.BitwiseAnd(__uint64_twos(rot), pt.Int(31))),
        ),
    )


def __uint64_twos(number: pt.Expr) -> pt.Expr:
    """
    Args:
        number: pt.Int

    Returns:
        pt.Int
    """
    return InlineAssembly(
        "\n".join(["addw", "bury 1"]),
        pt.BitwiseNot(number),
        pt.Int(1),
        type=pt.TealType.uint64,
    )


# The value==0 case (and that case only) would still trigger a native carry (and therefore a contract panic).
# We can get away with doing this because this function is exclusively used to negate absolute_bound which,
#  by construction, can never be 0.
def __uint32_twos(value: pt.Expr) -> pt.Expr:
    """
    Args:
        value: pt.Int

    Returns:
        pt.Int
    """
    return __mask_to_uint32(pt.BitwiseNot(value) + pt.Int(1))


def __mask_to_uint32(value: pt.Expr) -> pt.Expr:
    """
    Args:
        value: pt.Int

    Returns:
        pt.Int
    """
    return pt.BitwiseAnd(value, pt.Int((1 << 32) - 1))
