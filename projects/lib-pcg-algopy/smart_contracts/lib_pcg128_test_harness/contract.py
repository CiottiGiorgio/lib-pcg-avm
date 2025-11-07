from typing import Literal

from algopy import ARC4Contract, Array, BigUInt, arc4
from algopy.arc4 import abimethod

from lib_pcg import pcg128_init, pcg128_random
from lib_pcg.pcg128 import pcg128_random_arc4_uint128


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
