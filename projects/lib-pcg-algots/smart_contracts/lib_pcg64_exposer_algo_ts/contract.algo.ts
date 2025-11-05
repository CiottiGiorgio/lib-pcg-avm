import { assert, Contract, Global, Txn, arc4 } from '@algorandfoundation/algorand-typescript'
import { pcg64Init, pcg64Random } from '../../lib_pcg/pcg64.algo'

export class LibPcg64ExposerAlgoTs extends Contract {
  public bounded_rand_uint64(
    seed: arc4.StaticArray<arc4.Byte, 16>,
    lower_bound: arc4.Uint64,
    upper_bound: arc4.Uint64,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint64> {
    const state = pcg64Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg64Random(state, lower_bound.asUint64(), upper_bound.asUint64(), length.asUint64())

    return sequence
  }

  @arc4.baremethod({ allowActions: ['UpdateApplication'] })
  public update() {
    assert(Txn.sender === Global.creatorAddress)
  }
}
