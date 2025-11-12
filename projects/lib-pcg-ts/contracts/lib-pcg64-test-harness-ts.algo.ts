import { Contract } from '@algorandfoundation/tealscript';
import { pcg64Init, pcg64Random } from '../lib_pcg/pcg64.algo';
import { MAX_UINT64_IN_STACK_ARRAY } from './consts';

export class LibPcg64TestHarnessTs extends Contract {
  get_pcg64_sequence_arc4_uint64_return(
    seed: bytes<16>,
    lowerBound: uint64,
    upperBound: uint64,
    length: uint16
  ): uint64[] {
    let state = pcg64Init(seed);

    const result = pcg64Random(state, lowerBound as uint64, upperBound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  runtime_asserts_pcg64_stack_array(): void {
    const state = pcg64Init(bzero(16));

    // Can produce a maximal length stack-based array of uint64s.
    const result = pcg64Random(state, 0, 0, MAX_UINT64_IN_STACK_ARRAY - 2);
  }

  runtime_failure_stack_byteslice_overflow(): void {
    const state = pcg64Init(bzero(16));

    const result = pcg64Random(state, 0, 0, MAX_UINT64_IN_STACK_ARRAY - 1);
  }

  @allow.bareCreate()
  createApplication() {
    assert(globals.creatorAddress === this.txn.sender);
  }
}
