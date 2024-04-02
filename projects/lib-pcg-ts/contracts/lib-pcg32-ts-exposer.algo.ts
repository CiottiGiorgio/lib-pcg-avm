import { LibPcg32Ts } from './lib-pcg32-ts.algo';

export class LibPcg32TsExposer extends LibPcg32Ts {
  boundedRandUInt32(seed: uint64, lowerBound: uint64, upperBound: uint64, length: uint64): uint32[] {
    const rngState = this.pcg32Init(seed);

    return castBytes<uint32[]>(this.pcg32Random(rngState, 32, lowerBound, upperBound, length)[1]);
  }

  boundedRandUInt16(seed: uint64, lowerBound: uint64, upperBound: uint64, length: uint64): uint16[] {
    const rngState = this.pcg32Init(seed);

    return castBytes<uint16[]>(this.pcg32Random(rngState, 16, lowerBound, upperBound, length)[1]);
  }

  boundedRandUInt8(seed: uint64, lowerBound: uint64, upperBound: uint64, length: uint64): uint8[] {
    const rngState = this.pcg32Init(seed);

    return castBytes<uint8[]>(this.pcg32Random(rngState, 8, lowerBound, upperBound, length)[1]);
  }
}
