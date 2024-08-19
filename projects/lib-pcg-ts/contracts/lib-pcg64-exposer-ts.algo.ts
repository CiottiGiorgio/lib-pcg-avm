import { LibPcg64 } from '../lib_pcg/pcg64.algo';

export class LibPcg64ExposerTs extends LibPcg64 {
  // eslint-disable-next-line camelcase
  bounded_rand_uint64(seed: bytes<16>, lower_bound: uint64, upper_bound: uint64, length: uint16): uint64[] {
    let state = this.pcg64Init(seed);

    const result = this.pcg64Random(state, lower_bound, upper_bound, length as uint64);
    state = result[0];

    return result[1];
  }
}
