import { assert, BigUint, Bytes, bytes, op, uint64, Uint64 } from '@algorandfoundation/algorand-typescript'
import { pcgFirstIncrement, pcgSecondIncrement } from './consts.algo'
import { __pcg32Init, __pcg32Output, __pcg32Step, __uint64Twos } from './pcg32.algo'
import { DynamicArray, UintN64 } from '@algorandfoundation/algorand-typescript/arc4'

type PCG64STATE = [uint64, uint64]

export function __pcg64UnboundedRandom(state: PCG64STATE): [PCG64STATE, uint64] {
  const newState1 = __pcg32Step(state[0], pcgFirstIncrement)
  const newState2 = __pcg32Step(state[1], newState1 === 0 ? op.shl(pcgSecondIncrement, 1) : pcgSecondIncrement)

  return [[newState1, newState2], op.shl(__pcg32Output(state[0]), 32) | __pcg32Output(state[1])]
}

export function pcg64Init(seed: bytes): PCG64STATE {
  assert(seed.length === 16)

  return [
    __pcg32Init(op.extractUint64(seed, 0), pcgFirstIncrement),
    __pcg32Init(op.extractUint64(seed, 8), pcgSecondIncrement),
  ]
}

export function pcg64Random(
  state: PCG64STATE,
  lowerBound: uint64,
  upperBound: uint64,
  length: uint64,
): [PCG64STATE, DynamicArray<UintN64>] {
  const result = new DynamicArray<UintN64>()

  let absoluteBound: uint64

  if (lowerBound === 0 && upperBound === 0) {
    for (let i = Uint64(0); i < length; i = i + 1) {
      const [newState, n] = __pcg64UnboundedRandom(state)
      state = newState

      result.push(new UintN64(n))
    }
  } else {
    if (upperBound !== 0) {
      assert(upperBound > 1)
      assert(lowerBound < upperBound - 1)

      absoluteBound = upperBound - lowerBound
    } else {
      assert(lowerBound < 2 ** 64 - 1)

      absoluteBound = op.btoi(Bytes(BigUint(2 ** 64) - BigUint(lowerBound)))
    }

    const threshold: uint64 = __uint64Twos(absoluteBound) % absoluteBound

    for (let i = Uint64(0); i < length; i = i + 1) {
      while (true) {
        const [newState, candidate] = __pcg64UnboundedRandom(state)
        state = newState
        if (candidate >= threshold) {
          result.push(new UintN64((candidate % absoluteBound) + lowerBound))
          break
        }
      }
    }
  }

  return [state, result.copy()]
}
