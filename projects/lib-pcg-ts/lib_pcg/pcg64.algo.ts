import { __pcg32Init, __pcg32Output, __pcg32UnboundedRandom, __pcg32Step, __uint64Twos } from './pcg32.algo';
import { pcgFirstIncrement, pcgSecondIncrement } from './consts.algo';

type PCG64STATE = [uint64, uint64];

function __pcg64Random(state: PCG64STATE): [PCG64STATE, uint64] {
  const highResult = __pcg32UnboundedRandom(state[0]);

  const lowState = __pcg32Step(state[1], pcgSecondIncrement << (highResult[0] === 0 ? 1 : 0));

  return [[highResult[0], lowState], (highResult[1] << 32) | __pcg32Output(state[1])];
}

export function pcg64Init(seed: bytes<16>): PCG64STATE {
  assert(seed.length === 16);

  return [
    __pcg32Init(extractUint64(seed, 0), pcgFirstIncrement),
    __pcg32Init(extractUint64(seed, 8), pcgSecondIncrement),
  ];
}

export function pcg64Random(
  state: PCG64STATE,
  lowerBound: uint64,
  upperBound: uint64,
  length: uint64
): [PCG64STATE, uint64[]] {
  const result: uint64[] = [];
  let absoluteBound: uint64;
  let threshold: uint64;

  let newState = clone(state);

  if (lowerBound === 0 && upperBound === 0) {
    for (let i = 0; i < length; i = i + 1) {
      const stepResult = __pcg64Random(newState);
      newState = stepResult[0];
      result.push(stepResult[1]);
    }
  } else {
    if (upperBound !== 0) {
      assert(upperBound > 1);
      assert(lowerBound < upperBound - 1);

      absoluteBound = upperBound - lowerBound;
    } else {
      // assert(lowerBound < (1 << 64) - 1);
      assert(lowerBound < Uint<64>('18446744073709551615'));

      // I'm not sure this next commented line would actually work like that,
      //  but it's just to explain it more clearly.
      // absoluteBound = ((1 << 64) as uint128 - (lowerBound as uint128)) as uint64;
      absoluteBound = (Uint<128>('18446744073709551616') - (lowerBound as uint128)) as uint64;
    }

    threshold = __uint64Twos(absoluteBound) % absoluteBound;

    for (let i = 0; i < length; i = i + 1) {
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const stepResult = __pcg64Random(newState);
        newState = stepResult[0];
        if (stepResult[1] >= threshold) {
          result.push((stepResult[1] % absoluteBound) + lowerBound);
          break;
        }
      }
    }
  }

  return [newState, result];
}
