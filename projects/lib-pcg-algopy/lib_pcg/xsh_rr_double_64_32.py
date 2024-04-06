from algopy import BigUInt, Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import PCG_DEFAULT_INCREMENT, PCG_SECONDARY_DEFAULT_INCREMENT
from lib_pcg.xsh_rr_64_32 import (
    __pcg32_init,
    __pcg32_output,
    __pcg32_random,
    __pcg32_step,
    __uint64_twos,
)


@subroutine
def pcg64_init(initial_state1: UInt64, initial_state2: UInt64) -> tuple[UInt64, UInt64]:
    return (
        __pcg32_init(initial_state1, UInt64(PCG_DEFAULT_INCREMENT)),
        __pcg32_init(initial_state2, UInt64(PCG_SECONDARY_DEFAULT_INCREMENT)),
    )


@subroutine
def __pcg64_random(state1: UInt64, state2: UInt64) -> tuple[UInt64, UInt64, UInt64]:
    new_state1, high_prn = __pcg32_random(state1)

    cond_incr = PCG_SECONDARY_DEFAULT_INCREMENT << (
        UInt64(0) if new_state1 != 0 else UInt64(1)
    )
    new_state2 = __pcg32_step(state2, cond_incr)

    # TODO
    # This is what we would like to write. Unfortunately PuyaPy does not yet support upcasting bool to uint64.
    # new_state2 = __pcg32_step(
    #     state2,
    #     UInt64(PCG_SECONDARY_DEFAULT_INCREMENT) << (state1 == 0)
    # )

    return new_state1, new_state2, high_prn << 32 | __pcg32_output(state2)


@subroutine
def pcg64_random(
    state1: UInt64,
    state2: UInt64,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[UInt64, UInt64, Bytes]:
    result = Bytes()

    assert length < 2**16
    result += arc4.UInt16(length).bytes

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state1, state2, n = __pcg64_random(state1, state2)

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
                state1, state2, candidate = __pcg64_random(state1, state2)
                if candidate >= threshold:
                    break
            result += op.itob((candidate % absolute_bound) + lower_bound)

    return state1, state2, result
