import { LibPcg64Ts } from './lib-pcg64-ts.algo';

export class LibPcg64TsExposer extends LibPcg64Ts {
  // eslint-disable-next-line camelcase
  bounded_rand_uint64(seed: bytes<16>, lower_bound: uint64, upper_bound: uint64, length: uint64): uint64[] {
    const rngState = this.pcg64Init([extractUint64(seed, 0), extractUint64(seed, 8)]);

    return this.pcg64Random(rngState, lower_bound, upper_bound, length)[1];
  }
}
