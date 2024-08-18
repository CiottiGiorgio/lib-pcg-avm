import { LibPcg32 } from '../lib_pcg/lib-pcg32-ts.algo';

export class LibPcg32ExposerTs extends LibPcg32 {
  // eslint-disable-next-line camelcase
  bounded_rand_uint32(seed: bytes<8>, lower_bound: uint32, upper_bound: uint32, length: uint16): uint32[] {
    let state = this.pcg32Init(seed);

    // eslint-disable-next-line camelcase
    const result = this.pcg32Random(state, lower_bound as uint64, upper_bound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  // eslint-disable-next-line camelcase
  bounded_rand_uint16(seed: bytes<8>, lower_bound: uint16, upper_bound: uint16, length: uint16): uint16[] {
    let state = this.pcg32Init(seed);

    // eslint-disable-next-line camelcase
    const result = this.pcg16Random(state, lower_bound as uint64, upper_bound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  // eslint-disable-next-line camelcase
  bounded_rand_uint8(seed: bytes<8>, lower_bound: uint8, upper_bound: uint8, length: uint16): uint8[] {
    let state = this.pcg32Init(seed);

    // eslint-disable-next-line camelcase
    const result = this.pcg8Random(state, lower_bound as uint64, upper_bound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }
}
