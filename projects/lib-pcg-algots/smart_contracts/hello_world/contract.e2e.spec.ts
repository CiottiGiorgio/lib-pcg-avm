import { Config } from '@algorandfoundation/algokit-utils'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { HelloWorldFactory } from '../artifacts/hello_world/HelloWorldClient'

describe('HelloWorld contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
      // traceAll: true,
    })
  })
  beforeEach(localnet.beforeEach)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(HelloWorldFactory, {
      defaultSender: account,
    })

    const { appClient } = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append' })
    return { client: appClient }
  }

  test('says hello', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client.send.hello({ args: { name: 'World' } })

    expect(result.return).toBe('Hello World')
  })

  test('simulate says hello with correct budget consumed', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)
    const result = await client
      .newGroup()
      .hello({ args: { name: 'World' } })
      .hello({ args: { name: 'Jane' } })
      .simulate()

    expect(result.returns[0]).toBe('Hello World')
    expect(result.returns[1]).toBe('Hello Jane')
    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed).toBeLessThan(100)
  })
})
