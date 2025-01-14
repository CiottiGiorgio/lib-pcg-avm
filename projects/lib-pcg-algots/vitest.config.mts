import { puyaTsTransformer } from '@algorandfoundation/algorand-typescript-testing/test-transformer'
import typescript from '@rollup/plugin-typescript'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  esbuild: {},
  test: {
    server: {
      deps: {
        inline: ['@algorandfoundation/algorand-typescript-testing'],
      },
    },
    testTimeout: 10000,
    coverage: {
      provider: 'v8',
    },
  },
  plugins: [
    typescript({
      tsconfig: './tsconfig.test.json',
      transformers: {
        before: [puyaTsTransformer],
      },
    }),
  ],
})
