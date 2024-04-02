import { LibPcg32Ts } from './lib-pcg32-ts.algo';

/* eslint-disable no-underscore-dangle, no-loss-of-precision */
export class LibPcg64Ts extends LibPcg32Ts {
  protected __pcg64Random(state: [uint64, uint64]): [[uint64, uint64], uint64] {
    const prn1 = this.__pcg32Random(state[0]);
    let prn2: uint64;
    if (prn1[0] === 0) {
      prn2 = this.__pcg32Step(state[1], 1442695040888963409 << 1);
    } else {
      prn2 = this.__pcg32Step(state[1], 1442695040888963409);
    }

    return [[prn1[0], prn2], (prn1[1] << 32) | this.__pcg32Output(state[1])];
  }

  protected pcg64Init(state: [uint64, uint64]): [uint64, uint64] {
    return [this.__pcg32Init(state[0], 1442695040888963407), this.__pcg32Init(state[1], 1442695040888963409)];
  }

  protected pcg64Random(
    state: [uint64, uint64],
    lowerBound: uint64,
    upperBound: uint64,
    length: uint64
  ): [[uint64, uint64], uint64[]] {
    const result: uint64[] = [];
    let absoluteBound: uint64;
    let threshold: uint64;

    assert(length < 65536);

    let newState: [uint64, uint64];
    let n: uint64;
    newState = state;

    if (lowerBound === 0 && upperBound === 0) {
      for (let i = 0; i < length; i = i + 1) {
        const temp = this.__pcg64Random(newState);
        newState = temp[0];
        n = temp[1];
        result.push(n);
      }
    } else {
      if (upperBound !== 0) {
        assert(upperBound > 1);
        assert(lowerBound < upperBound - 1);

        absoluteBound = upperBound - lowerBound;
      } else {
        assert(lowerBound < 18446744073709551615);

        absoluteBound = ((18446744073709551616 as uint128) - (lowerBound as uint128)) as uint64;
      }

      threshold = this.__twosComplement(absoluteBound) % absoluteBound;

      for (let i = 0; i < length; i = i + 1) {
        // eslint-disable-next-line no-constant-condition
        while (true) {
          const temp = this.__pcg64Random(newState);
          newState = temp[0];
          n = temp[1];
          if (n >= threshold) {
            break;
          }
        }
        result.push(n);
      }
    }

    return [newState, result];
  }
}
