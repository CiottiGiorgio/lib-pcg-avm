import beaker
import pyteal as pt
from algokit_utils import DELETABLE_TEMPLATE_NAME, UPDATABLE_TEMPLATE_NAME

from lib_pcg.xsh_rr_64_32 import pcg32_init, pcg32_random

app = beaker.Application(
    "lib_pcg32_exposer",
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
def bounded_rand_uint32(
    seed: pt.abi.Uint64,
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
                pt.Int(32),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )


@app.external
def bounded_rand_uint16(
    seed: pt.abi.Uint64,
    lower_bound: pt.abi.Uint16,
    upper_bound: pt.abi.Uint16,
    length: pt.abi.Uint16,
    *,
    output: pt.abi.DynamicArray[pt.abi.Uint16]
) -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg32_init(rng_handle.index(), seed.get()),
        output.decode(
            pcg32_random(
                rng_handle.index(),
                pt.Int(16),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )


@app.external
def bounded_rand_uint8(
    seed: pt.abi.Uint64,
    lower_bound: pt.abi.Uint8,
    upper_bound: pt.abi.Uint8,
    length: pt.abi.Uint16,
    *,
    output: pt.abi.DynamicArray[pt.abi.Uint8]
) -> pt.Expr:
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        pcg32_init(rng_handle.index(), seed.get()),
        output.decode(
            pcg32_random(
                rng_handle.index(),
                pt.Int(8),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )
