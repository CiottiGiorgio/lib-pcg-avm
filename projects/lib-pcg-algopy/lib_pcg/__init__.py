from .xsh_rr_64_32 import (
    pcg8_init,
    pcg8_random,
    pcg16_init,
    pcg16_random,
    pcg32_init,
    pcg32_random,
)
from .xsh_rr_double_64_32 import pcg64_init, pcg64_random
from .xsh_rr_quadruple_64_32 import pcg128_init, pcg128_random

__all__ = [
    "pcg32_init",
    "pcg16_init",
    "pcg8_init",
    "pcg32_random",
    "pcg16_random",
    "pcg8_random",
    "pcg64_init",
    "pcg64_random",
    "pcg128_init",
    "pcg128_random",
]
