from typing import TypeAlias

from algopy import Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import PCG_DEFAULT_INCREMENT, PCG_DEFAULT_MULTIPLIER

PCG32STATE: TypeAlias = UInt64


@subroutine
def pcg32_init(seed: Bytes) -> PCG32STATE:
    assert seed.length == 8

    return __pcg32_init(op.btoi(seed), UInt64(PCG_DEFAULT_INCREMENT))


@subroutine
def pcg32_random(
    state: PCG32STATE,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[PCG32STATE, arc4.DynamicArray[arc4.UInt32]]:
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
    _high_mul, low_mul = op.mulw(state, PCG_DEFAULT_MULTIPLIER)
    _high_add, low_add = op.addw(low_mul, incr)

    return low_add


@subroutine
def __pcg32_random(state: PCG32STATE) -> tuple[PCG32STATE, UInt64]:
    return __pcg32_step(state, UInt64(PCG_DEFAULT_INCREMENT)), __pcg32_output(state)


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
