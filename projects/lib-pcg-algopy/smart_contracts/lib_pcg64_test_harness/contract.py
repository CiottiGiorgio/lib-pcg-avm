from typing import Literal

from algopy import ARC4Contract, UInt64, arc4, op
from algopy.arc4 import abimethod

from lib_pcg import pcg64_init, pcg64_random
from smart_contracts.consts import (
    MAX_UINT64_IN_STACK_ARRAY,
)


class LibPCG64TestHarnessAlgoPy(ARC4Contract):
    @abimethod
    def get_pcg64_sequence_arc4_uint64_return(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[16]],
        lower_bound: arc4.UInt64,
        upper_bound: arc4.UInt64,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt64]:
        state = pcg64_init(seed.bytes)

        state, sequence = pcg64_random(
            state, lower_bound.as_uint64(), upper_bound.as_uint64(), length.as_uint64()
        )

        return sequence

    @abimethod
    def runtime_asserts_pcg64_stack_array(self) -> None:
        state = pcg64_init(op.bzero(16))

        # Can produce a maximal length stack-based array of uint64s.
        state, sequence = pcg64_random(
            state, UInt64(0), UInt64(0), UInt64(MAX_UINT64_IN_STACK_ARRAY)
        )

    @abimethod
    def runtime_failure_stack_byteslice_overflow(self) -> None:
        state = pcg64_init(op.bzero(16))

        state, sequence = pcg64_random(
            state, UInt64(0), UInt64(0), UInt64(MAX_UINT64_IN_STACK_ARRAY + 1)
        )
