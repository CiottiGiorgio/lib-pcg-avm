# PCG Random Number Generator, AVM Edition

## lib-pcg-pyteal
This [AlgoKit](http://algokit.io) subproject implements PCG in [PyTeal](https://pyteal.readthedocs.io/en/stable/).
For more general info on this library, see the [main page](../..).

## Getting Started
Copy both the [pcg32](./lib_pcg/xsh_rr_64_32.py) and the [pcg64](./lib_pcg/xsh_rr_double_64_32.py)
files in your own project’s `lib_pcg` folder.

Import the library in your contracts like:
```python
...
from lib_pcg.xsh_rr_64_32 import pcg32_init, pcg32_random
...

@app.external
def your_method(
    ...
) -> ...:
    # Here you would acquire a safe randomness seed.
    ...
    
    # Create a ScratchVar that holds your PRNG state.
    rng_handle = pt.ScratchVar(pt.TealType.uint64)

    return pt.Seq(
        # Seed the PRNG
        pcg32_init(rng_handle.index(), seed.get()),
        
        # Generate a sequence
        output.decode(
            pcg32_random(
                rng_handle.index(),
                pt.Int(32),
                lower_bound.get(),
                upper_bound.get(),
                length.get(),
            )
        ),
    )
```
You can also take a look at the exposer contracts:
[
  [1](./smart_contracts/lib_pcg32_exposer/contract.py),
  [2](./smart_contracts/lib_pcg64_exposer/contract.py)
]

## Usage
Due to internal details, the `8 / 16 / 32`-bit generators all use `pcg32_init()` for seeding the algorithms,
but then you should use the respective `pcg8/16/32_random()` function to get your sequence.
This will change in the future to prevent ambiguity.

`64`-bit generator uses the respective `pcg64_init()` function.

You can pass non-zero `lower_bound` and `upper_bound` arguments to `pcg<N>_random()` to get integers in a desired range.  
Note that:
- `lower_bound` is always included in your range.
- `upper_bound` is always excluded by your range.
- You can set them independently.
- The range should be at least two elements wide.

When either bound is set to zero, that bound is not applied.

## Feature Support
- [ ] Package published on PyPI
- [x] `8 / 16 / 32`-bit generator
- [x] `64`-bit generator
- [ ] `128`-bit generator
