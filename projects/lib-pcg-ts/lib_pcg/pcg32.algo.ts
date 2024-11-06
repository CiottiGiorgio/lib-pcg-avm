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

export function __pcg32Random(state: PCG32STATE): [PCG32STATE, uint64] {
  return [__pcg32Step(state, pcgFirstIncrement), __pcg32Output(state)];
}

export function __pcg32Init(initialState: PCG32STATE, incr: uint64): PCG32STATE {
  const state = __pcg32Step(0, incr);
  const addwResult = addw(state, initialState);

  return __pcg32Step(addwResult.low, incr);
}

export function pcg32Init(seed: bytes<8>): PCG32STATE {
  assert(seed.length === 8);

  return __pcg32Init(btoi(seed), pcgFirstIncrement);
}

export function pcg16Init(seed: bytes<8>): PCG32STATE {
  return pcg32Init(seed);
}

export function pcg8Init(seed: bytes<8>): PCG32STATE {
  return pcg32Init(seed);
}

export function pcg32Random(
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
      const stepResult = __pcg32Random(state);
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

    threshold = __maskToUint32(__uint64Twos(absoluteBound)) % absoluteBound;

    for (let i = 0; i < length; i = i + 1) {
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const stepResult = __pcg32Random(state);
        state = stepResult[0];
        if (stepResult[1] >= threshold) {
          result.push(((stepResult[1] % absoluteBound) + lowerBound) as uint32);
          break;
        }
      }
    }
  }

  return [state, result];
}

export function pcg16Random(
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
      const stepResult = __pcg32Random(state);
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

    threshold = __maskToUint32(__uint64Twos(absoluteBound)) % absoluteBound;

    for (let i = 0; i < length; i = i + 1) {
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const stepResult = __pcg32Random(state);
        state = stepResult[0];
        if (stepResult[1] >= threshold) {
          result.push(((stepResult[1] % absoluteBound) + lowerBound) as uint16);
          break;
        }
      }
    }
  }

  return [state, result];
}

export function pcg8Random(
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
      const stepResult = __pcg32Random(state);
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

    threshold = __maskToUint32(__uint64Twos(absoluteBound)) % absoluteBound;

    for (let i = 0; i < length; i = i + 1) {
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const stepResult = __pcg32Random(state);
        state = stepResult[0];
        if (stepResult[1] >= threshold) {
          result.push(((stepResult[1] % absoluteBound) + lowerBound) as uint8);
          break;
        }
      }
    }
  }

  return [state, result];
}
