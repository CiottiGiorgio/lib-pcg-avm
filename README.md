# PCG Random Number Generator, AVM Edition

## lib-pcg-avm
**lib-pcg-avm** is a library for pseudo-random number generation based on the PCG (Permuted Congruential Generator) family of algorithms.
This library is implemented in three languages that compile down to AVM (Algorand Virtual Machine) bytecode:
- [Algorand Python](./projects/lib-pcg-algopy/README.md)
- [TEALScript](./projects/lib-pcg-ts/README.md)
- [PyTeal](./projects/lib-pcg-pyteal/README.md)

The reference implementation is the [PCG C Basic Implementation](https://github.com/imneme/pcg-c-basic).
The theory and analysis of PCG are covered in the excellent [PCG paper](https://www.pcg-random.org/paper.html).

I also talked briefly about lib-pcg-avm and randomness in Algorand in this [Decipher 2024 short talk](https://youtu.be/zdrD_OrhfDw?si=fV_lpsPUhhyEM7_0).

## Disclaimer
This library is not audited for soundness and safety. It’s also still a work in progress.
All three implementations are subject to the same test suite.
The test vectors used in the test suite are generated using the reference implementation.

Use at your own risk. See [MIT License](./LICENSE).

## Features and Usage
Each library implementation in this project can generate `8 / 16 / 32 / 64 / 128`-bit unsigned pseudo-random integer sequences.
For any of these `<N>`-bits numbers, the respective generator will be called `pcg<N>`.

A distinctive feature of this variant of the PCG family of algorithms, is that the `seed` it uses is always double the
size of the output integers.
For instance, the `pcg128` generator takes a 256-bit seed. Keep this in mind when you initialize the generator
with a (potentially larger) randomness seed.

The `pcg32` is the basic building block for all other generators:
- Generators that output smaller integers are essentially a single `pcg32` with its output truncated.
- Generators that output larger integers are essentially multiple `pcg32` properly initialized and combined.

When in doubt, pick `pcg64` generator.
Otherwise, you should always pick the smallest generator for your use case.
They are equally safe, but larger generators will cost you more regarding opcode budget and stack size.

## How to Seed the PRNG
An excellent way to acquire a pseudo-random seed is to use the [Algorand Randomness Beacon](https://developer.algorand.org/articles/randomness-on-algorand/).
To do it safely, follow the [Best Practices](https://developer.algorand.org/articles/usage-and-best-practices-for-randomness-beacon/).

See an example [here](https://github.com/CiottiGiorgio/verifiable-giveaway/blob/79aebd2cad78389699deea87e904b9acc7e7fe61/projects/verifiable-giveaway-contracts/smart_contracts/verifiable_giveaway/contract.py).

## Why Should I Use This Library?
PRNG algorithms can fail in very subtle ways that are difficult to detect and correct for.
This library is the result of months of research and development, and it implements the industry’s best practices when it comes to
[statistical soundness](https://en.wikipedia.org/wiki/Pseudorandom_number_generator#Potential_issues),
[modulo bias](https://www.pcg-random.org/posts/bounded-rands.html), and
[performance](https://www.pcg-random.org/rng-performance.html) (which in the AVM translates into opcode economy).

## Contributing
This is a project based on [AlgoKit](http://algokit.io). To contribute to the library clone this repo and, from the [root folder](.):
```bash
algokit project bootstrap all
```

To use LocalNet, start it with:
```bash
algokit localnet start
```

From any subproject folder, build the library with:
```bash
algokit project run build
```

## Testing
See [unified_tests](./projects/unified_tests/README.md).
