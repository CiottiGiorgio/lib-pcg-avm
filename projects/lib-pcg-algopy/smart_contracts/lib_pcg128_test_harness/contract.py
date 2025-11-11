from typing import Literal

from algopy import ARC4Contract, Array, BigUInt, UInt64, arc4, op
from algopy.arc4 import abimethod

from lib_pcg import pcg128_init, pcg128_random
from lib_pcg.pcg128 import pcg128_random_arc4_uint128
from smart_contracts.consts import MAX_BIGUINT_IN_STACK_ARRAY


class LibPCG128TestHarnessAlgoPy(ARC4Contract):
    @abimethod
    def get_pcg128_sequence_native_biguint_return(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[32]],
        lower_bound: arc4.UInt128,
        upper_bound: arc4.UInt128,
        length: arc4.UInt16,
    ) -> Array[BigUInt]:
        state = pcg128_init(seed.bytes)

        state, sequence = pcg128_random(
            state,
            lower_bound.as_biguint(),
            upper_bound.as_biguint(),
            length.as_uint64(),
        )

        return sequence

    @abimethod
    def get_pcg128_sequence_arc4_uint128_return(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[32]],
        lower_bound: arc4.UInt128,
        upper_bound: arc4.UInt128,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt128]:
        state = pcg128_init(seed.bytes)

        state, sequence = pcg128_random_arc4_uint128(
            state,
            lower_bound.as_biguint(),
            upper_bound.as_biguint(),
            length.as_uint64(),
        )

        return sequence

    @abimethod
    def runtime_asserts_stack_array_native_biguint(self) -> None:
        state = pcg128_init(op.bzero(32))

        # Can produce a maximal length stack-based array of biguints.
        state, sequence = pcg128_random(
            state, BigUInt(0), BigUInt(0), UInt64(MAX_BIGUINT_IN_STACK_ARRAY)
        )

    @abimethod
    def runtime_asserts_stack_array_arc4_uint128(self) -> None:
        state = pcg128_init(op.bzero(32))

        # Can produce a maximal length stack-based array of uint64s.
        state, sequence = pcg128_random_arc4_uint128(
            state, BigUInt(0), BigUInt(0), UInt64(MAX_BIGUINT_IN_STACK_ARRAY)
        )

    @abimethod
    def runtime_failure_stack_byteslice_overflow(self) -> None:
        state = pcg128_init(op.bzero(32))

        state, sequence = pcg128_random(
            state, BigUInt(0), BigUInt(0), UInt64(MAX_BIGUINT_IN_STACK_ARRAY + 1)
        )
