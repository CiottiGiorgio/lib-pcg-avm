from typing import Literal

from algopy import Global, Txn, arc4, op

from lib_pcg.xsh_rr_double_64_32 import pcg64_init, pcg64_random


class LibPcg64ExposerAlgopy(arc4.ARC4Contract):
    @arc4.abimethod
    def bounded_rand_uint64(
        self,
        seed: arc4.StaticArray[arc4.Byte, Literal[16]],
        lower_bound: arc4.UInt64,
        upper_bound: arc4.UInt64,
        length: arc4.UInt16,
    ) -> arc4.DynamicArray[arc4.UInt64]:
        state1, state2 = pcg64_init(
            op.extract_uint64(seed.bytes, 0), op.extract_uint64(seed.bytes, 8)
        )

        return arc4.DynamicArray[arc4.UInt64].from_bytes(
            pcg64_random(
                state1, state2, lower_bound.native, upper_bound.native, length.native
            )[2]
        )

    @arc4.baremethod(allow_actions=["UpdateApplication"])
    def update(self) -> None:
        assert Txn.sender == Global.creator_address
