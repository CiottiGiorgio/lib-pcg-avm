from typing import Literal

import beaker
import pyteal as pt
from algokit_utils import DELETABLE_TEMPLATE_NAME, UPDATABLE_TEMPLATE_NAME

from lib_pcg.pcg128 import pcg128_init, pcg128_random

app = beaker.Application(
    "lib_pcg128_exposer_pyteal",
)


@app.update(authorize=beaker.Authorize.only_creator(), bare=True)
def update() -> pt.Expr:
    return pt.Assert(
        pt.Tmpl.Int(UPDATABLE_TEMPLATE_NAME),
        comment="Check app is updatable",
    )


@app.delete(authorize=beaker.Authorize.only_creator(), bare=True)
def delete() -> pt.Expr:
    return pt.Assert(
        pt.Tmpl.Int(DELETABLE_TEMPLATE_NAME),
        comment="Check app is deletable",
    )


@app.external
def bounded_rand_uint128(
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
