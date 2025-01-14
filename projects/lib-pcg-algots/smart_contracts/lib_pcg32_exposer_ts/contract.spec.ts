import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import { LibPcg32ExposerTs } from './contract.algo'

describe('LibPcg32ExposerTs contract', () => {
  const ctx = new TestExecutionContext()
  it('Logs the returned value when sayHello is called', () => {
    const contract = ctx.contract.create(LibPcg32ExposerTs)

    const result = contract.hello('Sally')

    expect(result).toBe('Hello Sally')
  })
})
