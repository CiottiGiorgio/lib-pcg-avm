import { Contract } from '@algorandfoundation/tealscript';
import { pcg16Init, pcg16Random, pcg32Init, pcg32Random, pcg8Init, pcg8Random } from '../lib_pcg/pcg32.algo';
import { MAX_UINT16_IN_STACK_ARRAY, MAX_UINT32_IN_STACK_ARRAY, MAX_UINT8_IN_STACK_ARRAY } from './consts';

export class LibPcg32TestHarnessTs extends Contract {
  get_pcg32_sequence_arc4_uint32_return(
    seed: bytes<8>,
    lowerBound: uint32,
    upperBound: uint32,
    length: uint16
  ): uint32[] {
    let state = pcg32Init(castBytes<bytes>(seed));

    const result = pcg32Random(state, lowerBound as uint64, upperBound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  get_pcg32_sequence_arc4_uint16_return(
    seed: bytes<8>,
    lowerBound: uint16,
    upperBound: uint16,
    length: uint16
  ): uint16[] {
    let state = pcg16Init(castBytes<bytes>(seed));

    const result = pcg16Random(state, lowerBound as uint64, upperBound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  get_pcg32_sequence_arc4_uint8_return(seed: bytes<8>, lowerBound: uint8, upperBound: uint8, length: uint16): uint8[] {
    let state = pcg8Init(castBytes<bytes>(seed));

    const result = pcg8Random(state, lowerBound as uint64, upperBound as uint64, length as uint64);
    state = result[0];

    return result[1];
  }

  runtime_asserts_pcg32_stack_array(): void {
    const state = pcg32Init(bzero(8));

    // Can produce a maximal length stack-based array of uint32s.
    const result = pcg32Random(state, 0, 0, MAX_UINT32_IN_STACK_ARRAY - 2);
  }

  runtime_asserts_pcg16_stack_array(): void {
    const state = pcg16Init(bzero(8));

    // Can produce a maximal length stack-based array of uint16s.
    const result = pcg16Random(state, 0, 0, MAX_UINT16_IN_STACK_ARRAY - 5);
  }

  runtime_asserts_pcg8_stack_array(): void {
    const state = pcg8Init(bzero(8));

    // Can produce a maximal length stack-based array of uint8s.
    const result = pcg8Random(state, 0, 0, MAX_UINT8_IN_STACK_ARRAY - 12);
  }

  runtime_failure_stack_byteslice_overflow(): void {
    const state = pcg32Init(bzero(8));

    const result = pcg32Random(state, 0, 0, MAX_UINT32_IN_STACK_ARRAY - 1);
  }

  @allow.bareCreate()
  createApplication() {
    assert(globals.creatorAddress === this.txn.sender);
  }
}
