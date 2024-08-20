from typing import TypeAlias

from algopy import BigUInt, Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import PCG_FIRST_INCREMENT, PCG_SECOND_INCREMENT
from lib_pcg.pcg32 import (
    __pcg32_init,
    __pcg32_output,
    __pcg32_step,
    __uint64_twos,
)

PCG64STATE: TypeAlias = tuple[UInt64, UInt64]


@subroutine
def pcg64_init(seed: Bytes) -> PCG64STATE:
    """Double PCG XSH RR 64/32 initialization function the 64-bit integer generator.

    Args:
        seed: initial entropy used to initialize the state.

    Returns:
        The initialized state.

    """
    assert seed.length == 16

    return (
        __pcg32_init(op.extract_uint64(seed, 0), UInt64(PCG_FIRST_INCREMENT)),
        __pcg32_init(op.extract_uint64(seed, 8), UInt64(PCG_SECOND_INCREMENT)),
    )


@subroutine
def pcg64_random(
    state: PCG64STATE,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[PCG64STATE, arc4.DynamicArray[arc4.UInt64]]:
    """Double PCG XSH RR 64/32 generator function for 64-bit pseudo-random unsigned integers.

    Args:
        state: The state of the generator.
        lower_bound: If set to non-zero, it's the lowest (included) possible integer in the sequence.
        upper_bound: If set to non-zero, it's the highest (not included) possible integer in the sequence.
            If set to zero, the highest possible integer is the highest integer representable with 64 bits.
        length: The length of the sequence.

    upper_bound and lower_bound can be set independently of each other.
    However, they should always be set such that the desired range includes at least two numbers.

    Returns:
        A tuple of:
        - The new state of the generator.
        - A pseudo-random sequence of 64-bit uints.

    """
    result = arc4.DynamicArray[arc4.UInt64]()

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg64_unbounded_random(state)

            result.append(arc4.UInt64(n))
    else:
        if upper_bound != 0:
            assert upper_bound > 1
            assert lower_bound < upper_bound - 1

            absolute_bound = upper_bound - lower_bound
        else:
            assert lower_bound < (1 << 64) - 1

            absolute_bound = op.btoi((BigUInt(1 << 64) - BigUInt(lower_bound)).bytes)

        threshold = __uint64_twos(absolute_bound) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state, candidate = __pcg64_unbounded_random(state)
                if candidate >= threshold:
                    result.append(
                        arc4.UInt64((candidate % absolute_bound) + lower_bound)
                    )
                    break

    return state, result.copy()


@subroutine
def __pcg64_unbounded_random(state: PCG64STATE) -> tuple[PCG64STATE, UInt64]:
    """Double PCG XSH RR 64/32 next number in the sequence.

    We are concatenating two 32-bit generators in the way described by the PCG paper in chapter 4.3.4.

    Args:
        state: The state of the generator.

    Returns:
        A tuple of:
        - The new state of the generator.
        - A pseudo-random 64-bit uint.

    """
    new_state1 = __pcg32_step(state[0], UInt64(PCG_FIRST_INCREMENT))
    new_state2 = __pcg32_step(
        state[1], UInt64(PCG_SECOND_INCREMENT) << (new_state1 == 0)
    )

    return (new_state1, new_state2), __pcg32_output(state[0]) << 32 | __pcg32_output(
        state[1]
    )
