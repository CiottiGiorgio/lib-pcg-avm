import { describe, test, expect, beforeAll, beforeEach } from '@jest/globals';
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing';
import { LibPcg64TsExposerClient } from '../contracts/clients/LibPcg64TsExposerClient';

const fixture = algorandFixture();

let appClient: LibPcg64TsExposerClient;

describe('LibPcg64Ts', () => {
  beforeEach(fixture.beforeEach);

  beforeAll(async () => {
    await fixture.beforeEach();
    const { algod, testAccount } = fixture.context;

    appClient = new LibPcg64TsExposerClient(
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
      .boundedRandUInt64({
        seed: new Uint8Array([
          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x36,
        ]),
        lowerBound: 0,
        upperBound: 0,
        length: 127,
      })
      .simulate({ extraOpcodeBudget: 320_000 });
    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed!).toBeLessThan(39 * 700);
    expect(result.returns[0].slice(0, 10)).toEqual([
      BigInt('14048270771836679757'),
      BigInt('7712349120530716571'),
      BigInt('8266272021060027030'),
      BigInt('4909296892041742261'),
      BigInt('17703472758907470354'),
      BigInt('7547670355139024912'),
      BigInt('14683759177899822202'),
      BigInt('15415759776988739333'),
      BigInt('8857463401779885611'),
      BigInt('18380099057036996406'),
    ]);
  });
});
