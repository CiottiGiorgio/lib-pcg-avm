# PCG Random Number Generator, AVM Edition

## lib-pcg-ts
This [AlgoKit](http://algokit.io) subproject implements PCG in [TypeScript](https://tealscript.netlify.app/).
For more general info on this library, see the [main page](../..).

## Getting Started
Copy either the [pcg32](lib_pcg/lib-pcg32-ts.algo.ts) or the [pcg64](lib_pcg/lib-pcg64-ts.algo.ts)
file in your own project’s contract folder.

Have your contract extend from the library file like:
```typescript
export class YourContract extends LibPcg32Ts {
  yourMethod(...): ... {
    // Here you would acquire a safe randomness seed.
    ...

    // Seed the PRNG
    const rngState = this.pcg32Init(seed);

    // Generate a sequence
    const sequence = castBytes<uint32[]>(this.pcg32Random(rngState, 32, lower_bound, upper_bound, length)[1]);

    // The rest of your program
    ...
  }
}
```
You can also take a look at the exposer contracts:
[
  [1](./contracts/lib-pcg32-exposer-ts.algo.ts),
  [2](./contracts/lib-pcg64-exposer-ts.algo.ts)
]

## Usage
Due to internal details, the `8 / 16 / 32`-bit generators all use `this.pcg32Init()` for seeding the algorithms,
but then you should use the respective `this.pcg8/16/32Random()` function to get your sequence.
This will change in the future to prevent ambiguity.

`64`-bit generator uses the respective `this.pcg64Init()` function.

You can pass non-zero `lowerBound` and `upperBound` arguments to `this.pcg<N>Random()` to get integers in a desired range.
Note that:
- `lowerBound` is always included in your range.
- `upperBound` is always excluded by your range.
- You can set them independently.
- The range should be at least two elements wide.

## Feature Support
- [ ] Package published on npm
- [x] `8 / 16 / 32`-bit generator
- [x] `64`-bit generator
- [ ] `128`-bit generator
