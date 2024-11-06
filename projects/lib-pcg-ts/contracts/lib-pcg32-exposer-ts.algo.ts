import { Contract } from '@algorandfoundation/tealscript';
import { pcg16Init, pcg16Random, pcg32Init, pcg32Random, pcg8Init, pcg8Random } from '../lib_pcg/pcg32.algo';

export class LibPcg32ExposerTs extends Contract {
  // eslint-disable-next-line camelcase
  bounded_rand_uint32(seed: bytes<8>, lower_bound: uint32, upper_bound: uint32, length: uint16): uint32[] {
    let state = pcg32Init(seed);

    // eslint-disable-next-line camelcase
    const result = pcg32Random(state, lower_bound as uint64, upper_bound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  // eslint-disable-next-line camelcase
  bounded_rand_uint16(seed: bytes<8>, lower_bound: uint16, upper_bound: uint16, length: uint16): uint16[] {
    let state = pcg16Init(seed);

    // eslint-disable-next-line camelcase
    const result = pcg16Random(state, lower_bound as uint64, upper_bound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  // eslint-disable-next-line camelcase
  bounded_rand_uint8(seed: bytes<8>, lower_bound: uint8, upper_bound: uint8, length: uint16): uint8[] {
    let state = pcg8Init(seed);

    // eslint-disable-next-line camelcase
    const result = pcg8Random(state, lower_bound as uint64, upper_bound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  updateApplication() {
    assert(globals.creatorAddress === this.txn.sender);
  }
}
