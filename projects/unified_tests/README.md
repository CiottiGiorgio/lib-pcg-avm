# PCG Random Number Generator, AVM Edition

## unified_tests
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
From the [unified_tests subproject folder](.), it’s possible to link all contracts with:
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
From the [unified_tests subproject folder](.) (and from [root folder](../..)), it’s possible to test all libraries with:
```bash
algokit project run test
```

It’s also possible to link a specific implementation with:
```bash
algokit project run test-algopy
algokit project run test-algots
algokit project run test-pyteal
```
