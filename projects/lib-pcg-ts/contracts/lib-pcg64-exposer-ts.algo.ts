import { Contract } from '@algorandfoundation/tealscript';
import { pcg64Init, pcg64Random } from '../lib_pcg/pcg64.algo';

export class LibPcg64ExposerTs extends Contract {
  // eslint-disable-next-line camelcase
  bounded_rand_uint64(seed: bytes<16>, lower_bound: uint64, upper_bound: uint64, length: uint16): uint64[] {
    let state = pcg64Init(seed);

    const result = pcg64Random(state, lower_bound, upper_bound, length as uint64);
    state = result[0];

    return result[1];
  }

  updateApplication() {
    assert(globals.creatorAddress === this.txn.sender);
  }
}
