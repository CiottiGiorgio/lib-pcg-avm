import { assert, Contract, Global, Txn } from '@algorandfoundation/algorand-typescript'
import {
  baremethod,
  Byte,
  DynamicArray,
  StaticArray,
  UintN128,
  UintN16,
} from '@algorandfoundation/algorand-typescript/arc4'
import { pcg128Init, pcg128Random } from '../../lib_pcg'

export class LibPcg128ExposerAlgoTs extends Contract {
  public bounded_rand_uint128(
    seed: StaticArray<Byte, 32>,
    lower_bound: UintN128,
    upper_bound: UintN128,
    length: UintN16,
  ): DynamicArray<UintN128> {
    const state = pcg128Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg128Random(state, lower_bound.native, upper_bound.native, length.native)

    return sequence
  }

  @baremethod({ allowActions: ['UpdateApplication'] })
  public update() {
    assert(Txn.sender === Global.creatorAddress)
  }
}
