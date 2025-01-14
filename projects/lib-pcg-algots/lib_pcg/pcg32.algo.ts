import { uint64, op, bytes, Bytes, assert, Uint64 } from '@algorandfoundation/algorand-typescript';
import { DynamicArray, UintN } from '@algorandfoundation/algorand-typescript/arc4';
import { pcgFirstIncrement, pcgMultiplier } from './consts.algo';

type PCG32STATE = uint64;

export function __uint64Twos(value: uint64): uint64 {
  const [, addLow] = op.addw(~value, 1);
  return addLow;
}

function __maskToUint32(value: uint64): uint64 {
  return value & (op.shl(1, 32) - 1);
}

export function __pcg32Step(state: PCG32STATE, incr: uint64): uint64 {
  const [, mulLow] = op.mulw(state, pcgMultiplier);
  const [, addLow] = op.addw(mulLow, incr);

  return addLow;
}

export function __pcg32Output(state: PCG32STATE): uint64 {
  const xorshifted = __maskToUint32(op.shr(op.shr(state, 18) ^ state, 27));
  const rot = op.shr(state, 59);
  return op.shr(xorshifted, rot) | __maskToUint32(op.shl(xorshifted, __uint64Twos(rot) & 31));
}

export function __pcg32UnboundedRandom(state: PCG32STATE): [PCG32STATE, uint64] {
  return [__pcg32Step(state, pcgFirstIncrement), __pcg32Output(state)];
}

function __pcg32BoundedSequence(
  state: PCG32STATE,
  bitSize: uint64,
  lowerBound: uint64,
  upperBound: uint64,
  length: uint64
): [PCG32STATE, bytes] {
  let result: bytes = Bytes('');

  assert(length < op.shl(1, 16));
  result = new UintN<16>(length).bytes;

  assert(bitSize === 8 || bitSize === 16 || bitSize === 32);
  const byteSize = op.shr(bitSize, 3);
  const truncatedStartCached: uint64 = Uint64(8) - byteSize;

  let absoluteBound: uint64;

  if (lowerBound === 0 && upperBound === 0) {
    for (let i = Uint64(0); i < length; i = i + 1) {
      const [newState, n] = __pcg32UnboundedRandom(state);
      state = newState;

      result = op.concat(result, op.extract(op.itob(n), truncatedStartCached, byteSize));
    }
  } else {
    if (upperBound !== 0) {
      assert(upperBound > 1);
      assert(upperBound < op.shl(1, bitSize));
      assert(lowerBound < upperBound - 1);

      absoluteBound = upperBound - lowerBound;
    } else {
      assert(lowerBound < op.shl(1, bitSize) - 1);

      absoluteBound = op.shl(1, bitSize) - lowerBound;
    }

    const threshold: uint64 = __maskToUint32(__uint64Twos(absoluteBound)) % absoluteBound;

    for (let i = Uint64(0); i < length; i = i + 1) {
      while (true) {
        const [newState, candidate] = __pcg32UnboundedRandom(state);
        state = newState;
        if (candidate >= threshold) {
          result = op.concat(
            result,
            op.extract(op.itob((candidate % absoluteBound) + lowerBound), truncatedStartCached, byteSize)
          );
          break;
        }
      }
    }
  }

  return [state, result];
}

export function __pcg32Init(initialState: PCG32STATE, incr: uint64): PCG32STATE {
  const state = __pcg32Step(0, incr);
  const [, addLow] = op.addw(state, initialState);

  return __pcg32Step(addLow, incr);
}

export function pcg32Init(seed: bytes): PCG32STATE {
  assert(seed.length === 8);

  return __pcg32Init(op.btoi(seed), pcgFirstIncrement);
}

export function pcg16Init(seed: bytes): PCG32STATE {
  return pcg32Init(seed);
}

export function pcg8Init(seed: bytes): PCG32STATE {
  return pcg32Init(seed);
}

export function pcg32Random(
  state: PCG32STATE,
  lowerBound: uint64,
  upperBound: uint64,
  length: uint64
): [PCG32STATE, DynamicArray<UintN<32>>] {
  const result = new DynamicArray<UintN<32>>();
  const [newState, sequence] = __pcg32BoundedSequence(state, 32, lowerBound, upperBound, length);

  // This works while waiting for .fromBytes() to be implemented
  for (let i = Uint64(0); i < length; i = i + 1) {
    result.push(new UintN<32>(op.extractUint32(sequence, 2 + i * 4)));
  }

  return [newState, result.copy()];
}

export function pcg16Random(
  state: PCG32STATE,
  lowerBound: uint64,
  upperBound: uint64,
  length: uint64
): [PCG32STATE, DynamicArray<UintN<16>>] {
  const result = new DynamicArray<UintN<16>>();
  const [newState, sequence] = __pcg32BoundedSequence(state, 16, lowerBound, upperBound, length);

  // This works while waiting for .fromBytes() to be implemented
  for (let i = Uint64(0); i < length; i = i + 1) {
    result.push(new UintN<16>(op.extractUint16(sequence, 2 + i * 2)));
  }

  return [newState, result.copy()];
}

export function pcg8Random(
  state: PCG32STATE,
  lowerBound: uint64,
  upperBound: uint64,
  length: uint64
): [PCG32STATE, DynamicArray<UintN<8>>] {
  const result = new DynamicArray<UintN<8>>();
  const [newState, sequence] = __pcg32BoundedSequence(state, 8, lowerBound, upperBound, length);

  // This works while waiting for .fromBytes() to be implemented
  for (let i = Uint64(0); i < length; i = i + 1) {
    result.push(new UintN<8>(op.btoi(op.extract(sequence, 2 + i, 1))));
  }

  return [newState, result.copy()];
}
