import { Contract, BigUint, Uint64, op, arc4 } from '@algorandfoundation/algorand-typescript'
import { pcg128Init, pcg128Random } from '../../lib_pcg/pcg128.algo'
import { MAX_UINT128_IN_STACK_ARRAY } from '../consts'

export class LibPcg128TestHarnessAlgoTs extends Contract {
  public get_pcg128_sequence_arc4_uint128_return(
    seed: arc4.StaticArray<arc4.Byte, 32>,
    lower_bound: arc4.Uint128,
    upper_bound: arc4.Uint128,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint128> {
    const state = pcg128Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg128Random(
      state,
      lower_bound.asBigUint(),
      upper_bound.asBigUint(),
      length.asUint64(),
    )

    return sequence
  }

  public runtime_asserts_pcg128_stack_array(): void {
    const state = pcg128Init(op.bzero(32))

    // Can produce a maximal length stack-based array
    // Because puya-ts returns the tuple from pcg128Random as a byteslice instead of a multi-value on the stack,
    //  we need to account for the overhead of that in the max sequence we can generate on a stack array.
    // It should be two uint16 for the tuple head, and four uint64 for the state.
    // Tests confirm this to be the overhead.
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg128Random(state, BigUint(0), BigUint(0), Uint64(MAX_UINT128_IN_STACK_ARRAY - 2))
  }

  public runtime_failure_stack_byteslice_overflow(): void {
    const state = pcg128Init(op.bzero(32))

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg128Random(state, BigUint(0), BigUint(0), Uint64(MAX_UINT128_IN_STACK_ARRAY - 1))
  }
}
