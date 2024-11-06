import { Contract } from '@algorandfoundation/tealscript';
import { pcg128Init, pcg128Random } from '../lib_pcg/pcg128.algo';

export class LibPcg128ExposerTs extends Contract {
  // eslint-disable-next-line camelcase
  bounded_rand_uint128(seed: bytes<32>, lower_bound: uint128, upper_bound: uint128, length: uint16): uint128[] {
    let state = pcg128Init(seed);

    const result = pcg128Random(state, lower_bound, upper_bound, length as uint64);
    state = result[0];

    return result[1];
  }

  updateApplication() {
    assert(globals.creatorAddress === this.txn.sender);
  }
}
