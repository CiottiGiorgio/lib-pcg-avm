from algopy import Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import PCG_DEFAULT_INCREMENT, PCG_DEFAULT_MULTIPLIER


@subroutine
def pcg32_init(initial_state: UInt64) -> UInt64:
    return __pcg32_init(initial_state, UInt64(PCG_DEFAULT_INCREMENT))


@subroutine
def pcg32_random(
    state: UInt64,
    bit_size: UInt64,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[UInt64, Bytes]:
    result = Bytes()

    assert length < 2**16
    result += arc4.UInt16(length).bytes

    assert bit_size == 8 or bit_size == 16 or bit_size == 32
    byte_size = bit_size >> 3
    truncate_start_cached = 8 - byte_size

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg32_random(state)

            result += op.extract(op.itob(n), truncate_start_cached, byte_size)
    else:
        if upper_bound != 0:
            assert upper_bound > 1
            assert upper_bound < (1 << bit_size)
            assert lower_bound < (upper_bound - 1)

            absolute_bound = upper_bound - lower_bound
        else:
            assert lower_bound < ((1 << bit_size) - 1)

            absolute_bound = (1 << bit_size) - lower_bound

        threshold = __mask_to_32bits(__uint64_twos(absolute_bound)) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state, candidate = __pcg32_random(state)
                if candidate >= threshold:
                    break
            result += op.extract(
                op.itob((candidate % absolute_bound) + lower_bound),
                truncate_start_cached,
                byte_size,
            )

    return state, result


@subroutine
def __pcg32_init(initial_state: UInt64, incr: UInt64) -> UInt64:
    state = __pcg32_step(UInt64(0), incr)
    _high_addw, state = op.addw(state, initial_state)

    return __pcg32_step(state, incr)


@subroutine
def __pcg32_step(state: UInt64, incr: UInt64) -> UInt64:
    _high_mul, low_mul = op.mulw(state, PCG_DEFAULT_MULTIPLIER)
    _high_add, low_add = op.addw(low_mul, incr)

    return low_add


@subroutine
def __pcg32_random(state: UInt64) -> tuple[UInt64, UInt64]:
    return __pcg32_step(state, UInt64(PCG_DEFAULT_INCREMENT)), __pcg32_output(state)


@subroutine
def __pcg32_output(value: UInt64) -> UInt64:
    return __pcg32_rotation(
        __mask_to_32bits(((value >> 18) ^ value) >> 27), value >> 59
    )


@subroutine
def __pcg32_rotation(value: UInt64, rot: UInt64) -> UInt64:
    return (value >> rot) | __mask_to_32bits(value << (__uint64_twos(rot) & 31))


@subroutine
def __uint64_twos(value: UInt64) -> UInt64:
    addw_high, addw_low = op.addw(~value, 1)

    return addw_low


@subroutine
def __mask_to_32bits(value: UInt64) -> UInt64:
    return value & ((2**32) - 1)
