import { __pcg32Init, __pcg32Output, __pcg32Step } from './pcg32.algo';
import { pcgFirstIncrement, pcgSecondIncrement, pcgThirdIncrement, pcgFourthIncrement } from './consts.algo';

type PCG128STATE = [uint64, uint64, uint64, uint64];

function __uint128Twos(value: uint128): uint128 {
  return (
    (((~rawBytes(value) as uint256) + Uint<256>('1')) as uint128) & Uint<128>('340282366920938463463374607431768211455')
  );
}

function __pcg128Random(state: PCG128STATE): [PCG128STATE, uint128] {
  const state1 = __pcg32Step(state[0], pcgFirstIncrement);
  const state2 = __pcg32Step(state[1], pcgSecondIncrement << (state1 === 0 ? 1 : 0));
  const state3 = __pcg32Step(state[2], pcgThirdIncrement << (state2 === 0 ? 1 : 0));
  const state4 = __pcg32Step(state[3], pcgFourthIncrement << (state3 === 0 ? 1 : 0));

  return [
    [state1, state2, state3, state4],
    ((__pcg32Output(state[0]) as uint128) * Uint<128>('79228162514264337593543950336')) |
      ((__pcg32Output(state[1]) as uint128) * Uint<128>('18446744073709551616')) |
      ((__pcg32Output(state[2]) as uint128) * Uint<128>('4294967296')) |
      (__pcg32Output(state[3]) as uint128),
  ];
}

export function pcg128Init(seed: bytes<32>): PCG128STATE {
  assert(seed.length === 32);

  return [
    __pcg32Init(extractUint64(seed, 0), pcgFirstIncrement),
    __pcg32Init(extractUint64(seed, 8), pcgSecondIncrement),
    __pcg32Init(extractUint64(seed, 16), pcgThirdIncrement),
    __pcg32Init(extractUint64(seed, 24), pcgFourthIncrement),
  ];
}

export function pcg128Random(
  state: PCG128STATE,
  lowerBound: uint128,
  upperBound: uint128,
  length: uint64
): [PCG128STATE, uint128[]] {
  const result: uint128[] = [];
  let absoluteBound: uint128;
  let threshold: uint128;

  let newState = clone(state);

  if (lowerBound === 0 && upperBound === 0) {
    for (let i = 0; i < length; i = i + 1) {
      const stepResult = __pcg128Random(newState);
      newState = stepResult[0];
      result.push(stepResult[1]);
    }
  } else {
    if (upperBound !== 0) {
      assert(upperBound > 1);
      // assert(upperBound < (1 << 128));
      assert((upperBound as uint256) < Uint<256>('340282366920938463463374607431768211456'));
      assert(lowerBound < upperBound - 1);

      absoluteBound = upperBound - lowerBound;
    } else {
      // assert(lowerBound < (1 << 128) - 1);
      assert(lowerBound < Uint<128>('340282366920938463463374607431768211455'));

      // I'm not sure this next commented line would actually work like that,
      //  but it's just to explain it more clearly.
      // absoluteBound = ((1 << 128) as uint256 - (lowerBound as uint256)) as uint64;
      absoluteBound = (Uint<256>('340282366920938463463374607431768211456') - (lowerBound as uint256)) as uint128;
    }

    threshold = __uint128Twos(absoluteBound) % absoluteBound;

    for (let i = 0; i < length; i = i + 1) {
      // eslint-disable-next-line no-constant-condition
      while (true) {
        const stepResult = __pcg128Random(newState);
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
