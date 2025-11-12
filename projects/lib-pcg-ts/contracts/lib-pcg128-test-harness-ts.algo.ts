import { Contract } from '@algorandfoundation/tealscript';
import { pcg128Init, pcg128Random } from '../lib_pcg/pcg128.algo';
import { MAX_UINT128_IN_STACK_ARRAY } from './consts';

export class LibPcg128TestHarnessTs extends Contract {
  get_pcg128_sequence_arc4_uint128_return(
    seed: bytes<32>,
    lowerBound: uint128,
    upperBound: uint128,
    length: uint16
  ): uint128[] {
    let state = pcg128Init(seed);

    const result = pcg128Random(state, lowerBound as uint128, upperBound as uint128, length as uint64);
    state = result[0];

    return result[1];
  }

  runtime_asserts_pcg128_stack_array(): void {
    const state = pcg128Init(bzero(32));

    // Can produce a maximal length stack-based array of uint128s.
    const result = pcg128Random(state, 0 as uint128, 0 as uint128, MAX_UINT128_IN_STACK_ARRAY - 2);
  }

  runtime_failure_stack_byteslice_overflow(): void {
    const state = pcg128Init(bzero(32));

    const result = pcg128Random(state, 0 as uint128, 0 as uint128, MAX_UINT128_IN_STACK_ARRAY - 1);
  }

  @allow.bareCreate()
  createApplication() {
    assert(globals.creatorAddress === this.txn.sender);
  }
}
