from typing import TypeAlias

from algopy import BigUInt, Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import (
    PCG_FIRST_INCREMENT,
    PCG_FOURTH_INCREMENT,
    PCG_SECOND_INCREMENT,
    PCG_THIRD_INCREMENT,
)
from lib_pcg.pcg32 import (
    __pcg32_init,
    __pcg32_output,
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
        __pcg32_init(op.extract_uint64(seed, 8), UInt64(PCG_SECOND_INCREMENT)),
        __pcg32_init(op.extract_uint64(seed, 16), UInt64(PCG_THIRD_INCREMENT)),
        __pcg32_init(op.extract_uint64(seed, 24), UInt64(PCG_FOURTH_INCREMENT)),
    )


@subroutine
def pcg128_random(
    state: PCG128STATE,
    lower_bound: BigUInt,
    upper_bound: BigUInt,
    length: UInt64,
) -> tuple[PCG128STATE, arc4.DynamicArray[arc4.UInt128]]:
    """Quadruple PCG XSH RR 64/32 generator function for 128-bit pseudo-random big integers.

    Args:
        state: The state of the generator.
        lower_bound: If set to non-zero, it's the lowest (included) possible big integer in the sequence.
        upper_bound: If set to non-zero, it's the highest (not included) possible big integer in the sequence.
            If set to zero, the highest possible integer is the highest big integer representable with 128 bits.
        length: The length of the sequence.

    upper_bound and lower_bound can be set independently of each other.
    However, they should always be set such that the desired range includes at least two numbers.

    Returns:
        A tuple of:
        - The new state of the generator.
        - A pseudo-random sequence of 128-bit uints.

    """
    result = arc4.DynamicArray[arc4.UInt128]()

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg128_unbounded_random(state)

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
                state, candidate = __pcg128_unbounded_random(state)
                if candidate >= threshold:
                    result.append(
                        arc4.UInt128((candidate % absolute_bound) + lower_bound)
                    )
                    break

    return state, result.copy()


@subroutine
def __pcg128_unbounded_random(state: PCG128STATE) -> tuple[PCG128STATE, BigUInt]:
    """Quadruple PCG XSH RR 64/32 next number in the sequence.

    We are concatenating two 32-bit generators in the way described by the PCG paper in chapter 4.3.4.

    Args:
        state: The state of the generator.

    Returns:
        A tuple of:
        - The new state of the generator.
        - A pseudo-random 128-bit uint.

    """
    new_state1 = __pcg32_step(state[0], UInt64(PCG_FIRST_INCREMENT))

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
            op.itob(__pcg32_output(state[0]) << 32 | __pcg32_output(state[1]))
            + op.itob(__pcg32_output(state[2]) << 32 | __pcg32_output(state[3]))
        ),
    )


@subroutine
def __uint128_twos(value: BigUInt) -> BigUInt:
    """Performs the two's complement on a native BigUInt.

    We need to assume for correctness of this code that the input is a non-zero BigUInt.
    In the event that the underlying representation is actually 256-bit long,
     if value == 0 then we will trigger a native BigUInt overflow.

    ~0 + 1 == ((1 << 256) - 1) + 1 == 1 << 256
    which is unrepresentable as a BigUInt.

    Fortunately, we only use this function to negate an absolute_bound which, by construction,
     is always different from zero.

    We mask the result back to 128-bit for correctness.

    Args:
        value: A BigUInt that is assumed to be a 128-bit BigUInt.

    Returns:
        The two's complement of the input value masked to 128-bit.

    """
    return (BigUInt.from_bytes(~value.bytes) + 1) & BigUInt((1 << 128) - 1)
