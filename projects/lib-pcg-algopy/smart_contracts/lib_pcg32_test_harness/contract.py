from typing import Literal

from algopy import ARC4Contract, UInt64, arc4, op
from algopy.arc4 import abimethod

from lib_pcg import (
    pcg8_init,
    pcg8_random,
    pcg16_init,
    pcg16_random,
    pcg32_init,
    pcg32_random,
)
from smart_contracts.consts import (
    MAX_UINT8_IN_STACK_ARRAY,
    MAX_UINT16_IN_STACK_ARRAY,
    MAX_UINT32_IN_STACK_ARRAY,
)


class LibPCG32TestHarnessAlgoPy(ARC4Contract):
    @abimethod
    def get_pcg32_sequence_arc4_uint32_return(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt32,
        upper_bound: arc4.UInt32,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt32]:
        state = pcg32_init(seed.bytes)

        state, sequence = pcg32_random(
            state, lower_bound.as_uint64(), upper_bound.as_uint64(), length.as_uint64()
        )

        return sequence

    @abimethod
    def get_pcg32_sequence_arc4_uint16_return(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt16,
        upper_bound: arc4.UInt16,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt16]:
        state = pcg16_init(seed.bytes)

        state, sequence = pcg16_random(
            state, lower_bound.as_uint64(), upper_bound.as_uint64(), length.as_uint64()
        )

        return sequence

    @abimethod
    def get_pcg32_sequence_arc4_uint8_return(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt8,
        upper_bound: arc4.UInt8,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt8]:
        state = pcg8_init(seed.bytes)

        state, sequence = pcg8_random(
            state, lower_bound.as_uint64(), upper_bound.as_uint64(), length.as_uint64()
        )

        return sequence

    @abimethod
    def runtime_asserts_pcg32_stack_array(self) -> None:
        state = pcg32_init(op.bzero(8))

        # Can produce a maximal length stack-based array of uint32s.
        state, sequence = pcg32_random(
            state, UInt64(0), UInt64(0), UInt64(MAX_UINT32_IN_STACK_ARRAY)
        )

    @abimethod
    def runtime_asserts_pcg16_stack_array(self) -> None:
        state = pcg16_init(op.bzero(8))

        # Can produce a maximal length stack-based array of uint16s.
        state, sequence = pcg16_random(
            state, UInt64(0), UInt64(0), UInt64(MAX_UINT16_IN_STACK_ARRAY)
        )

    @abimethod
    def runtime_asserts_pcg8_stack_array(self) -> None:
        state = pcg8_init(op.bzero(8))

        # Can produce a maximal length stack-based array of uint8s.
        state, sequence = pcg8_random(
            state, UInt64(0), UInt64(0), UInt64(MAX_UINT8_IN_STACK_ARRAY)
        )

    @abimethod
    def runtime_failure_stack_byteslice_overflow(self) -> None:
        state = pcg32_init(op.bzero(8))

        state, sequence = pcg32_random(
            state, UInt64(0), UInt64(0), UInt64(MAX_UINT32_IN_STACK_ARRAY + 1)
        )
