import { assert, BigUint, Bytes, bytes, op, uint64, Uint64, arc4, clone } from '@algorandfoundation/algorand-typescript'
import { pcgFirstIncrement, pcgSecondIncrement } from './consts.algo'
import { __pcg32Init, __pcg32Output, __pcg32Step, __uint64Twos } from './pcg32.algo'

type PCG64STATE = [uint64, uint64]

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
): [PCG64STATE, arc4.DynamicArray<arc4.Uint64>] {
  const result = new arc4.DynamicArray<arc4.Uint64>()

  let helperState = clone(state)
  let absoluteBound: uint64

  if (lowerBound === 0 && upperBound === 0) {
    let n: uint64
    for (let i = Uint64(0); i < length; i = i + 1) {
      ;[helperState, n] = __pcg64UnboundedRandom(helperState)

      result.push(new arc4.Uint64(n))
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

    let candidate: uint64
    for (let i = Uint64(0); i < length; i = i + 1) {
      while (true) {
        ;[helperState, candidate] = __pcg64UnboundedRandom(helperState)
        if (candidate >= threshold) {
          result.push(new arc4.Uint64((candidate % absoluteBound) + lowerBound))
          break
        }
      }
    }
  }

  return [state, clone(result)]
}

export function __pcg64UnboundedRandom(state: PCG64STATE): [PCG64STATE, uint64] {
  const newState1 = __pcg32Step(state[0], pcgFirstIncrement)
  const newState2 = __pcg32Step(state[1], newState1 === 0 ? op.shl(pcgSecondIncrement, 1) : pcgSecondIncrement)

  return [[newState1, newState2], op.shl(__pcg32Output(state[0]), 32) | __pcg32Output(state[1])]
}
