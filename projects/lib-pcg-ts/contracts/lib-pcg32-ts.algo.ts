import { Contract } from '@algorandfoundation/tealscript';

/* eslint-disable no-underscore-dangle, no-loss-of-precision, no-param-reassign */
export class LibPcg32Ts extends Contract {
  protected __twosComplement(value: uint64): uint64 {
    const addwResult = addw(~value, 1);
    return addwResult.low;
  }

  protected __maskToUint32(value: uint64): uint64 {
    return value & 4294967295;
  }

  protected __pcg32Step(state: uint64, incr: uint64): uint64 {
    const mulwResult = mulw(state, 6364136223846793005);
    const addwResult = addw(mulwResult.low, incr);

    return addwResult.low;
  }

  protected __pcg32Rotation(value: uint64, rot: uint64): uint64 {
    return (value >> rot) | this.__maskToUint32(value << (this.__twosComplement(rot) & 31));
  }

  protected __pcg32Output(state: uint64): uint64 {
    return this.__pcg32Rotation(this.__maskToUint32(((state >> 18) ^ state) >> 27), state >> 59);
  }

  protected __pcg32Random(state: uint64): [uint64, uint64] {
    return [this.__pcg32Step(state, 1442695040888963407), this.__pcg32Output(state)];
  }

  protected __pcg32Init(initialState: uint64, incr: uint64): uint64 {
    const state = this.__pcg32Step(0, incr);
    const addwResult = addw(state, initialState);

    return this.__pcg32Step(addwResult.low, incr);
  }

  protected pcg32Init(initialState: uint64): uint64 {
    return this.__pcg32Init(initialState, 1442695040888963407);
  }

  protected pcg32Random(
    state: uint64,
    bitSize: uint64,
    lowerBound: uint64,
    upperBound: uint64,
    length: uint64
  ): [uint64, bytes] {
    let result: bytes = '';
    let absoluteBound: uint64;
    let threshold: uint64;

    assert(length < 65536);

    assert(bitSize === 8 || bitSize === 16 || bitSize === 32);
    const byteSize = bitSize >> 3;
    const truncateStartCached = 8 - byteSize;

    if (lowerBound === 0 && upperBound === 0) {
      for (let i = 0; i < length; i = i + 1) {
        const prn = this.__pcg32Random(state);
        state = prn[0];
        result += extract3(itob(prn[1]), truncateStartCached, byteSize);
      }
    } else {
      if (upperBound !== 0) {
        assert(upperBound > 1);
        assert(upperBound < 1 << bitSize);

        assert(lowerBound < upperBound - 1);

        absoluteBound = upperBound - lowerBound;
      } else {
        assert(lowerBound < (1 << bitSize) - 1);

        absoluteBound = (1 << bitSize) - lowerBound;
      }

      threshold = this.__twosComplement(absoluteBound) % absoluteBound;

      for (let i = 0; i < length; i = i + 1) {
        let prn: [uint64, uint64];
        // eslint-disable-next-line no-constant-condition
        while (true) {
          prn = this.__pcg32Random(state);
          state = prn[0];
          if (prn[1] >= threshold) {
            break;
          }
        }

        result += extract3(itob((prn[1] % absoluteBound) + lowerBound), truncateStartCached, byteSize);
      }
    }

    return [state, result];
  }
}
