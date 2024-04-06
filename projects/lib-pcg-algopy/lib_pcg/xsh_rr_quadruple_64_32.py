from algopy import BigUInt, Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import (
    PCG_DEFAULT_INCREMENT,
    PCG_QUATERNARY_DEFAULT_INCREMENT,
    PCG_SECONDARY_DEFAULT_INCREMENT,
    PCG_TERTIARY_DEFAULT_INCREMENT,
)
from lib_pcg.xsh_rr_64_32 import (
    __pcg32_init,
    __pcg32_output,
    __pcg32_random,
    __pcg32_step,
)


@subroutine
def pcg128_init(seed: Bytes) -> tuple[UInt64, UInt64, UInt64, UInt64]:
    assert seed.length == 32

    return (
        __pcg32_init(op.extract_uint64(seed, 0), UInt64(PCG_DEFAULT_INCREMENT)),
        __pcg32_init(
            op.extract_uint64(seed, 8), UInt64(PCG_SECONDARY_DEFAULT_INCREMENT)
        ),
        __pcg32_init(
            op.extract_uint64(seed, 16), UInt64(PCG_TERTIARY_DEFAULT_INCREMENT)
        ),
        __pcg32_init(
            op.extract_uint64(seed, 24), UInt64(PCG_QUATERNARY_DEFAULT_INCREMENT)
        ),
    )


@subroutine
def __pcg128_random(
    state: tuple[UInt64, UInt64, UInt64, UInt64]
) -> tuple[UInt64, UInt64, UInt64, UInt64, BigUInt]:
    new_state1, rn1 = __pcg32_random(state[0])

    cond_incr = PCG_SECONDARY_DEFAULT_INCREMENT << (
        UInt64(0) if new_state1 != 0 else UInt64(1)
    )
    new_state2 = __pcg32_step(state[1], cond_incr)

    cond_incr = PCG_TERTIARY_DEFAULT_INCREMENT << (
        UInt64(0) if new_state2 != 0 else UInt64(1)
    )
    new_state3 = __pcg32_step(state[2], cond_incr)

    cond_incr = PCG_QUATERNARY_DEFAULT_INCREMENT << (
        UInt64(0) if new_state3 != 0 else UInt64(1)
    )
    new_state4 = __pcg32_step(state[3], cond_incr)

    return (
        new_state1,
        new_state2,
        new_state3,
        new_state4,
        BigUInt.from_bytes(
            op.itob(rn1 << 32 | __pcg32_output(state[1]))
            + op.itob(__pcg32_output(state[2]) << 32 | __pcg32_output(state[3]))
        ),
    )


# There's no way to write a general uint512 two's complement because there's no way to get a larger number than
#  an uint512 like we can do for uint64 with wide math.
# Fortunately, we don't use uint512. This code works assuming that "value: BigUInt" is an uint256.
# This code will prevent a native overflow and return a correctly masked uint256.
@subroutine
def __pcg128_twos(value: BigUInt) -> BigUInt:
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


@subroutine
def pcg128_random(
    state: tuple[UInt64, UInt64, UInt64, UInt64],
    lower_bound: BigUInt,
    upper_bound: BigUInt,
    length: UInt64,
) -> tuple[UInt64, UInt64, UInt64, UInt64, Bytes]:
    result = Bytes()

    assert length < 2**16
    result += arc4.UInt16(length).bytes

    state1, state2, state3, state4 = state
    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state1, state2, state3, state4, n = __pcg128_random(
                (state1, state2, state3, state4)
            )

            result += n.bytes
    else:
        if upper_bound != 0:
            assert upper_bound > BigUInt(1)
            assert lower_bound < upper_bound - BigUInt(1)

            absolute_bound = upper_bound - lower_bound
        else:
            assert lower_bound < BigUInt(2**256 - 1)

            absolute_bound = BigUInt(2**256) - lower_bound

        threshold = __pcg128_twos(absolute_bound) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state1, state2, state3, state4, candidate = __pcg128_random(
                    (state1, state2, state3, state4)
                )
                if candidate >= threshold:
                    break
            result += candidate.bytes

    return state1, state2, state3, state4, result
