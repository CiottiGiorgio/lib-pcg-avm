# PCG Random Number Generator, AVM Edition

## lib-pcg-algopy
This [AlgoKit](http://algokit.io) subproject implements PCG in [Algorand Python](https://github.com/algorandfoundation/puya).
For more general info on this library, see the [main page](https://github.com/CiottiGiorgio/lib-pcg-avm).

## Getting Started
Install `lib-pcg-algopy` in your project.
Using poetry, this looks like:
```bash
poetry add lib-pcg-algopy
```

The typical use case of using the library to generate a sequence of pseudo-random numbers looks like:
```python
from algopy import arc4
from lib_pcg import pcg32_init, pcg32_random

class YourContract(arc4.ARC4Contract):
  @arc4.abimethod
  def your_method(self, ...) -> ...:
    # Here you would acquire a safe randomness seed.
    ...
    
    # Seed the PRNG
    state = pcg32_init(<your_randomness_seed>)
  
    # Generate a sequence
    state, sequence = pcg32_random(state, <lower_bound>, <upper_bound>, <sequence_length>)
  
    # The rest of your program
    ...
```
You can also take a look at the exposer contracts:
[
  [1](https://github.com/CiottiGiorgio/lib-pcg-avm/blob/main/projects/lib-pcg-algopy/smart_contracts/lib_pcg32_exposer/contract.py),
  [2](https://github.com/CiottiGiorgio/lib-pcg-avm/blob/main/projects/lib-pcg-algopy/smart_contracts/lib_pcg64_exposer/contract.py),
  [3](https://github.com/CiottiGiorgio/lib-pcg-avm/blob/main/projects/lib-pcg-algopy/smart_contracts/lib_pcg128_exposer/contract.py)
]

## Usage
All generators all use `pcg<N>_init()` for seeding the algorithm.

To generate a sequence, use `pcg<N>_random()`.

You can pass non-zero `lower_bound` and `upper_bound` arguments to `pcg<N>_random()` to get integers in a desired range.  
Note that:
- `lower_bound` is always included in your range.
- `upper_bound` is always excluded by your range.
- You can set them independently.
- The range should be at least two elements wide.

When either bound is set to zero, that bound is not applied.

## Feature Support
- [x] Package published on PyPI
- [x] `8 / 16 / 32`-bit generator
- [x] `64`-bit generator
- [x] `128`-bit generator
