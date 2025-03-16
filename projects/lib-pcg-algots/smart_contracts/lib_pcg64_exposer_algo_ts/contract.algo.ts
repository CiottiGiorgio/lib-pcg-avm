import {assert, Contract, Global, Txn} from '@algorandfoundation/algorand-typescript'
import {
  baremethod,
  Byte,
  DynamicArray,
  StaticArray,
  UintN16,
  UintN64
} from "@algorandfoundation/algorand-typescript/arc4";
import {pcg64Init, pcg64Random} from "../../lib_pcg/pcg64.algo";

export class LibPcg64ExposerAlgoTs extends Contract {
  public bounded_rand_uint64(
    seed: StaticArray<Byte, 16>,
    lower_bound: UintN64,
    upper_bound: UintN64,
    length: UintN16
  ): DynamicArray<UintN64> {
    const state = pcg64Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg64Random(state, lower_bound.native, upper_bound.native, length.native)

    return sequence
  }

  @baremethod({ allowActions: ['UpdateApplication'] })
  public update() {
    assert(Txn.sender === Global.creatorAddress);
  }
}
