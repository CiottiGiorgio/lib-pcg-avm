from typing import TypeAlias

from algopy import BigUInt, Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import (
    PCG_FIRST_INCREMENT,
    PCG_FOURTH_INCREMENT,
    PCG_SECOND_INCREMENT,
    PCG_THIRD_INCREMENT,
)
from lib_pcg.xsh_rr_64_32 import (
    __pcg32_init,
    __pcg32_output,
    __pcg32_random,
    __pcg32_step,
)

PCG128STATE: TypeAlias = tuple[UInt64, UInt64, UInt64, UInt64]


@subroutine
def pcg128_init(seed: Bytes) -> PCG128STATE:
    """Quadruple PCG XSH RR 64/32 initialization function the 64-bit integer generator.

    Args:
        seed: initial entropy used to initialize the state.

    Returns:
        The initialized state.

    """
    assert seed.length == 32

    return (
        __pcg32_init(op.extract_uint64(seed, 0), UInt64(PCG_FIRST_INCREMENT)),
        __pcg32_init(
            op.extract_uint64(seed, 8), UInt64(PCG_SECOND_INCREMENT)
        ),
        __pcg32_init(
            op.extract_uint64(seed, 16), UInt64(PCG_THIRD_INCREMENT)
        ),
        __pcg32_init(
            op.extract_uint64(seed, 24), UInt64(PCG_FOURTH_INCREMENT)
        ),
    )


@subroutine
def __pcg128_random(state: PCG128STATE) -> tuple[PCG128STATE, BigUInt]:
    new_state1, rn1 = __pcg32_random(state[0])

    new_state2 = __pcg32_step(
        state[1], UInt64(PCG_SECOND_INCREMENT) << (new_state1 == 0)
    )

    new_state3 = __pcg32_step(
        state[2], UInt64(PCG_THIRD_INCREMENT) << (new_state2 == 0)
    )

    new_state4 = __pcg32_step(
        state[3], UInt64(PCG_FOURTH_INCREMENT) << (new_state3 == 0)
    )

    return (
        (new_state1, new_state2, new_state3, new_state4),
        BigUInt.from_bytes(
            op.itob(rn1 << 32 | __pcg32_output(state[1]))
            + op.itob(__pcg32_output(state[2]) << 32 | __pcg32_output(state[3]))
        ),
    )


@subroutine
def pcg128_random(
    state: PCG128STATE,
    lower_bound: BigUInt,
    upper_bound: BigUInt,
    length: UInt64,
) -> tuple[PCG128STATE, arc4.DynamicArray[arc4.UInt128]]:
    """Single PCG XSH RR 64/32 generator function for 128-bit pseudo-random big integers.

    Args:
        state: The state of the generator.
        lower_bound: If set to non-zero, it's the lowest (included) possible big integer in the sequence.
        upper_bound: If set to non-zero, it's the highest (not included) possible big integer in the sequence.
            If set to zero, the highest possible integer is the highest big integer representable with 128 bits.
        length: The length of the sequence.

    upper_bound and lower_bound can be set independently of each other.
    However, they should always be set such that the desired range includes at least two numbers.

    Returns:
        The state of the generator after generating the sequence and the generated sequence of 128-bit big integers.

    """
    result = arc4.DynamicArray[arc4.UInt128]()

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg128_random(state)

            result.append(arc4.UInt128(n))
    else:
        if upper_bound != 0:
            assert upper_bound > BigUInt(1)
            assert upper_bound < BigUInt(1 << 128)
            assert lower_bound < upper_bound - BigUInt(1)

            absolute_bound = upper_bound - lower_bound
        else:
            assert lower_bound < BigUInt(1 << 128 - 1)

            absolute_bound = BigUInt(1 << 128) - lower_bound

        threshold = __uint128_twos(absolute_bound) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state, candidate = __pcg128_random(state)
                if candidate >= threshold:
                    break
            result.append(arc4.UInt128((candidate % absolute_bound) + lower_bound))

    return state, result.copy()


# There's no way to write a general uint512 two's complement because there's no way to get a larger number than
#  an uint512 like we can do for uint64 with wide math.
# Fortunately, we don't use uint512. This code works assuming that "value: BigUInt" is an uint256.
# This code will prevent a native overflow and return a correctly masked uint256.
@subroutine
def __uint128_twos(value: BigUInt) -> BigUInt:
    wide_value_compl = (
        value
        ^ BigUInt.from_bytes(
            b"\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00\x00\x00\x00\x00"
            + b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
            + b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
        )
    ) + BigUInt(1)

    return wide_value_compl & BigUInt.from_bytes(
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
        + b"\x00\x00\x00\x00\x00\x00\x00\x00"
        + b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
        + b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
    )
