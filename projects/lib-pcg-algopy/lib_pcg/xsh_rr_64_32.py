from typing import TypeAlias

from algopy import Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import PCG_FIRST_INCREMENT, PCG_MULTIPLIER

PCG32STATE: TypeAlias = UInt64


@subroutine
def pcg32_init(seed: Bytes) -> PCG32STATE:
    """Single PCG XSH RR 64/32 initialization function for all generators from 32-bits and below.

    Args:
        seed: initial entropy used to initialize the state.

    Returns:
        The initialized state.

    """
    assert seed.length == 8

    return __pcg32_init(op.btoi(seed), UInt64(PCG_FIRST_INCREMENT))


@subroutine
def pcg16_init(seed: Bytes) -> PCG32STATE:
    """
    Proxy to the real function.

    This is only used to prevent the ambiguity of calling pcg32_init with an 8 or 16 bit generator.
    """
    return pcg32_init(seed)


@subroutine
def pcg8_init(seed: Bytes) -> PCG32STATE:
    """
    Proxy to the real function.

    This is only used to prevent the ambiguity of calling pcg32_init with an 8 or 16 bit generator.
    """
    return pcg32_init(seed)


@subroutine
def pcg32_random(
    state: PCG32STATE,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[PCG32STATE, arc4.DynamicArray[arc4.UInt32]]:
    """Single PCG XSH RR 64/32 generator function for 32-bit pseudo-random unsigned integers.

    Args:
        state: The state of the generator.
        lower_bound: If set to non-zero, it's the lowest (included) possible integer in the sequence.
        upper_bound: If set to non-zero, it's the highest (not included) possible integer in the sequence.
            If set to zero, the highest possible integer is the highest integer representable with 32 bits.
        length: The length of the sequence.

    upper_bound and lower_bound can be set independently of each other.
    However, they should always be set such that the desired range includes at least two numbers.

    Returns:
        The state of the generator after generating the sequence and the generated sequence of 32-bit integers.

    """
    result = arc4.DynamicArray[arc4.UInt32]()

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg32_random(state)

            result.append(arc4.UInt32(n))
    else:
        if upper_bound != 0:
            assert upper_bound > 1
            assert upper_bound < (1 << 32)
            assert lower_bound < (upper_bound - 1)

            absolute_bound = upper_bound - lower_bound
        else:
            assert lower_bound < ((1 << 32) - 1)

            absolute_bound = (1 << 32) - lower_bound

        threshold = __mask_to_32bits(__uint64_twos(absolute_bound)) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state, candidate = __pcg32_random(state)
                if candidate >= threshold:
                    break
            result.append(arc4.UInt32((candidate % absolute_bound) + lower_bound))

    return state, result.copy()


@subroutine
def pcg16_random(
    state: PCG32STATE,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[PCG32STATE, arc4.DynamicArray[arc4.UInt16]]:
    """Single PCG XSH RR 64/32 generator for 16-bit pseudo-random unsigned integers.

    Args:
        state: The state of the generator.
        lower_bound: If set to non-zero, it's the lowest (included) possible integer in the sequence.
        upper_bound: If set to non-zero, it's the highest (not included) possible integer in the sequence.
            If set to zero, the highest possible integer is the highest integer representable with 16 bits.
        length: The length of the sequence.

    upper_bound and lower_bound can be set independently of each other.
    However, they should always be set such that the desired range includes at least two numbers.

    Returns:
        The state of the generator after generating the sequence and the generated sequence of 16-bit integers.

    """
    result = arc4.DynamicArray[arc4.UInt16]()

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg32_random(state)

            result.append(arc4.UInt16(n))
    else:
        if upper_bound != 0:
            assert upper_bound > 1
            assert upper_bound < (1 << 16)
            assert lower_bound < (upper_bound - 1)

            absolute_bound = upper_bound - lower_bound
        else:
            assert lower_bound < ((1 << 16) - 1)

            absolute_bound = (1 << 16) - lower_bound

        threshold = __mask_to_32bits(__uint64_twos(absolute_bound)) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state, candidate = __pcg32_random(state)
                if candidate >= threshold:
                    break
            result.append(arc4.UInt16((candidate % absolute_bound) + lower_bound))

    return state, result.copy()


@subroutine
def pcg8_random(
    state: PCG32STATE,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[PCG32STATE, arc4.DynamicArray[arc4.UInt8]]:
    """Single PCG XSH RR 64/32 generator for 8-bit pseudo-random unsigned integers.

    Args:
        state: The state of the generator.
        lower_bound: If set to non-zero, it's the lowest (included) possible integer in the sequence.
        upper_bound: If set to non-zero, it's the highest (not included) possible integer in the sequence.
            If set to zero, the highest possible integer is the highest integer representable with 8 bits.
        length: The length of the sequence.

    upper_bound and lower_bound can be set independently of each other.
    However, they should always be set such that the desired range includes at least two numbers.

    Returns:
        The state of the generator after generating the sequence and the generated sequence of 8-bit integers.

    """
    result = arc4.DynamicArray[arc4.UInt8]()

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg32_random(state)

            result.append(arc4.UInt8(n))
    else:
        if upper_bound != 0:
            assert upper_bound > 1
            assert upper_bound < (1 << 8)
            assert lower_bound < (upper_bound - 1)

            absolute_bound = upper_bound - lower_bound
        else:
            assert lower_bound < ((1 << 8) - 1)

            absolute_bound = (1 << 8) - lower_bound

        threshold = __mask_to_32bits(__uint64_twos(absolute_bound)) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state, candidate = __pcg32_random(state)
                if candidate >= threshold:
                    break
            result.append(arc4.UInt8((candidate % absolute_bound) + lower_bound))

    return state, result.copy()


@subroutine
def __pcg32_init(initial_state: PCG32STATE, incr: UInt64) -> PCG32STATE:
    state = __pcg32_step(UInt64(0), incr)
    _high_addw, state = op.addw(state, initial_state)

    return __pcg32_step(state, incr)


@subroutine
def __pcg32_step(state: PCG32STATE, incr: UInt64) -> PCG32STATE:
    _high_mul, low_mul = op.mulw(state, PCG_MULTIPLIER)
    _high_add, low_add = op.addw(low_mul, incr)

    return low_add


@subroutine
def __pcg32_random(state: PCG32STATE) -> tuple[PCG32STATE, UInt64]:
    return __pcg32_step(state, UInt64(PCG_FIRST_INCREMENT)), __pcg32_output(state)


@subroutine
def __pcg32_output(value: PCG32STATE) -> UInt64:
    return __pcg32_rotation(
        __mask_to_32bits(((value >> 18) ^ value) >> 27), value >> 59
    )


@subroutine
def __pcg32_rotation(value: UInt64, rot: UInt64) -> UInt64:
    return (value >> rot) | __mask_to_32bits(value << (__uint64_twos(rot) & 31))


@subroutine
def __uint64_twos(value: UInt64) -> UInt64:
    _addw_high, addw_low = op.addw(~value, 1)

    return addw_low


@subroutine
def __mask_to_32bits(value: UInt64) -> UInt64:
    return value & ((1 << 32) - 1)
