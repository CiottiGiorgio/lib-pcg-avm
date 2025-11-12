from typing import Literal

import beaker
import pyteal as pt

from lib_pcg.pcg128 import (
    pcg128_init,
    pcg128_random,
)
from smart_contracts.consts import (
    MAX_UINT128_IN_STACK_ARRAY,
)

app = beaker.Application("lib_pcg128_test_harness_pyteal")


@app.external
def get_pcg128_sequence_arc4_uint128_return(
    seed: pt.abi.StaticBytes[Literal[32]],
    lower_bound: pt.abi.StaticBytes[Literal[16]],
    upper_bound: pt.abi.StaticBytes[Literal[16]],
    length: pt.abi.Uint16,
    *,
    output: pt.abi.DynamicArray[pt.abi.StaticBytes[Literal[16]]]
) -> pt.Expr:
    rng_handle_state1 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state2 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state3 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state4 = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg128_init(
            rng_handle_state1.index(),
            rng_handle_state2.index(),
            rng_handle_state3.index(),
            rng_handle_state4.index(),
            seed.get(),
        ),
        output.decode(
            pcg128_random(
                rng_handle_state1.index(),
                rng_handle_state2.index(),
                rng_handle_state3.index(),
                rng_handle_state4.index(),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )


@app.external
def runtime_asserts_pcg128_stack_array() -> pt.Expr:
    rng_handle_state1 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state2 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state3 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state4 = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg128_init(
            rng_handle_state1.index(),
            rng_handle_state2.index(),
            rng_handle_state3.index(),
            rng_handle_state4.index(),
            pt.BytesZero(pt.Int(32)),
        ),
        pt.Pop(
            pcg128_random(
                rng_handle_state1.index(),
                rng_handle_state2.index(),
                rng_handle_state3.index(),
                rng_handle_state4.index(),
                pt.BytesZero(pt.Int(1)),
                pt.BytesZero(pt.Int(1)),
                pt.Int(MAX_UINT128_IN_STACK_ARRAY),
            )
        ),
    )


@app.external
def runtime_failure_stack_byteslice_overflow() -> pt.Expr:
    rng_handle_state1 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state2 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state3 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state4 = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg128_init(
            rng_handle_state1.index(),
            rng_handle_state2.index(),
            rng_handle_state3.index(),
            rng_handle_state4.index(),
            pt.BytesZero(pt.Int(32)),
        ),
        pt.Pop(
            pcg128_random(
                rng_handle_state1.index(),
                rng_handle_state2.index(),
                rng_handle_state3.index(),
                rng_handle_state4.index(),
                pt.BytesZero(pt.Int(1)),
                pt.BytesZero(pt.Int(1)),
                pt.Int(MAX_UINT128_IN_STACK_ARRAY + 1),
            )
        ),
    )
