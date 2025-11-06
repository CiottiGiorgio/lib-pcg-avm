from typing import Literal

from algopy import Array, Global, Txn, UInt64, arc4

from lib_pcg import (
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
    ) -> Array[UInt64]:
        state = pcg32_init(seed.bytes)

        state, sequence = pcg32_random(
            state, lower_bound.as_uint64(), upper_bound.as_uint64(), length.as_uint64()
        )

        return sequence

    @arc4.baremethod(allow_actions=["UpdateApplication"])
    def update(self) -> None:
        assert Txn.sender == Global.creator_address
