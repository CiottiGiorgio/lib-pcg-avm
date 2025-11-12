import { Contract, Uint64, op, arc4 } from '@algorandfoundation/algorand-typescript'
import { pcg64Init, pcg64Random } from '../../lib_pcg/pcg64.algo'
import { MAX_UINT64_IN_STACK_ARRAY } from '../consts.algo'

export class LibPcg64TestHarnessAlgoTs extends Contract {
  public get_pcg64_sequence_arc4_uint64_return(
    seed: arc4.StaticArray<arc4.Byte, 16>,
    lower_bound: arc4.Uint64,
    upper_bound: arc4.Uint64,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint64> {
    const state = pcg64Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg64Random(state, lower_bound.asUint64(), upper_bound.asUint64(), length.asUint64())

    return sequence
  }

  public runtime_asserts_pcg64_stack_array(): void {
    const state = pcg64Init(op.bzero(16))

    // Can produce a maximal length stack-based array
    // Because puya-ts returns the tuple from pcg64Random as a byteslice instead of a multi-value on the stack,
    //  we need to account for the overhead of that in the max sequence we can generate on a stack array.
    // It should be two uint16 for the tuple head, and two uint64 for the state.
    // Given that the residual stack size after the array prefix is not divisible by 8 (64bits), we are still able
    //  to squeeze one more uint64 in.
    // Tests confirm this to be the overhead.
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg64Random(state, Uint64(0), Uint64(0), Uint64(MAX_UINT64_IN_STACK_ARRAY - 2))
  }

  public runtime_failure_stack_byteslice_overflow(): void {
    const state = pcg64Init(op.bzero(16))

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg64Random(state, Uint64(0), Uint64(0), Uint64(MAX_UINT64_IN_STACK_ARRAY - 1))
  }
}
