import { assert, biguint, BigUint, Bytes, bytes, op, uint64, Uint64 } from '@algorandfoundation/algorand-typescript'
import { pcgFirstIncrement, pcgSecondIncrement, pcgThirdIncrement, pcgFourthIncrement } from './consts.algo'
import { __pcg32Init, __pcg32Output, __pcg32Step } from './pcg32.algo'
import { DynamicArray, UintN128 } from '@algorandfoundation/algorand-typescript/arc4'

type PCG128STATE = [uint64, uint64, uint64, uint64]

export function pcg128Init(seed: bytes): PCG128STATE {
  assert(seed.length === 32)

  return [
    __pcg32Init(op.extractUint64(seed, 0), pcgFirstIncrement),
    __pcg32Init(op.extractUint64(seed, 8), pcgSecondIncrement),
    __pcg32Init(op.extractUint64(seed, 16), pcgThirdIncrement),
    __pcg32Init(op.extractUint64(seed, 24), pcgFourthIncrement),
  ]
}

export function pcg128Random(
  state: PCG128STATE,
  lowerBound: biguint,
  upperBound: biguint,
  length: uint64,
): [PCG128STATE, DynamicArray<UintN128>] {
  const result = new DynamicArray<UintN128>()

  let absoluteBound: biguint

  if (lowerBound === BigUint(0) && upperBound === BigUint(0)) {
    for (let i = Uint64(0); i < length; i = i + 1) {
      const [newState, n] = __pcg128UnboundedRandom(state)
      state = newState

      result.push(new UintN128(n))
    }
  } else {
    if (upperBound !== BigUint(0)) {
      assert(upperBound > BigUint(1))
      assert(upperBound < BigUint(2 ** 128))
      assert(lowerBound < upperBound - BigUint(1))

      absoluteBound = upperBound - lowerBound
    } else {
      assert(lowerBound < BigUint(2 ** 128 - 1))

      absoluteBound = BigUint(2 ** 128) - BigUint(lowerBound)
    }

    const threshold: biguint = __uint128Twos(absoluteBound) % absoluteBound

    for (let i = Uint64(0); i < length; i = i + 1) {
      while (true) {
        const [newState, candidate] = __pcg128UnboundedRandom(state)
        state = newState
        if (candidate >= threshold) {
          result.push(new UintN128((candidate % absoluteBound) + lowerBound))
          break
        }
      }
    }
  }

  return [state, result.copy()]
}

export function __pcg128UnboundedRandom(state: PCG128STATE): [PCG128STATE, biguint] {
  const newState1 = __pcg32Step(state[0], pcgFirstIncrement)
  const newState2 = __pcg32Step(state[1], newState1 === 0 ? op.shl(pcgSecondIncrement, 1) : pcgSecondIncrement)
  const newState3 = __pcg32Step(state[2], newState2 === 0 ? op.shl(pcgThirdIncrement, 1) : pcgThirdIncrement)
  const newState4 = __pcg32Step(state[3], newState3 === 0 ? op.shl(pcgFourthIncrement, 1) : pcgFourthIncrement)

  return [
    [newState1, newState2, newState3, newState4],
    BigUint(
      op.concat(
        op.itob(op.shl(__pcg32Output(state[0]), 32) | __pcg32Output(state[1])),
        op.itob(op.shl(__pcg32Output(state[2]), 32) | __pcg32Output(state[3])),
      ),
    ),
  ]
}

export function __uint128Twos(value: biguint): biguint {
  return (BigUint(Bytes(value).bitwiseInvert()) + BigUint(1)) & BigUint(2 ** 128 - 1)
}
