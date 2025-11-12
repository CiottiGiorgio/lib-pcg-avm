import { Contract, Uint64, op, arc4 } from '@algorandfoundation/algorand-typescript'
import { pcg16Init, pcg16Random, pcg32Init, pcg32Random, pcg8Init, pcg8Random } from '../../lib_pcg/pcg32.algo'
import { MAX_UINT16_IN_STACK_ARRAY, MAX_UINT32_IN_STACK_ARRAY, MAX_UINT8_IN_STACK_ARRAY } from '../consts'

export class LibPcg32TestHarnessAlgoTs extends Contract {
  public get_pcg32_sequence_arc4_uint32_return(
    seed: arc4.StaticArray<arc4.Byte, 8>,
    lower_bound: arc4.Uint32,
    upper_bound: arc4.Uint32,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint32> {
    const state = pcg32Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg32Random(state, lower_bound.asUint64(), upper_bound.asUint64(), length.asUint64())

    return sequence
  }

  public get_pcg32_sequence_arc4_uint16_return(
    seed: arc4.StaticArray<arc4.Byte, 8>,
    lower_bound: arc4.Uint16,
    upper_bound: arc4.Uint16,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint16> {
    const state = pcg16Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg16Random(state, lower_bound.asUint64(), upper_bound.asUint64(), length.asUint64())

    return sequence
  }

  public get_pcg32_sequence_arc4_uint8_return(
    seed: arc4.StaticArray<arc4.Byte, 8>,
    lower_bound: arc4.Uint8,
    upper_bound: arc4.Uint8,
    length: arc4.Uint16,
  ): arc4.DynamicArray<arc4.Uint8> {
    const state = pcg8Init(seed.bytes)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg8Random(state, lower_bound.asUint64(), upper_bound.asUint64(), length.asUint64())

    return sequence
  }

  public runtime_asserts_pcg32_stack_array(): void {
    const state = pcg32Init(op.bzero(8))

    // Can produce a maximal length stack-based array
    // Because puya-ts returns the tuple from pcg32Random as a byteslice instead of a multi-value on the stack,
    //  we need to account for the overhead of that in the max sequence we can generate on a stack array.
    // It should be two uint16 for the tuple head, and one uint64 for the state (amounting 3 uint32).
    // Tests confirm this to be the overhead.
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg32Random(state, Uint64(0), Uint64(0), Uint64(MAX_UINT32_IN_STACK_ARRAY - 3))
  }

  public runtime_asserts_pcg16_stack_array(): void {
    const state = pcg16Init(op.bzero(8))

    // Can produce a maximal length stack-based array
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg16Random(state, Uint64(0), Uint64(0), Uint64(MAX_UINT16_IN_STACK_ARRAY - 6))
  }

  public runtime_asserts_pcg8_stack_array(): void {
    const state = pcg8Init(op.bzero(8))

    // Can produce a maximal length stack-based array
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg8Random(state, Uint64(0), Uint64(0), Uint64(MAX_UINT8_IN_STACK_ARRAY - 12))
  }

  public runtime_failure_stack_byteslice_overflow(): void {
    const state = pcg32Init(op.bzero(8))

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const [newState, sequence] = pcg32Random(state, Uint64(0), Uint64(0), Uint64(MAX_UINT32_IN_STACK_ARRAY - 1))
  }
}
