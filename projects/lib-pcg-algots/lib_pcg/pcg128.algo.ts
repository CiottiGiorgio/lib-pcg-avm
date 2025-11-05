import {
  assert,
  biguint,
  BigUint,
  Bytes,
  bytes,
  op,
  uint64,
  Uint64,
  arc4,
  clone,
} from '@algorandfoundation/algorand-typescript'
import { pcgFirstIncrement, pcgSecondIncrement, pcgThirdIncrement, pcgFourthIncrement } from './consts.algo'
import { __pcg32Init, __pcg32Output, __pcg32Step } from './pcg32.algo'

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
): [PCG128STATE, arc4.DynamicArray<arc4.Uint128>] {
  const result = new arc4.DynamicArray<arc4.Uint128>()

  let helperState = clone(state)
  let absoluteBound: biguint

  if (lowerBound === BigUint(0) && upperBound === BigUint(0)) {
    let n: biguint
    for (let i = Uint64(0); i < length; i = i + 1) {
      ;[helperState, n] = __pcg128UnboundedRandom(helperState)

      // The current version of puya-ts has a bug where it checks that a biguint can fit into an arc4.Uint
      //  by checking its byteslice length.
      // This is erroneous because the biguint could be padded with zeros.
      // A correct approach would be using b< or bitlen.
      // As it happens, the pinned release of puya-ts pads biguints with zeros to always have them be long 64 bytes.
      // This means that creating an arc4.Uint128 from a biguint pretty much always fails the runtime check.
      //
      // The solution is to do an unsafe casting and leveraging the knowledge that tha return from __pcg128UnboundedRandom
      // will be a byteslice of exactly 64 bytes.
      //
      // Additionally, this also saves the opcodes and bytecode spent for arc4 validation.
      result.push(
        arc4.convertBytes<arc4.Uint128>(op.extract(Bytes(n), 48, 16), {
          strategy: 'unsafe-cast',
        }),
      )
      // result.push(new arc4.Uint128(n))
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

    let candidate: biguint
    for (let i = Uint64(0); i < length; i = i + 1) {
      while (true) {
        ;[helperState, candidate] = __pcg128UnboundedRandom(helperState)
        if (candidate >= threshold) {
          // Please read the comment up above of the similar line in the unbounded case for more
          //  explanation of this byte sorcery.
          // In this case, we leverage the fact that operations between biguints [(candidate % x) + y]
          //  in the AVM always return the unpadded version.
          // Given this, we manually pad it as an arc4.Uint128.
          result.push(
            arc4.convertBytes<arc4.Uint128>(Bytes((candidate % absoluteBound) + lowerBound).bitwiseOr(op.bzero(16)), {
              strategy: 'unsafe-cast',
            }),
          )
          // result.push(new arc4.Uint128((candidate % absoluteBound) + lowerBound))
          break
        }
      }
    }
  }

  return [state, clone(result)]
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
