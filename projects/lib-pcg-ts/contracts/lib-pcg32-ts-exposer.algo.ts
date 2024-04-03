import { LibPcg32Ts } from './lib-pcg32-ts.algo';

export class LibPcg32TsExposer extends LibPcg32Ts {
  // eslint-disable-next-line camelcase
  boundedRandUInt32(seed: uint64, lower_bound: uint64, upper_bound: uint64, length: uint64): uint32[] {
    const rngState = this.pcg32Init(seed);

    return castBytes<uint32[]>(this.pcg32Random(rngState, 32, lower_bound, upper_bound, length)[1]);
  }

  // eslint-disable-next-line camelcase
  boundedRandUInt16(seed: uint64, lower_bound: uint64, upper_bound: uint64, length: uint64): uint16[] {
    const rngState = this.pcg32Init(seed);

    return castBytes<uint16[]>(this.pcg32Random(rngState, 16, lower_bound, upper_bound, length)[1]);
  }

  // eslint-disable-next-line camelcase
  boundedRandUInt8(seed: uint64, lower_bound: uint64, upper_bound: uint64, length: uint64): uint8[] {
    const rngState = this.pcg32Init(seed);

    return castBytes<uint8[]>(this.pcg32Random(rngState, 8, lower_bound, upper_bound, length)[1]);
  }
}
