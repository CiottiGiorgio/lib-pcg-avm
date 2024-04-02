import { describe, test, expect, beforeAll, beforeEach } from '@jest/globals';
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing';
import { LibPcg32TsExposerClient } from '../contracts/clients/LibPcg32TsExposerClient';

const fixture = algorandFixture();

let appClient: LibPcg32TsExposerClient;

describe('LibPcg32Ts', () => {
  beforeEach(fixture.beforeEach);

  beforeAll(async () => {
    await fixture.beforeEach();
    const { algod, testAccount } = fixture.context;

    appClient = new LibPcg32TsExposerClient(
      {
        sender: testAccount,
        resolveBy: 'id',
        id: 0,
      },
      algod
    );

    await appClient.create.createApplication({});
  });

  test('random unbounded sequence', async () => {
    const result = await appClient
      .compose()
      .boundedRandUInt32({ seed: 42, lowerBound: 0, upperBound: 0, length: 254 })
      .simulate({ extraOpcodeBudget: 320_000 });
    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed!).toBeLessThan(40 * 700);
    expect(result.returns[0].slice(0, 10)).toEqual(
      [
        3270867926, 1795671209, 1924641435, 1143034755, 4121910957, 1757328946, 3418829100, 3589261271, 2062288904,
        4279450293,
      ].map((x) => BigInt(x))
    );
  });

  // Hardly worth it to implement the same testing that we have on Python here.
  // The actual release will have unified testing for all contracts correctly checking all combinations
  // of bitsize and bounds.
});
