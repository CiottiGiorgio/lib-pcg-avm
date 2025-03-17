from typing import Literal

from algopy import Global, Txn, arc4

from lib_pcg import (
    pcg8_init,
    pcg8_random,
    pcg16_init,
    pcg16_random,
    pcg32_init,
    pcg32_random,
)


class LibPcg32ExposerAlgoPy(arc4.ARC4Contract):
    @arc4.abimethod
    def bounded_rand_uint32(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt32,
        upper_bound: arc4.UInt32,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt32]:
        state = pcg32_init(seed.bytes)

        state, sequence = pcg32_random(
            state, lower_bound.native, upper_bound.native, length.native
        )

        return sequence

    @arc4.abimethod
    def bounded_rand_uint16(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt16,
        upper_bound: arc4.UInt16,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt16]:
        state = pcg16_init(seed.bytes)

        state, sequence = pcg16_random(
            state, lower_bound.native, upper_bound.native, length.native
        )

        return sequence

    @arc4.abimethod
    def bounded_rand_uint8(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt8,
        upper_bound: arc4.UInt8,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt8]:
        state = pcg8_init(seed.bytes)

        state, sequence = pcg8_random(
            state, lower_bound.native, upper_bound.native, length.native
        )

        return sequence

    @arc4.baremethod(allow_actions=["UpdateApplication"])
    def update(self) -> None:
        assert Txn.sender == Global.creator_address
