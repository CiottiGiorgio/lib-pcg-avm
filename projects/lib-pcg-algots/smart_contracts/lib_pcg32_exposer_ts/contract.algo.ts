import { Contract, assert, Global, Txn } from '@algorandfoundation/algorand-typescript'
import { StaticArray, DynamicArray, Byte, UintN, baremethod } from '@algorandfoundation/algorand-typescript/arc4'
import { pcg16Init, pcg16Random, pcg32Init, pcg32Random, pcg8Init, pcg8Random } from '../../lib_pcg/pcg32.algo'

export class LibPcg32ExposerTs extends Contract {
  public bounded_rand_uint32(
    seed: StaticArray<Byte, 8>,
    lower_bound: UintN<32>,
    upper_bound: UintN<32>,
    length: UintN<16>
  ): DynamicArray<UintN<32>> {
    const state = pcg32Init(seed.bytes);

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg32Random(state, lower_bound.native, upper_bound.native, length.native);

    return sequence;
  }

  public bounded_rand_uint16(
    seed: StaticArray<Byte, 8>,
    lower_bound: UintN<16>,
    upper_bound: UintN<16>,
    length: UintN<16>
  ): DynamicArray<UintN<16>> {
    const state = pcg16Init(seed.bytes);

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg16Random(state, lower_bound.native, upper_bound.native, length.native);

    return sequence;
  }

  public bounded_rand_uint8(
    seed: StaticArray<Byte, 8>,
    lower_bound: UintN<8>,
    upper_bound: UintN<8>,
    length: UintN<16>
  ): DynamicArray<UintN<8>> {
    const state = pcg8Init(seed.bytes);

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg8Random(state, lower_bound.native, upper_bound.native, length.native);

    return sequence;
  }

  @baremethod({ allowActions: ['UpdateApplication'] })
  public update() {
    assert(Txn.sender === Global.creatorAddress);
  }
}
