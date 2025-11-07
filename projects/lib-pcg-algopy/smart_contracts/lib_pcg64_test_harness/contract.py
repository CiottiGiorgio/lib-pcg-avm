from typing import Literal

from algopy import ARC4Contract, Array, UInt64, arc4
from algopy.arc4 import abimethod

from lib_pcg import pcg64_init, pcg64_random
from lib_pcg.pcg64 import pcg64_random_arc4_uint64


class LibPCG64TestHarnessAlgoPy(ARC4Contract):
    @abimethod
    def get_pcg64_sequence_native_uint64_return(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[16]],
        lower_bound: arc4.UInt64,
        upper_bound: arc4.UInt64,
        length: arc4.UInt16,
    ) -> Array[UInt64]:
        state = pcg64_init(seed.bytes)

        state, sequence = pcg64_random(
            state,
            lower_bound.as_uint64(),
            upper_bound.as_uint64(),
            length.as_uint64(),
        )

        return sequence

    @abimethod
    def get_pcg64_sequence_arc4_uint64_return(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[16]],
        lower_bound: arc4.UInt64,
        upper_bound: arc4.UInt64,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt64]:
        state = pcg64_init(seed.bytes)

        state, sequence = pcg64_random_arc4_uint64(
            state, lower_bound.as_uint64(), upper_bound.as_uint64(), length.as_uint64()
        )

        return sequence
