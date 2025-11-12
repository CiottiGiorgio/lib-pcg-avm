from typing import Literal

import beaker
import pyteal as pt

from lib_pcg.pcg32 import (
    pcg8_init,
    pcg8_random,
    pcg16_init,
    pcg16_random,
    pcg32_init,
    pcg32_random,
)
from smart_contracts.consts import (
    MAX_UINT8_IN_STACK_ARRAY,
    MAX_UINT16_IN_STACK_ARRAY,
    MAX_UINT32_IN_STACK_ARRAY,
)

app = beaker.Application("lib_pcg32_test_harness_pyteal")


@app.external
def get_pcg32_sequence_arc4_uint32_return(
    seed: pt.abi.StaticBytes[Literal[8]],
    lower_bound: pt.abi.Uint32,
    upper_bound: pt.abi.Uint32,
    length: pt.abi.Uint16,
    *,
    output: pt.abi.DynamicArray[pt.abi.Uint32]
) -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg32_init(rng_handle.index(), seed.get()),
        output.decode(
            pcg32_random(
                rng_handle.index(),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )


@app.external
def get_pcg32_sequence_arc4_uint16_return(
    seed: pt.abi.StaticBytes[Literal[8]],
    lower_bound: pt.abi.Uint16,
    upper_bound: pt.abi.Uint16,
    length: pt.abi.Uint16,
    *,
    output: pt.abi.DynamicArray[pt.abi.Uint16]
) -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg16_init(rng_handle.index(), seed.get()),
        output.decode(
            pcg16_random(
                rng_handle.index(),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )


@app.external
def get_pcg32_sequence_arc4_uint8_return(
    seed: pt.abi.StaticBytes[Literal[8]],
    lower_bound: pt.abi.Uint8,
    upper_bound: pt.abi.Uint8,
    length: pt.abi.Uint16,
    *,
    output: pt.abi.DynamicArray[pt.abi.Uint8]
) -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg8_init(rng_handle.index(), seed.get()),
        output.decode(
            pcg8_random(
                rng_handle.index(),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )


@app.external
def runtime_asserts_pcg32_stack_array() -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg32_init(rng_handle.index(), pt.BytesZero(pt.Int(8))),
        pt.Pop(
            pcg32_random(
                rng_handle.index(),
                pt.Int(0),
                pt.Int(0),
                pt.Int(MAX_UINT32_IN_STACK_ARRAY),
            )
        ),
    )


@app.external
def runtime_asserts_pcg16_stack_array() -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg16_init(rng_handle.index(), pt.BytesZero(pt.Int(8))),
        pt.Pop(
            pcg16_random(
                rng_handle.index(),
                pt.Int(0),
                pt.Int(0),
                pt.Int(MAX_UINT16_IN_STACK_ARRAY),
            )
        ),
    )


@app.external
def runtime_asserts_pcg8_stack_array() -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg8_init(rng_handle.index(), pt.BytesZero(pt.Int(8))),
        pt.Pop(
            pcg8_random(
                rng_handle.index(),
                pt.Int(0),
                pt.Int(0),
                pt.Int(MAX_UINT8_IN_STACK_ARRAY),
            )
        ),
    )


@app.external
def runtime_failure_stack_byteslice_overflow() -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg32_init(rng_handle.index(), pt.BytesZero(pt.Int(8))),
        pt.Pop(
            pcg32_random(
                rng_handle.index(),
                pt.Int(0),
                pt.Int(0),
                pt.Int(MAX_UINT32_IN_STACK_ARRAY + 1),
            )
        ),
    )
