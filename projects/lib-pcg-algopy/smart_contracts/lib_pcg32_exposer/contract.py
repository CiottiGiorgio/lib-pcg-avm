from typing import Literal

from algopy import Global, Txn, UInt64, arc4

from lib_pcg.xsh_rr_64_32 import pcg32_init, pcg32_random


class LibPcg32ExposerAlgopy(arc4.ARC4Contract):
    @arc4.abimethod
    def bounded_rand_uint32(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt32,
        upper_bound: arc4.UInt32,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt32]:
        state = pcg32_init(seed.bytes)

        return arc4.DynamicArray[arc4.UInt32].from_bytes(
            pcg32_random(
                state, UInt64(32), lower_bound.native, upper_bound.native, length.native
            )[1]
        )

    @arc4.abimethod
    def bounded_rand_uint16(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt16,
        upper_bound: arc4.UInt16,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt16]:
        state = pcg32_init(seed.bytes)

        return arc4.DynamicArray[arc4.UInt16].from_bytes(
            pcg32_random(
                state, UInt64(16), lower_bound.native, upper_bound.native, length.native
            )[1]
        )

    @arc4.abimethod
    def bounded_rand_uint8(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[8]],
        lower_bound: arc4.UInt8,
        upper_bound: arc4.UInt8,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt8]:
        state = pcg32_init(seed.bytes)

        return arc4.DynamicArray[arc4.UInt8].from_bytes(
            pcg32_random(
                state, UInt64(8), lower_bound.native, upper_bound.native, length.native
            )[1]
        )

    @arc4.baremethod(allow_actions=["UpdateApplication"])
    def update(self) -> None:
        assert Txn.sender == Global.creator_address
