import pytest
from algokit_utils import (
    AlgorandClient,
    LogicError,
    SigningAccount,
)
from test_harness.lib_pcg64.adapter import ILibPCG64TestHarnessAdapter

from tests.consts import (
    FULLY_BOUNDED_SEQUENCE,
    LOWER_BOUNDED_SEQUENCE,
    OPCODE_BUDGET_PER_APP_CALL,
    RNG_SEED,
    UNBOUNDED_SEQUENCE,
    UPPER_BOUNDED_SEQUENCE,
)

EXPECTED_MAXIMAL_SEQUENCE_LENGTH = (1024 - 4 - 2) // (64 >> 3)


@pytest.fixture(scope="session")
def lib_pcg64_harness(
    request: pytest.FixtureRequest,
    algorand_client: AlgorandClient,
    deployer: SigningAccount,
) -> ILibPCG64TestHarnessAdapter:
    language = request.config.getoption("language")
    match language:
        case "algopy":
            from test_harness.lib_pcg64.algopy import LibPCG64TestHarnessAdapter

            harness = LibPCG64TestHarnessAdapter()
            harness.deploy(algorand_client, deployer)

            return harness
        case "algots":
            from test_harness.lib_pcg64.algots import LibPCG64TestHarnessAdapter

            harness = LibPCG64TestHarnessAdapter()
            harness.deploy(algorand_client, deployer)

            return harness
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
            return 13_000
        case "algots":
            return 9_500
        case "ts":
            return 35_500
        case "pyteal":
            return 9_500
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_unbounded_arc4_uint64_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 25
        case "algots":
            return 22
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


@pytest.fixture(scope="session")
def max_opup_bounded_arc4_uint64_return(request: pytest.FixtureRequest) -> int:
    match request.config.getoption("language"):
        case "algopy":
            return 42
        case "algots":
            return 41
        case "ts":
            pass
        case "pyteal":
            pass
        case _:
            raise ValueError


# This simple test ensures that the code size of this library doesn't grow unexpectedly if we
#  start taking subroutine inlining and opcode assembly opportunities.
def test_library_size(
    lib_pcg64_harness: ILibPCG64TestHarnessAdapter, expected_library_size: int
) -> None:
    assert lib_pcg64_harness.bytecode_size < expected_library_size


@pytest.mark.parametrize(
    "max_opup_fixture_name,lower_bound,upper_bound,expected_sequence",
    [
        (
            "max_opup_unbounded_arc4_uint64_return",
            0,
            0,
            UNBOUNDED_SEQUENCE["pcg64-64bit"],
        ),
        (
            "max_opup_bounded_arc4_uint64_return",
            2**63 - 1,
            0,
            LOWER_BOUNDED_SEQUENCE["pcg64-64bit"],
        ),
        (
            "max_opup_bounded_arc4_uint64_return",
            0,
            2**63 + 1,
            UPPER_BOUNDED_SEQUENCE["pcg64-64bit"],
        ),
        (
            "max_opup_bounded_arc4_uint64_return",
            1,
            2**64 - 1,
            FULLY_BOUNDED_SEQUENCE["pcg64-64bit"],
        ),
    ],
)
def test_arc4_uint64_return(
    lib_pcg64_harness: ILibPCG64TestHarnessAdapter,
    max_opup_fixture_name: str,
    lower_bound: int,
    upper_bound: int,
    expected_sequence: list[int],
    request: pytest.FixtureRequest,
) -> None:
    max_opup = request.getfixturevalue(max_opup_fixture_name)

    result = lib_pcg64_harness.get_pcg64_sequence_arc4_uint64_return(
        RNG_SEED["pcg64"],
        lower_bound,
        upper_bound,
        EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
    )

    assert result.returns[0].value == expected_sequence
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < OPCODE_BUDGET_PER_APP_CALL * max_opup
    )


def test_runtime_asserts_pcg64_stack_array(
    lib_pcg64_harness: ILibPCG64TestHarnessAdapter,
) -> None:
    result = lib_pcg64_harness.runtime_asserts_pcg64_stack_array()

    assert result.returns[0]


def test_failure(lib_pcg64_harness: ILibPCG64TestHarnessAdapter) -> None:
    with pytest.raises(
        LogicError, match=r"concat produced a too big \([0-9]{4}\) byte-array"
    ):
        lib_pcg64_harness.runtime_failure_stack_byteslice_overflow()
