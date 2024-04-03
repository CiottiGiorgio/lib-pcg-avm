from typing import Literal

import beaker
import pyteal as pt
from algokit_utils import DELETABLE_TEMPLATE_NAME, UPDATABLE_TEMPLATE_NAME

from lib_pcg.xsh_rr_double_64_32 import pcg64_init, pcg64_random

app = beaker.Application(
    "lib_pcg64_exposer_pyteal",
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
def bounded_rand_uint64(
    seed: pt.abi.StaticBytes[Literal[16]],
    lower_bound: pt.abi.Uint64,
    upper_bound: pt.abi.Uint64,
    length: pt.abi.Uint16,
    *,
    output: pt.abi.DynamicArray[pt.abi.Uint64]
) -> pt.Expr:
    rng_handle_state1 = pt.ScratchVar(pt.TealType.uint64)
    rng_handle_state2 = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg64_init(
            rng_handle_state1.index(),
            rng_handle_state2.index(),
            pt.ExtractUint64(seed.get(), pt.Int(0)),
            pt.ExtractUint64(seed.get(), pt.Int(8)),
        ),
        output.decode(
            pcg64_random(
                rng_handle_state1.index(),
                rng_handle_state2.index(),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )
