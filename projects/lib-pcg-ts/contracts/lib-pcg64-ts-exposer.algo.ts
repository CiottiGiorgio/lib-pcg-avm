import { LibPcg64Ts } from './lib-pcg64-ts.algo';

export class LibPcg64TsExposer extends LibPcg64Ts {
  boundedRandUInt64(seed: bytes<16>, lowerBound: uint64, upperBound: uint64, length: uint64): uint64[] {
    const rngState = this.pcg64Init([extractUint64(seed, 0), extractUint64(seed, 8)]);

    return this.pcg64Random(rngState, lowerBound, upperBound, length)[1];
  }
}
