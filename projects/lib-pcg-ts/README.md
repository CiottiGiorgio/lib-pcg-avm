# PCG Random Number Generator, AVM Edition

## lib-pcg-ts
This [AlgoKit](http://algokit.io) subproject implements PCG in [TEALScript](https://tealscript.netlify.app/).
For more general info on this library, see the [main page](../..).

## Getting Started
Copy the [pcg32](lib_pcg/pcg32.algo.ts), [pcg64](lib_pcg/pcg64.algo.ts), and [pcg128](lib_pcg/pcg128.algo.ts)
files in your own project’s `lib_pcg` folder.

In your contract, import `pcg<N>Init` and `pcg<N>Random` for your preferred size:
```typescript
export class YourContract extends Contract {
  yourMethod(...): ... {
    // Here you would acquire a safe randomness seed.
    ...

    // Seed the PRNG
    let rngState = pcg32Init(castBytes<bytes>(<your_randomness_seed>));

    // Generate a sequence
    const result = pcg32Random(rngState, lower_bound, upper_bound, length);
    const newRngState = result[0];
    const sequence = result[1];

    // The rest of your program
    ...
  }
}
```
You can also take a look at the exposer contracts:
[
  [1](./contracts/lib-pcg32-exposer-ts.algo.ts),
  [2](./contracts/lib-pcg64-exposer-ts.algo.ts),
  [3](./contracts/lib-pcg128-exposer-ts.algo.ts)
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
