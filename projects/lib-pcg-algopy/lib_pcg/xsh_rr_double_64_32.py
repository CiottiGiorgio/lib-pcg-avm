from typing import TypeAlias

from algopy import BigUInt, Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import PCG_DEFAULT_INCREMENT, PCG_SECONDARY_DEFAULT_INCREMENT
from lib_pcg.xsh_rr_64_32 import (
    __pcg32_init,
    __pcg32_output,
    __pcg32_random,
    __pcg32_step,
    __uint64_twos,
)

PCG64STATE: TypeAlias = tuple[UInt64, UInt64]


@subroutine
def pcg64_init(seed: Bytes) -> PCG64STATE:
    assert seed.length == 16

    return (
        __pcg32_init(op.extract_uint64(seed, 0), UInt64(PCG_DEFAULT_INCREMENT)),
        __pcg32_init(
            op.extract_uint64(seed, 8), UInt64(PCG_SECONDARY_DEFAULT_INCREMENT)
        ),
    )


@subroutine
def __pcg64_random(state: PCG64STATE) -> tuple[PCG64STATE, UInt64]:
    new_state1, high_prn = __pcg32_random(state[0])

    new_state2 = __pcg32_step(
        state[1], UInt64(PCG_SECONDARY_DEFAULT_INCREMENT) << (state[0] == 0)
    )

    return (new_state1, new_state2), high_prn << 32 | __pcg32_output(state[1])


@subroutine
def pcg64_random(
    state: PCG64STATE,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[PCG64STATE, Bytes]:
    result = Bytes()

    assert length < 2**16
    result += arc4.UInt16(length).bytes

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg64_random(state)

            result += op.itob(n)
    else:
        if upper_bound != 0:
            assert upper_bound > 1
            assert lower_bound < upper_bound - 1

            absolute_bound = upper_bound - lower_bound
        else:
            assert lower_bound < (2**64) - 1

            absolute_bound = op.btoi((BigUInt(2**64) - BigUInt(lower_bound)).bytes)

        threshold = __uint64_twos(absolute_bound) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state, candidate = __pcg64_random(state)
                if candidate >= threshold:
                    break
            result += op.itob((candidate % absolute_bound) + lower_bound)

    return state, result
