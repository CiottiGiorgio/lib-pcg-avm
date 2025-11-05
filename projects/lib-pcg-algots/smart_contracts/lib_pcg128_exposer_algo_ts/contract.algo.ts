import { assert, Contract, Global, Txn, arc4 } from '@algorandfoundation/algorand-typescript'
import { pcg128Init, pcg128Random } from '../../lib_pcg/pcg128.algo'

export class LibPcg128ExposerAlgoTs extends Contract {
  public bounded_rand_uint128(
    seed: arc4.StaticArray<arc4.Byte, 32>,
    lower_bound: arc4.Uint128,
    upper_bound: arc4.Uint128,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint128> {
    const state = pcg128Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg128Random(state, lower_bound.asBigUint(), upper_bound.asBigUint(), length.asUint64())

    return sequence
  }

  @arc4.baremethod({ allowActions: ['UpdateApplication'] })
  public update() {
    assert(Txn.sender === Global.creatorAddress)
  }
}
