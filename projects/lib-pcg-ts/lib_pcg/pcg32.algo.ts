import { pcgFirstIncrement, pcgMultiplier } from './consts.algo';

type PCG32STATE = uint64;

export function __uint64Twos(value: uint64): uint64 {
  const addwResult = addw(~value, 1);
  return addwResult.low;
}

function __maskToUint32(value: uint64): uint64 {
  // return value & ((1 << 32) - 1);
  return value & 4294967295;
}

export function __pcg32Step(state: PCG32STATE, incr: uint64): uint64 {
  const mulwResult = mulw(state, pcgMultiplier);
  const addwResult = addw(mulwResult.low, incr);

  return addwResult.low;
}

export function __pcg32Output(state: PCG32STATE): uint64 {
  const xorshifted = __maskToUint32(((state >> 18) ^ state) >> 27);
  const rot = state >> 59;
  return (xorshifted >> rot) | __maskToUint32(xorshifted << (__uint64Twos(rot) & 31));
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
  let result: bytes = '';

  assert(length < 2 ** 16);
  // when this bytearray is cast to the actual type, the length will be prefixed by castBytes.
  // result += extract3(itob(length), 6, 2);

  assert(bitSize === 8 || bitSize === 16 || bitSize === 32);
  const byteSize = bitSize >> 3;
  const truncatedStartCached = 8 - byteSize;

  let absoluteBound: uint64;

  if (lowerBound === 0 && upperBound === 0) {
    for (let i = 0; i < length; i = i + 1) {
      const stepResult = __pcg32UnboundedRandom(state);
      state = stepResult[0];

      result += extract3(itob(stepResult[1]), truncatedStartCached, byteSize);
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

    const threshold = __maskToUint32(__uint64Twos(absoluteBound)) % absoluteBound;

    for (let i = 0; i < length; i = i + 1) {
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const stepResult = __pcg32UnboundedRandom(state);
        state = stepResult[0];
        if (stepResult[1] >= threshold) {
          result += extract3(itob((stepResult[1] % absoluteBound) + lowerBound), truncatedStartCached, byteSize);
          break;
        }
      }
    }
  }

  return [state, result];
}

export function __pcg32Init(initialState: PCG32STATE, incr: uint64): PCG32STATE {
  const state = __pcg32Step(0, incr);
  const addwResult = addw(state, initialState);

  return __pcg32Step(addwResult.low, incr);
}

export function pcg32Init(seed: bytes): PCG32STATE {
  assert(seed.length === 8);

  return __pcg32Init(btoi(seed), pcgFirstIncrement);
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
): [PCG32STATE, uint32[]] {
  const result = __pcg32BoundedSequence(state, 32, lowerBound, upperBound, length);
  return [result[0], castBytes<uint32[]>(result[1])];
}

export function pcg16Random(
  state: PCG32STATE,
  lowerBound: uint64,
  upperBound: uint64,
  length: uint64
): [PCG32STATE, uint16[]] {
  const result = __pcg32BoundedSequence(state, 16, lowerBound, upperBound, length);
  return [result[0], castBytes<uint16[]>(result[1])];
}

export function pcg8Random(
  state: PCG32STATE,
  lowerBound: uint64,
  upperBound: uint64,
  length: uint64
): [PCG32STATE, uint8[]] {
  const result = __pcg32BoundedSequence(state, 8, lowerBound, upperBound, length);
  return [result[0], castBytes<uint8[]>(result[1])];
}
