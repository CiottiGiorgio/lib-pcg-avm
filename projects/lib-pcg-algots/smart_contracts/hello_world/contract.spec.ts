import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import { HelloWorld } from './contract.algo'

describe('HelloWorld contract', () => {
  const ctx = new TestExecutionContext()
  it('Logs the returned value when sayHello is called', () => {
    const contract = ctx.contract.create(HelloWorld)

    const result = contract.hello('Sally')

    expect(result).toBe('Hello Sally')
  })
})
