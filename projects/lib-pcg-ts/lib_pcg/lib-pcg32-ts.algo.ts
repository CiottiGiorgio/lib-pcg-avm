import { Contract } from '@algorandfoundation/tealscript';
import { pcgFirstIncrement, pcgMultiplier } from './consts.algo';

type PCG32STATE = uint64;

/* eslint-disable no-underscore-dangle, no-loss-of-precision, no-param-reassign */
export class LibPcg32 extends Contract {
  protected __uint64Twos(value: uint64): uint64 {
    const addwResult = addw(~value, 1);
    return addwResult.low;
  }

  protected __maskToUint32(value: uint64): uint64 {
    // return value & ((1 << 32) - 1);
    return value & 4294967295;
  }

  protected __pcg32Step(state: PCG32STATE, incr: uint64): uint64 {
    const mulwResult = mulw(state, pcgMultiplier);
    const addwResult = addw(mulwResult.low, incr);

    return addwResult.low;
  }

  protected __pcg32Rotation(value: uint64, rot: uint64): uint64 {
    return (value >> rot) | this.__maskToUint32(value << (this.__uint64Twos(rot) & 31));
  }

  protected __pcg32Output(state: PCG32STATE): uint64 {
    return this.__pcg32Rotation(this.__maskToUint32(((state >> 18) ^ state) >> 27), state >> 59);
  }

  protected __pcg32Random(state: PCG32STATE): [PCG32STATE, uint64] {
    return [this.__pcg32Step(state, pcgFirstIncrement), this.__pcg32Output(state)];
  }

  protected __pcg32Init(initialState: PCG32STATE, incr: uint64): PCG32STATE {
    const state = this.__pcg32Step(0, incr);
    const addwResult = addw(state, initialState);

    return this.__pcg32Step(addwResult.low, incr);
  }

  protected pcg32Init(seed: bytes<8>): PCG32STATE {
    assert(seed.length === 8);

    return this.__pcg32Init(btoi(seed), pcgFirstIncrement);
  }

  protected pcg16Init(seed: bytes<8>): PCG32STATE {
    return this.pcg32Init(seed);
  }

  protected pcg8Init(seed: bytes<8>): PCG32STATE {
    return this.pcg32Init(seed);
  }

  protected pcg32Random(
    state: PCG32STATE,
    lowerBound: uint64,
    upperBound: uint64,
    length: uint64
  ): [PCG32STATE, uint32[]] {
    const result: uint32[] = [];
    let absoluteBound: uint64;
    let threshold: uint64;

    if (lowerBound === 0 && upperBound === 0) {
      for (let i = 0; i < length; i = i + 1) {
        const stepResult = this.__pcg32Random(state);
        state = stepResult[0];
        result.push(stepResult[1] as uint32);
      }
    } else {
      if (upperBound !== 0) {
        assert(upperBound > 1);
        assert(upperBound < 1 << 32);
        assert(lowerBound < upperBound - 1);

        absoluteBound = upperBound - lowerBound;
      } else {
        assert(lowerBound < (1 << 32) - 1);

        absoluteBound = (1 << 32) - lowerBound;
      }

      threshold = this.__maskToUint32(this.__uint64Twos(absoluteBound)) % absoluteBound;

      for (let i = 0; i < length; i = i + 1) {
        let stepResult: [PCG32STATE, uint64];
        // eslint-disable-next-line no-constant-condition
        while (true) {
          stepResult = this.__pcg32Random(state);
          state = stepResult[0];
          if (stepResult[1] >= threshold) {
            break;
          }
        }

        result.push(((stepResult[1] % absoluteBound) + lowerBound) as uint32);
      }
    }

    return [state, result];
  }

  protected pcg16Random(
    state: PCG32STATE,
    lowerBound: uint64,
    upperBound: uint64,
    length: uint64
  ): [PCG32STATE, uint16[]] {
    const result: uint16[] = [];
    let absoluteBound: uint64;
    let threshold: uint64;

    if (lowerBound === 0 && upperBound === 0) {
      for (let i = 0; i < length; i = i + 1) {
        const stepResult = this.__pcg32Random(state);
        state = stepResult[0];
        result.push(extractUint16(itob(stepResult[1]), 6) as uint16);
      }
    } else {
      if (upperBound !== 0) {
        assert(upperBound > 1);
        assert(upperBound < 1 << 16);
        assert(lowerBound < upperBound - 1);

        absoluteBound = upperBound - lowerBound;
      } else {
        assert(lowerBound < (1 << 16) - 1);

        absoluteBound = (1 << 16) - lowerBound;
      }

      threshold = this.__maskToUint32(this.__uint64Twos(absoluteBound)) % absoluteBound;

      for (let i = 0; i < length; i = i + 1) {
        let stepResult: [PCG32STATE, uint64];
        // eslint-disable-next-line no-constant-condition
        while (true) {
          stepResult = this.__pcg32Random(state);
          state = stepResult[0];
          if (stepResult[1] >= threshold) {
            break;
          }
        }

        result.push(((stepResult[1] % absoluteBound) + lowerBound) as uint16);
      }
    }

    return [state, result];
  }

  protected pcg8Random(
    state: PCG32STATE,
    lowerBound: uint64,
    upperBound: uint64,
    length: uint64
  ): [PCG32STATE, uint8[]] {
    const result: uint8[] = [];
    let absoluteBound: uint64;
    let threshold: uint64;

    if (lowerBound === 0 && upperBound === 0) {
      for (let i = 0; i < length; i = i + 1) {
        const stepResult = this.__pcg32Random(state);
        state = stepResult[0];
        result.push(btoi(extract3(itob(stepResult[1]), 7, 1)) as uint8);
      }
    } else {
      if (upperBound !== 0) {
        assert(upperBound > 1);
        assert(upperBound < 1 << 8);
        assert(lowerBound < upperBound - 1);

        absoluteBound = upperBound - lowerBound;
      } else {
        assert(lowerBound < (1 << 8) - 1);

        absoluteBound = (1 << 8) - lowerBound;
      }

      threshold = this.__maskToUint32(this.__uint64Twos(absoluteBound)) % absoluteBound;

      for (let i = 0; i < length; i = i + 1) {
        let stepResult: [PCG32STATE, uint64];
        // eslint-disable-next-line no-constant-condition
        while (true) {
          stepResult = this.__pcg32Random(state);
          state = stepResult[0];
          if (stepResult[1] >= threshold) {
            break;
          }
        }

        result.push(((stepResult[1] % absoluteBound) + lowerBound) as uint8);
      }
    }

    return [state, result];
  }
}
