from typing import Literal

from algopy import Global, Txn, arc4

from lib_pcg import pcg64_init, pcg64_random


class LibPcg64ExposerAlgoPy(arc4.ARC4Contract):
    @arc4.abimethod
    def bounded_rand_uint64(
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

    @arc4.baremethod(allow_actions=["UpdateApplication"])
    def update(self) -> None:
        assert Txn.sender == Global.creator_address
