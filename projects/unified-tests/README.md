# PCG Random Number Generator, AVM Edition

## unified-tests
This [AlgoKit](http://algokit.io) subproject implements the common tests for all included implementations of PCG for the AVM.
For more general info on this library, see the [main page](../..).

This testing suite guarantees that:
- The generated sequences are equal to the expected sequences from the reference implementation.
- The on-chain cost (in terms of opcode budget and library size) is bounded to reasonable limits.

## How to Run Tests
Each implementation exposes library code through `exposer` contracts.
These `exposer` contracts must be re-built and linked to this subproject before running tests.

### Building
From the [root folder](../..), it’s possible to build all contracts with:
```bash
algokit project run build
```
the same command can be used from a subproject folder to build a specific implementation.

It’s also possible to build a specific implementation with:
```bash
algokit project run build --project-name=lib-pcg-algopy
algokit project run build --project-name=lib-pcg-algots
algokit project run build --project-name=lib-pcg-pyteal
```

### Linking
From the [unified-tests subproject folder](.), it’s possible to link all contracts with:
```bash
algokit project link --all --language=python
```

It’s also possible to link a specific implementation with:
```bash
algokit project link --project-name=lib-pcg-algopy --language=python
algokit project link --project-name=lib-pcg-algots --language=python
algokit project link --project-name=lib-pcg-pyteal --language=python
```

### Testing
From the [unified-tests subproject folder](.) (and from [root folder](../..)), it’s possible to test all libraries with:
```bash
algokit project run test
```

It’s also possible to link a specific implementation with:
```bash
algokit project run test-algopy
algokit project run test-algots
algokit project run test-pyteal
```

## Testing Methodology

The golden standard for testing a PRNG is a strong statistical test ran over a significant 
portion of the generator's output.
Since this is not a new kind of generator, it should be enough to validate that it runs
the same as another reference implementation.

This is straightforward to do only in the 32-bit case where there's no extension mechanism and 
generators from the minimal C implementation can be directly compared with lib-pcg-avm.
The only reference implementation that uses extension mechanisms is the cpp implementation, and it 
uses the extension mechanism described in chapter 7.1 of the PCG paper.
Since generators from 64-bit and beyond use the extension mechanism described in chapter 4.3.4 
of the PCG paper, the outputs are not directly comparable.

The values for the 64-bit and 128-bit generators are created by modifying the minimal C implementation
of the reference PCG implementation to extend with the mechanism described in chapter 4.3.4.

Nevertheless, all generators in lib-pcg-avm are tested to produce the same values by comparing 
a short initial sequence.
