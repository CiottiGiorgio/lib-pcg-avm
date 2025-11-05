import { Contract, assert, Global, Txn, arc4 } from '@algorandfoundation/algorand-typescript'
import { pcg16Init, pcg16Random, pcg32Init, pcg32Random, pcg8Init, pcg8Random } from '../../lib_pcg/pcg32.algo'

export class LibPcg32ExposerAlgoTs extends Contract {
  public bounded_rand_uint32(
    seed: arc4.StaticArray<arc4.Byte, 8>,
    lower_bound: arc4.Uint32,
    upper_bound: arc4.Uint32,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint32> {
    const state = pcg32Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg32Random(state, lower_bound.asUint64(), upper_bound.asUint64(), length.asUint64())

    return sequence
  }

  public bounded_rand_uint16(
    seed: arc4.StaticArray<arc4.Byte, 8>,
    lower_bound: arc4.Uint16,
    upper_bound: arc4.Uint16,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint16> {
    const state = pcg16Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg16Random(state, lower_bound.asUint64(), upper_bound.asUint64(), length.asUint64())

    return sequence
  }

  public bounded_rand_uint8(
    seed: arc4.StaticArray<arc4.Byte, 8>,
    lower_bound: arc4.Uint8,
    upper_bound: arc4.Uint8,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint8> {
    const state = pcg8Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg8Random(state, lower_bound.asUint64(), upper_bound.asUint64(), length.asUint64())

    return sequence
  }

  @arc4.baremethod({ allowActions: ['UpdateApplication'] })
  public update() {
    assert(Txn.sender === Global.creatorAddress)
  }
}
