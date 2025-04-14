# PCG Random Number Generator, AVM Edition

## lib-pcg-algots

This [AlgoKit](http://algokit.io) subproject implements PCG in [Algorand TypeScript](https://github.com/algorandfoundation/puya-ts).
For more general info on this library, see the [main page](../..).

## Getting Started

Copy the [pcg32](lib_pcg/pcg32.algo.ts), [pcg64](lib_pcg/pcg64.algo.ts), and [pcg128](lib_pcg/pcg128.algo.ts)
files in your own project’s `lib_pcg` folder.

The typical use case of using the library to generate a sequence of pseudo-random numbers looks like:

```typescript
import { Contract, assert, Global, Txn } from '@algorandfoundation/algorand-typescript'
import { StaticArray, DynamicArray, Byte, UintN, baremethod } from '@algorandfoundation/algorand-typescript/arc4'
import { pcg32Init, pcg32Random } from '../../lib_pcg/pcg32.algo'

export class YourContract extends Contract {
  public bounded_rand_uint32(...): ... {
    // Here you would acquire a safe randomness seed
    const seed = ...

    // Seed the PRNG
    const state = pcg32Init(seed)

    // Generate a sequence
    const [newState, sequence] = pcg32Random(state, <lower_bound>, <upper_bound>, <length>)

    // The rest of your program
    ...
  }
}
```

You can also take a look at the exposer contracts:
[
[1](./smart_contracts/lib_pcg32_exposer_algo_ts/contract.algo.ts),
[2](./smart_contracts/lib_pcg64_exposer_algo_ts/contract.algo.ts),
[3](./smart_contracts/lib_pcg128_exposer_algo_ts/contract.algo.ts)
]

## Usage

All generators all use `pcg<N>Init()` for seeding the algorithm.

To generate a sequence, use `pcg<N>Random()`.

You can pass non-zero `lowerBound` and `upperBound` arguments to `pcg<N>Random()` to get integers in a desired range.  
Note that:

- `lowerBound` is always included in your range.
- `upperBound` is always excluded by your range.
- You can set them independently.
- The range should be at least two elements wide.

When either bound is set to zero, that bound is not applied.

## Feature Support

- [ ] Package published on npm
- [x] `8 / 16 / 32`-bit generator
- [x] `64`-bit generator
- [x] `128`-bit generator
