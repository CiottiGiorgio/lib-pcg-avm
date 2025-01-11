from typing import TypeAlias

from algopy import Bytes, UInt64, arc4, op, subroutine, urange

from lib_pcg.consts import PCG_FIRST_INCREMENT, PCG_MULTIPLIER

PCG32STATE: TypeAlias = UInt64


@subroutine
def pcg32_init(seed: Bytes) -> PCG32STATE:
    """Single PCG XSH RR 64/32 initialization function for all generators from 32-bits and below.

    Args:
        seed: Initial entropy used to initialize the state.

    Returns:
        The initialized state.

    """
    assert seed.length == 8

    return __pcg32_init(op.btoi(seed), UInt64(PCG_FIRST_INCREMENT))


@subroutine
def pcg16_init(seed: Bytes) -> PCG32STATE:
    """Proxy to the real function.

    This is only used to prevent the ambiguity of calling pcg32_init with an 8 or 16 bit generator.

    """
    return pcg32_init(seed)


@subroutine
def pcg8_init(seed: Bytes) -> PCG32STATE:
    """Proxy to the real function.

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
        A tuple of:
        - The new state of the generator.
        - A pseudo-random sequence of 32-bit uints.

    """
    state, sequence = __pcg32_bounded_sequence(
        state, UInt64(32), lower_bound, upper_bound, length
    )
    return state, arc4.DynamicArray[arc4.UInt32].from_bytes(sequence)


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
        A tuple of:
        - The new state of the generator.
        - A pseudo-random sequence of 16-bit uints.

    """
    state, sequence = __pcg32_bounded_sequence(
        state, UInt64(16), lower_bound, upper_bound, length
    )
    return state, arc4.DynamicArray[arc4.UInt16].from_bytes(sequence)


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
        A tuple of:
        - The new state of the generator.
        - A pseudo-random sequence of 8-bit uints.

    """
    state, sequence = __pcg32_bounded_sequence(
        state, UInt64(8), lower_bound, upper_bound, length
    )
    return state, arc4.DynamicArray[arc4.UInt8].from_bytes(sequence)


@subroutine
def __pcg32_init(initial_state: PCG32STATE, incr: UInt64) -> PCG32STATE:
    """PCG XSH RR 64/32 state initialization.

    Notably, we perform a second step after initializing the generator because it primes it for
     the first number that we are going to generate.
    More details in __pcg32_unbounded_random() subroutine.

    Args:
        initial_state: Initial entropy used to initialize the state.
        incr: Constant used in the modulo addition.

    Returns:
        The properly initialized state of the generator.

    """
    state = __pcg32_step(UInt64(0), incr)
    _high_addw, state = op.addw(state, initial_state)

    return __pcg32_step(state, incr)


@subroutine
def __pcg32_bounded_sequence(
    state: PCG32STATE,
    bit_size: UInt64,
    lower_bound: UInt64,
    upper_bound: UInt64,
    length: UInt64,
) -> tuple[PCG32STATE, Bytes]:
    """PCG XSH RR 64/32 sequence of bounded arbitrary (8/16/32)-bit integers.

    This is the underlying function that generates the sequence for all public facing pcg32_random functions.
    Since subroutines don't (currently) support any form of overloading/templating,
     all public facing pcg32_random functions are just proxies to this function that provide a static signature and
     do the expected casting explicitly.
    Constructing the sequence by manipulating Bytes directly is also more efficient and leads to better opcode economy.
    Also, bundling all the logic in a single function reduces code duplication and library size.

    Args:
        state: The state of the generator.
        bit_size: Either 8, 16, or 32 integer.
        lower_bound: If set to non-zero, it's the lowest (included) possible integer in the sequence.
        upper_bound: If set to non-zero, it's the highest (not included) possible integer in the sequence.
            If set to zero, the highest possible integer is the highest integer representable with 8 bits.
        length: The length of the sequence.

    upper_bound and lower_bound can be set independently of each other.
    However, they should always be set such that the desired range includes at least two numbers.

    Returns:
        A tuple of:
        - The new state of the generator.
        - A pseudo-random 32-bit uint.

    """
    result = Bytes()

    assert length < 2**16
    result += arc4.UInt16(length).bytes

    assert bit_size == 8 or bit_size == 16 or bit_size == 32
    byte_size = bit_size >> 3
    truncate_start_cached = 8 - byte_size

    if lower_bound == 0 and upper_bound == 0:
        for i in urange(length):  # noqa: B007
            state, n = __pcg32_unbounded_random(state)

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

        threshold = __mask_to_uint32(__uint64_twos(absolute_bound)) % absolute_bound

        for i in urange(length):  # noqa: B007
            while True:
                state, candidate = __pcg32_unbounded_random(state)
                if candidate >= threshold:
                    result += op.extract(
                        op.itob((candidate % absolute_bound) + lower_bound),
                        truncate_start_cached,
                        byte_size,
                    )
                    break

    return state, result


@subroutine(inline=True)
def __pcg32_unbounded_random(state: PCG32STATE) -> tuple[PCG32STATE, UInt64]:
    """PCG XSH RR 64/32 next number in the sequence.

    Notably, the C reference implementation advanced the state _after_ passing it to the output function.
    This is done because on traditional machines this would result in machine code that computes
     the output and the step in parallel (instead of one depending on the result of the other).

    Args:
        state: The state of the generator.

    Returns:
        A tuple of:
        - The new state of the generator.
        - A pseudo-random sequence of <bit_size>-bit uints.

    """
    return __pcg32_step(state, UInt64(PCG_FIRST_INCREMENT)), __pcg32_output(state)


@subroutine
def __pcg32_step(state: PCG32STATE, incr: UInt64) -> PCG32STATE:
    """PCG XSH RR 64/32 single step advance in the underlying LCG.

    Args:
        state: The state of the generator.
        incr: Constant used in the modulo addition.

    Returns:
        The new state of the generator.

    """
    _high_mul, low_mul = op.mulw(state, PCG_MULTIPLIER)
    _high_add, low_add = op.addw(low_mul, incr)

    return low_add


@subroutine(inline=True)
def __pcg32_output(state: PCG32STATE) -> UInt64:
    """PCG XSH RR 64/32 output k-to-1 permutation function."""
    return __pcg32_rotation(
        __mask_to_uint32(((state >> 18) ^ state) >> 27), state >> 59
    )


@subroutine(inline=True)
def __pcg32_rotation(value: UInt64, rot: UInt64) -> UInt64:
    """PCG XSH RR 64/32 rotation function."""
    return (value >> rot) | __mask_to_uint32(value << (__uint64_twos(rot) & 31))


@subroutine(inline=True)
def __uint64_twos(value: UInt64) -> UInt64:
    """Performs the two's complement on a native uint64."""
    _addw_high, addw_low = op.addw(~value, 1)

    return addw_low


@subroutine(inline=True)
def __mask_to_uint32(value: UInt64) -> UInt64:
    """Sets input's highest 32 bits to zero."""
    return value & ((1 << 32) - 1)
