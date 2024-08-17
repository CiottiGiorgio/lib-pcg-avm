from typing import Literal

from algopy import Global, Txn, arc4

from lib_pcg import pcg128_init, pcg128_random


class LibPcg128ExposerAlgopy(arc4.ARC4Contract):
    @arc4.abimethod
    def bounded_rand_uint128(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[32]],
        lower_bound: arc4.UInt128,
        upper_bound: arc4.UInt128,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt128]:
        state = pcg128_init(seed.bytes)

        state, sequence = pcg128_random(
            state, lower_bound.native, upper_bound.native, length.native
        )

        return sequence

    @arc4.baremethod(allow_actions=["UpdateApplication"])
    def update(self) -> None:
        assert Txn.sender == Global.creator_address
