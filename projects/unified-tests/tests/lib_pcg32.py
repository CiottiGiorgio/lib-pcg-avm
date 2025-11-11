import pytest
from algokit_utils import (
    AlgorandClient,
    LogicError,
    SigningAccount,
)
from test_harness.lib_pcg32.adapter import ILibPCG32TestHarnessAdapter

from tests.consts import (
    FULLY_BOUNDED_SEQUENCE,
    LOWER_BOUNDED_SEQUENCE,
    OPCODE_BUDGET_PER_APP_CALL,
    RNG_SEED,
    UNBOUNDED_SEQUENCE,
    UPPER_BOUNDED_SEQUENCE,
)


def expected_maximal_sequence_length(bit_size: int) -> int:
    return (1024 - 4 - 2) // (bit_size >> 3)


@pytest.fixture(scope="session")
def lib_pcg32_harness(
    request: pytest.FixtureRequest,
    algorand_client: AlgorandClient,
    deployer: SigningAccount,
) -> ILibPCG32TestHarnessAdapter:
    language = request.config.getoption("language")
    match language:
        case "algopy":
            from test_harness.lib_pcg32.algopy import LibPCG32TestHarnessAdapter

            harness = LibPCG32TestHarnessAdapter()
            harness.deploy(algorand_client, deployer)

            return harness
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def expected_library_size(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 17_500
        case "algots":
            return 13_500
        case "ts":
            return 35_500
        case "pyteal":
            return 9_500
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_unbounded_native_uint64_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 12
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_unbounded_arc4_uint32_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 32
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_unbounded_arc4_uint16_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 71
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_unbounded_arc4_uint8_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 142
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_bounded_native_uint64_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 21
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_bounded_arc4_uint32_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 49
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_bounded_arc4_uint16_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 71
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_bounded_arc4_uint8_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 142
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


# This simple test ensures that the code size of this library doesn't grow unexpectedly if we
#  start taking subroutine inlining and opcode assembly opportunities.
def test_library_size(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter, expected_library_size: int
) -> None:
    assert lib_pcg32_harness.bytecode_size < expected_library_size


@pytest.mark.parametrize(
    "max_opup_fixture_name,lower_bound,upper_bound,expected_sequence",
    [
        (
            "max_opup_unbounded_native_uint64_return",
            0,
            0,
            UNBOUNDED_SEQUENCE["pcg32-native"],
        ),
        (
            "max_opup_bounded_native_uint64_return",
            2**31 - 1,
            0,
            LOWER_BOUNDED_SEQUENCE["pcg32-native"],
        ),
        (
            "max_opup_bounded_native_uint64_return",
            0,
            2**31 + 1,
            UPPER_BOUNDED_SEQUENCE["pcg32-native"],
        ),
        (
            "max_opup_bounded_native_uint64_return",
            1,
            2**32 - 1,
            FULLY_BOUNDED_SEQUENCE["pcg32-native"],
        ),
    ],
)
def test_native_uint64_return(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter,
    max_opup_fixture_name: str,
    lower_bound: int,
    upper_bound: int,
    expected_sequence: list[int],
    request: pytest.FixtureRequest,
) -> None:
    max_opup = request.getfixturevalue(max_opup_fixture_name)

    result = lib_pcg32_harness.get_pcg32_sequence_native_uint64_return(
        RNG_SEED["pcg32"],
        lower_bound,
        upper_bound,
        expected_maximal_sequence_length(64),
    )

    assert result.returns[0].value == expected_sequence
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < OPCODE_BUDGET_PER_APP_CALL * max_opup
    )


@pytest.mark.parametrize(
    "max_opup_fixture_name,lower_bound,upper_bound,expected_sequence",
    [
        (
            "max_opup_unbounded_arc4_uint32_return",
            0,
            0,
            UNBOUNDED_SEQUENCE["pcg32-32bit"],
        ),
        (
            "max_opup_bounded_arc4_uint32_return",
            2**31 - 1,
            0,
            LOWER_BOUNDED_SEQUENCE["pcg32-32bit"],
        ),
        (
            "max_opup_bounded_arc4_uint32_return",
            0,
            2**31 + 1,
            UPPER_BOUNDED_SEQUENCE["pcg32-32bit"],
        ),
        (
            "max_opup_bounded_arc4_uint32_return",
            1,
            2**32 - 1,
            FULLY_BOUNDED_SEQUENCE["pcg32-32bit"],
        ),
    ],
)
def test_arc4_uint32_return(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter,
    max_opup_fixture_name: str,
    lower_bound: int,
    upper_bound: int,
    expected_sequence: list[int],
    request: pytest.FixtureRequest,
) -> None:
    max_opup = request.getfixturevalue(max_opup_fixture_name)

    result = lib_pcg32_harness.get_pcg32_sequence_arc4_uint32_return(
        RNG_SEED["pcg32"],
        lower_bound,
        upper_bound,
        expected_maximal_sequence_length(32),
    )

    assert result.returns[0].value == expected_sequence
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < OPCODE_BUDGET_PER_APP_CALL * max_opup
    )


@pytest.mark.parametrize(
    "max_opup_fixture_name,lower_bound,upper_bound,expected_sequence",
    [
        (
            "max_opup_unbounded_arc4_uint16_return",
            0,
            0,
            UNBOUNDED_SEQUENCE["pcg32-16bit"],
        ),
        (
            "max_opup_bounded_arc4_uint16_return",
            2**15 - 1,
            0,
            LOWER_BOUNDED_SEQUENCE["pcg32-16bit"],
        ),
        (
            "max_opup_bounded_arc4_uint16_return",
            0,
            2**15 + 1,
            UPPER_BOUNDED_SEQUENCE["pcg32-16bit"],
        ),
        (
            "max_opup_bounded_arc4_uint16_return",
            1,
            2**16 - 1,
            FULLY_BOUNDED_SEQUENCE["pcg32-16bit"],
        ),
    ],
)
def test_arc4_uint16_return(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter,
    max_opup_fixture_name: str,
    lower_bound: int,
    upper_bound: int,
    expected_sequence: list[int],
    request: pytest.FixtureRequest,
) -> None:
    max_opup = request.getfixturevalue(max_opup_fixture_name)

    result = lib_pcg32_harness.get_pcg32_sequence_arc4_uint16_return(
        RNG_SEED["pcg32"],
        lower_bound,
        upper_bound,
        expected_maximal_sequence_length(16),
    )

    assert result.returns[0].value == expected_sequence
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < OPCODE_BUDGET_PER_APP_CALL * max_opup
    )


@pytest.mark.parametrize(
    "max_opup_fixture_name,lower_bound,upper_bound,expected_sequence",
    [
        (
            "max_opup_unbounded_arc4_uint8_return",
            0,
            0,
            UNBOUNDED_SEQUENCE["pcg32-8bit"],
        ),
        (
            "max_opup_bounded_arc4_uint8_return",
            2**7 - 1,
            0,
            LOWER_BOUNDED_SEQUENCE["pcg32-8bit"],
        ),
        (
            "max_opup_bounded_arc4_uint8_return",
            0,
            2**7 + 1,
            UPPER_BOUNDED_SEQUENCE["pcg32-8bit"],
        ),
        (
            "max_opup_bounded_arc4_uint8_return",
            1,
            2**8 - 1,
            FULLY_BOUNDED_SEQUENCE["pcg32-8bit"],
        ),
    ],
)
def test_arc4_uint8_return(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter,
    max_opup_fixture_name: str,
    lower_bound: int,
    upper_bound: int,
    expected_sequence: list[int],
    request: pytest.FixtureRequest,
) -> None:
    max_opup = request.getfixturevalue(max_opup_fixture_name)

    result = lib_pcg32_harness.get_pcg32_sequence_arc4_uint8_return(
        RNG_SEED["pcg32"], lower_bound, upper_bound, expected_maximal_sequence_length(8)
    )

    assert result.returns[0].value == expected_sequence
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < OPCODE_BUDGET_PER_APP_CALL * max_opup
    )


def test_runtime_asserts_stack_array_native_uint64(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter,
) -> None:
    result = lib_pcg32_harness.runtime_asserts_stack_array_native_uint64()

    assert result.returns[0]


def test_runtime_asserts_stack_array_arc4_uint32(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter,
) -> None:
    result = lib_pcg32_harness.runtime_asserts_stack_array_arc4_uint32()

    assert result.returns[0]


def test_runtime_asserts_stack_array_arc4_uint16(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter,
) -> None:
    result = lib_pcg32_harness.runtime_asserts_stack_array_arc4_uint16()

    assert result.returns[0]


@pytest.mark.skip(
    reason="This test takes more opcode budget than simulate can provide."
)
def test_runtime_asserts_stack_array_arc4_uint8(
    lib_pcg32_harness: ILibPCG32TestHarnessAdapter,
) -> None:
    result = lib_pcg32_harness.runtime_asserts_stack_array_arc4_uint8()

    assert result.returns[0]


def test_failure(lib_pcg32_harness: ILibPCG32TestHarnessAdapter) -> None:
    with pytest.raises(LogicError, match="max array length exceeded"):
        lib_pcg32_harness.runtime_failure_stack_byteslice_overflow()
