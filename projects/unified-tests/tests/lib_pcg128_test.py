import pytest
from algokit_utils import (
    AlgorandClient,
    LogicError,
    SigningAccount,
)
from test_harness.lib_pcg128.adapter import ILibPCG128TestHarnessAdapter

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
def lib_pcg128_harness(
    request: pytest.FixtureRequest,
    algorand_client: AlgorandClient,
    deployer: SigningAccount,
) -> ILibPCG128TestHarnessAdapter:
    language = request.config.getoption("language")
    match language:
        case "algopy":
            from test_harness.lib_pcg128.algopy import LibPCG128TestHarnessAdapter

            harness = LibPCG128TestHarnessAdapter()
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
            return 15_500
        case "algots":
            return 13_500
        case "ts":
            return 35_500
        case "pyteal":
            return 9_500
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_unbounded_arc4_uint128_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 23
        case "algots":
            pass
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_bounded_arc4_uint128_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 39
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
    lib_pcg128_harness: ILibPCG128TestHarnessAdapter, expected_library_size: int
) -> None:
    assert lib_pcg128_harness.bytecode_size < expected_library_size


@pytest.mark.parametrize(
    "max_opup_fixture_name,lower_bound,upper_bound,expected_sequence",
    [
        (
            "max_opup_unbounded_arc4_uint128_return",
            0,
            0,
            UNBOUNDED_SEQUENCE["pcg128-128bit"],
        ),
        (
            "max_opup_bounded_arc4_uint128_return",
            2**127 - 1,
            0,
            LOWER_BOUNDED_SEQUENCE["pcg128-128bit"],
        ),
        (
            "max_opup_bounded_arc4_uint128_return",
            0,
            2**127 + 1,
            UPPER_BOUNDED_SEQUENCE["pcg128-128bit"],
        ),
        (
            "max_opup_bounded_arc4_uint128_return",
            1,
            2**128 - 1,
            FULLY_BOUNDED_SEQUENCE["pcg128-128bit"],
        ),
    ],
)
def test_arc4_uint128_return(
    lib_pcg128_harness: ILibPCG128TestHarnessAdapter,
    max_opup_fixture_name: str,
    lower_bound: int,
    upper_bound: int,
    expected_sequence: list[int],
    request: pytest.FixtureRequest,
) -> None:
    max_opup = request.getfixturevalue(max_opup_fixture_name)

    result = lib_pcg128_harness.get_pcg128_sequence_arc4_uint128_return(
        RNG_SEED["pcg128"],
        lower_bound,
        upper_bound,
        expected_maximal_sequence_length(128),
    )

    assert result.returns[0].value == expected_sequence
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < OPCODE_BUDGET_PER_APP_CALL * max_opup
    )


def test_runtime_runtime_asserts_pcg128_stack_array(
    lib_pcg128_harness: ILibPCG128TestHarnessAdapter,
) -> None:
    result = lib_pcg128_harness.runtime_asserts_pcg128_stack_array()

    assert result.returns[0]


def test_failure(lib_pcg128_harness: ILibPCG128TestHarnessAdapter) -> None:
    with pytest.raises(LogicError, match=r"concat produced a too big \(4098\) byte-array"):
        lib_pcg128_harness.runtime_failure_stack_byteslice_overflow()
