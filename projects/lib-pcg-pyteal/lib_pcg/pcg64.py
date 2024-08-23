import pyteal as pt

from lib_pcg.consts import PCG_FIRST_INCREMENT, PCG_SECOND_INCREMENT
from lib_pcg.pcg32 import (
    __pcg32_init,
    __pcg32_output,
    __pcg32_step,
    __uint64_twos,
)


@pt.Subroutine(pt.TealType.none)
def pcg64_init(
    state1_slot_index: pt.Expr,
    state2_slot_index: pt.Expr,
    seed: pt.Expr,
) -> pt.Expr:
    return pt.Seq(
        pt.Assert(pt.Len(seed) == pt.Int(16)),
        __pcg32_init(
            state1_slot_index, pt.ExtractUint64(seed, pt.Int(0)), PCG_FIRST_INCREMENT
        ),
        __pcg32_init(
            state2_slot_index, pt.ExtractUint64(seed, pt.Int(8)), PCG_SECOND_INCREMENT
        ),
    )


@pt.Subroutine(pt.TealType.bytes)
def pcg64_random(
    state1_slot_index: pt.Expr,
    state2_slot_index: pt.Expr,
    lower_bound: pt.Expr,
    upper_bound: pt.Expr,
    length: pt.Expr,
) -> pt.Expr:
    result_length = pt.abi.make(pt.abi.Uint16)

    absolute_bound = pt.ScratchVar(pt.TealType.uint64)
    threshold = pt.ScratchVar(pt.TealType.uint64)
    result = pt.ScratchVar(pt.TealType.bytes)

    i = pt.ScratchVar(pt.TealType.uint64)
    candidate = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        result_length.set(
            length
        ),  # This is also used because it's an assert on "length" value.
        result.store(result_length.encode()),
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
                                pt.Itob(
                                    __pcg64_unbounded_random(
                                        state1_slot_index, state2_slot_index
                                    )
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
                        pt.Assert(lower_bound < upper_bound - pt.Int(1)),
                        absolute_bound.store(upper_bound - lower_bound),
                    )
                )
                .Else(
                    pt.Seq(
                        pt.Assert(lower_bound < pt.Int(2**64 - 1)),
                        # Here we would like to write 2**64 - lower_bound. Problem is that 2 ** 64 is unrepresentable
                        #  with a single uint64.
                        # We will write this operation with bigint math and optimize it later.
                        # At this point it's guaranteed that lower_bound != 0.
                        absolute_bound.store(
                            pt.Btoi(
                                pt.BytesMinus(
                                    pt.Bytes(b"\x01\x00\x00\x00\x00\x00\x00\x00\x00"),
                                    pt.Itob(lower_bound),
                                )
                            )
                        ),
                    )
                ),
                threshold.store(
                    __uint64_twos(absolute_bound.load()) % absolute_bound.load()
                ),
                pt.For(
                    i.store(pt.Int(0)), i.load() < length, i.store(i.load() + pt.Int(1))
                ).Do(
                    pt.Seq(
                        candidate.store(
                            __pcg64_unbounded_random(
                                state1_slot_index, state2_slot_index
                            )
                        ),
                        pt.While(candidate.load() < threshold.load()).Do(
                            candidate.store(
                                __pcg64_unbounded_random(
                                    state1_slot_index, state2_slot_index
                                )
                            ),
                        ),
                        result.store(
                            pt.Concat(
                                result.load(),
                                pt.Itob(
                                    (candidate.load() % absolute_bound.load())
                                    + lower_bound
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
def __pcg64_unbounded_random(
    state1_slot_index: pt.Expr, state2_slot_index: pt.Expr
) -> pt.Expr:
    old_state1 = pt.ScratchVar(pt.TealType.uint64)
    old_state2 = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        old_state1.store(pt.ScratchLoad(None, pt.TealType.uint64, state1_slot_index)),
        old_state2.store(pt.ScratchLoad(None, pt.TealType.uint64, state2_slot_index)),
        __pcg32_step(state1_slot_index, PCG_FIRST_INCREMENT),
        # We want to do the "carry" on the second generator if the first reached 0.
        # This is kind of an arbitrary way of composing two 2^64 period generators into a single 2^128 period.
        # The paper has more details on chapter 3.4.3
        # We want that the next increment is multiplied by 2. We do this in a branchless way.
        # "* 2" == "<< 1". We use the boolean result of comparing the first state with 0 as the input for the shift.
        # Since __pcg32_step is inlined, this should result in a reduction in code size
        #  (because we don't write explicitly both cases).
        # TODO: As an optimization, it's always possible to do the "second" increment after a step with the
        #  "normal" increment.
        #  If we find out that it's possible to do both steps with fewer opcodes (by using bigint math or by
        #  SIMDing), this could result in faster code.
        #  E.G.:
        #  __simd_pcg32_step1_2,
        #  if pcg1.state == 0 then pcg2.state += PCG_SECONDARY_DEFAULT_INCREMENT
        __pcg32_step(
            state2_slot_index,
            pt.ShiftLeft(
                PCG_SECOND_INCREMENT,
                pt.ScratchLoad(None, pt.TealType.uint64, state1_slot_index)
                == pt.Int(0),
            ),
        ),
        pt.Return(
            pt.BitwiseOr(
                pt.ShiftLeft(__pcg32_output(old_state1.load()), pt.Int(32)),
                __pcg32_output(old_state2.load()),
            )
        ),
    )
