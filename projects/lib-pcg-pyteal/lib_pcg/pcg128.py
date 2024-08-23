import pyteal as pt

from lib_pcg.consts import (
    PCG_FIRST_INCREMENT,
    PCG_FOURTH_INCREMENT,
    PCG_SECOND_INCREMENT,
    PCG_THIRD_INCREMENT,
)
from lib_pcg.pcg32 import (
    __pcg32_init,
    __pcg32_output,
    __pcg32_step,
)


@pt.Subroutine(pt.TealType.none)
def pcg128_init(
    state1_slot_index: pt.Expr,
    state2_slot_index: pt.Expr,
    state3_slot_index: pt.Expr,
    state4_slot_index: pt.Expr,
    seed: pt.Expr,
) -> pt.Expr:
    """
    Args:
        state1_slot_index: pt.Int
        state2_slot_index: pt.Int
        state3_slot_index: pt.Int
        state4_slot_index: pt.Int
        seed: pt.Bytes

    Returns:
        None
    """
    return pt.Seq(
        pt.Assert(pt.Len(seed) == pt.Int(32)),
        __pcg32_init(
            state1_slot_index, pt.ExtractUint64(seed, pt.Int(0)), PCG_FIRST_INCREMENT
        ),
        __pcg32_init(
            state2_slot_index, pt.ExtractUint64(seed, pt.Int(8)), PCG_SECOND_INCREMENT
        ),
        __pcg32_init(
            state3_slot_index, pt.ExtractUint64(seed, pt.Int(16)), PCG_THIRD_INCREMENT
        ),
        __pcg32_init(
            state4_slot_index, pt.ExtractUint64(seed, pt.Int(24)), PCG_FOURTH_INCREMENT
        ),
    )


@pt.Subroutine(pt.TealType.bytes)
def pcg128_random(
    state1_slot_index: pt.Expr,
    state2_slot_index: pt.Expr,
    state3_slot_index: pt.Expr,
    state4_slot_index: pt.Expr,
    lower_bound: pt.Expr,
    upper_bound: pt.Expr,
    length: pt.Expr,
) -> pt.Expr:
    """
    Args:
        state1_slot_index: pt.Int
        state2_slot_index: pt.Int
        state3_slot_index: pt.Int
        state4_slot_index: pt.Int
        lower_bound: pt.Bytes
        upper_bound: pt.Bytes
        length: pt.Int

    Returns:
        pt.Bytes
    """
    result_length = pt.abi.make(pt.abi.Uint16)

    absolute_bound = pt.ScratchVar(pt.TealType.bytes)
    threshold = pt.ScratchVar(pt.TealType.bytes)
    result = pt.ScratchVar(pt.TealType.bytes)

    i = pt.ScratchVar(pt.TealType.uint64)
    candidate = pt.ScratchVar(pt.TealType.bytes)

    return pt.Seq(
        result_length.set(
            length
        ),  # This is also used because it's an assert on "length" value.
        result.store(result_length.encode()),
        pt.If(
            pt.And(
                pt.BytesEq(lower_bound, pt.Bytes((0).to_bytes(32, "big"))),
                pt.BytesEq(upper_bound, pt.Bytes((0).to_bytes(32, "big"))),
            )
        )
        .Then(
            pt.Seq(
                pt.For(
                    i.store(pt.Int(0)), i.load() < length, i.store(i.load() + pt.Int(1))
                ).Do(
                    pt.Seq(
                        result.store(
                            pt.Concat(
                                result.load(),
                                __pcg128_unbounded_random(
                                    state1_slot_index,
                                    state2_slot_index,
                                    state3_slot_index,
                                    state4_slot_index,
                                ),
                            )
                        )
                    )
                )
            )
        )
        .Else(
            pt.Seq(
                pt.If(pt.BytesNeq(upper_bound, pt.Bytes((0).to_bytes(32, "big"))))
                .Then(
                    pt.Seq(
                        pt.Assert(
                            pt.BytesGt(upper_bound, pt.Bytes((1).to_bytes(32, "big")))
                        ),
                        pt.Assert(
                            pt.BytesLt(
                                upper_bound, pt.Bytes((1 << 128).to_bytes(32, "big"))
                            )
                        ),
                        pt.Assert(
                            pt.BytesLt(
                                lower_bound,
                                pt.BytesMinus(
                                    upper_bound, pt.Bytes((1).to_bytes(32, "big"))
                                ),
                            )
                        ),
                        absolute_bound.store(pt.BytesMinus(upper_bound, lower_bound)),
                    )
                )
                .Else(
                    pt.Seq(
                        pt.Assert(
                            pt.BytesLt(
                                lower_bound,
                                pt.Bytes(((1 << 128) - 1).to_bytes(32, "big")),
                            )
                        ),
                        # Here we would like to write 2**128 - lower_bound. Problem is that 2 ** 64 is unrepresentable
                        #  with a single uint64.
                        # We will write this operation with bigint math and optimize it later.
                        # At this point it's guaranteed that lower_bound != 0.
                        absolute_bound.store(
                            pt.BytesMinus(
                                pt.Bytes((1 << 128).to_bytes(32, "big")), lower_bound
                            )
                        ),
                    )
                ),
                threshold.store(
                    pt.BytesMod(
                        __uint128_twos(absolute_bound.load()), absolute_bound.load()
                    )
                ),
                pt.For(
                    i.store(pt.Int(0)), i.load() < length, i.store(i.load() + pt.Int(1))
                ).Do(
                    pt.Seq(
                        candidate.store(
                            __pcg128_unbounded_random(
                                state1_slot_index,
                                state2_slot_index,
                                state3_slot_index,
                                state4_slot_index,
                            ),
                        ),
                        pt.While(pt.BytesLt(candidate.load(), threshold.load())).Do(
                            candidate.store(
                                __pcg128_unbounded_random(
                                    state1_slot_index,
                                    state2_slot_index,
                                    state3_slot_index,
                                    state4_slot_index,
                                ),
                            ),
                        ),
                        result.store(
                            pt.Concat(
                                result.load(),
                                pt.BytesOr(
                                    pt.BytesZero(pt.Int(16)),
                                    pt.BytesAdd(
                                        pt.BytesMod(
                                            candidate.load(), absolute_bound.load()
                                        ),
                                        lower_bound,
                                    ),
                                ),
                            )
                        ),
                    )
                ),
            )
        ),
        pt.Return(result.load()),
    )


@pt.Subroutine(pt.TealType.bytes)
def __pcg128_unbounded_random(
    state1_slot_index: pt.Expr,
    state2_slot_index: pt.Expr,
    state3_slot_index: pt.Expr,
    state4_slot_index: pt.Expr,
) -> pt.Expr:
    """
    Args:
        state1_slot_index: pt.Int
        state2_slot_index: pt.Int
        state3_slot_index: pt.Int
        state4_slot_index: pt.Int

    Returns:
        pt.Bytes
    """
    old_state1 = pt.ScratchVar(pt.TealType.uint64)
    old_state2 = pt.ScratchVar(pt.TealType.uint64)
    old_state3 = pt.ScratchVar(pt.TealType.uint64)
    old_state4 = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        old_state1.store(pt.ScratchLoad(None, pt.TealType.uint64, state1_slot_index)),
        old_state2.store(pt.ScratchLoad(None, pt.TealType.uint64, state2_slot_index)),
        old_state3.store(pt.ScratchLoad(None, pt.TealType.uint64, state3_slot_index)),
        old_state4.store(pt.ScratchLoad(None, pt.TealType.uint64, state4_slot_index)),
        __pcg32_step(state1_slot_index, PCG_FIRST_INCREMENT),
        __pcg32_step(
            state2_slot_index,
            pt.ShiftLeft(
                PCG_SECOND_INCREMENT,
                pt.ScratchLoad(None, pt.TealType.uint64, state1_slot_index)
                == pt.Int(0),
            ),
        ),
        __pcg32_step(
            state3_slot_index,
            pt.ShiftLeft(
                PCG_THIRD_INCREMENT,
                pt.ScratchLoad(None, pt.TealType.uint64, state2_slot_index)
                == pt.Int(0),
            ),
        ),
        __pcg32_step(
            state4_slot_index,
            pt.ShiftLeft(
                PCG_FOURTH_INCREMENT,
                pt.ScratchLoad(None, pt.TealType.uint64, state3_slot_index)
                == pt.Int(0),
            ),
        ),
        pt.Return(
            pt.Concat(
                pt.Itob(
                    pt.BitwiseOr(
                        pt.ShiftLeft(__pcg32_output(old_state1.load()), pt.Int(32)),
                        __pcg32_output(old_state2.load()),
                    )
                ),
                pt.Itob(
                    pt.BitwiseOr(
                        pt.ShiftLeft(__pcg32_output(old_state3.load()), pt.Int(32)),
                        __pcg32_output(old_state4.load()),
                    )
                ),
            )
        ),
    )


def __uint128_twos(value: pt.Expr) -> pt.Expr:
    """
    Args:
        value: pt.Bytes

    Returns:
        pt.Bytes
    """
    return pt.BytesAnd(
        pt.BytesAdd(pt.BytesNot(value), pt.Bytes((1).to_bytes(32, "big"))),
        pt.Bytes(((1 << 128) - 1).to_bytes(16, "big")),
    )
