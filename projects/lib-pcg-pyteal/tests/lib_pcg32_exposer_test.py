import json
from pathlib import Path

import algokit_utils
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.atomic_transaction_composer import SimulateAtomicTransactionResponse
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.lib_pcg32_exposer.client import (
    LibPcg32ExposerClient,
    SimulateOptions,
)


@pytest.fixture(scope="session")
def lib_pcg32_exposer_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcg32ExposerClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcg32ExposerClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.ReplaceApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
        allow_delete=True,
        allow_update=True,
    )
    return client


RNG_SEED = 42

BIT_SIZES = [8, 16, 32]
UNBOUNDED_MAX_OPUP_CALLS = [91, 46, 23]
BOUNDED_MAX_OPUP_CALLS = [105, 53, 27]
# These sequences are generated using the reference C implementation.
p = Path(__file__).parent.parent.parent.parent / "test_vectors" / "32bit_sequences.json"
with open(p) as f:
    test_vectors = json.load(f)

UNBOUNDED_SEQUENCE = (test_vectors["unbounded"][f"{bits}bit"] for bits in BIT_SIZES)
LOWER_BOUNDED_SEQUENCE = (test_vectors["lower_bounded"][f"{bits}bit"] for bits in BIT_SIZES)
UPPER_BOUNDED_SEQUENCE = (test_vectors["upper_bounded"][f"{bits}bit"] for bits in BIT_SIZES)
UPPER_LOWER_BOUNDED_SEQUENCE = (test_vectors["upper_lower_bounded"][f"{bits}bit"] for bits in BIT_SIZES)


def __bit_size_to_method(
    lib_pcg32_exposer_client: LibPcg32ExposerClient,
    bit_size: int,
    lower_bound: int,
    upper_bound: int,
    length: int,
) -> SimulateAtomicTransactionResponse:
    match bit_size:
        case 8:
            result = (
                lib_pcg32_exposer_client.compose()
                .bounded_rand_uint8(
                    seed=RNG_SEED,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    length=length,
                )
                .simulate(SimulateOptions(extra_opcode_budget=320_000))
            )
        case 16:
            result = (
                lib_pcg32_exposer_client.compose()
                .bounded_rand_uint16(
                    seed=RNG_SEED,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    length=length,
                )
                .simulate(SimulateOptions(extra_opcode_budget=320_000))
            )
        case 32:
            result = (
                lib_pcg32_exposer_client.compose()
                .bounded_rand_uint32(
                    seed=RNG_SEED,
                    lower_bound=lower_bound,
                    upper_bound=upper_bound,
                    length=length,
                )
                .simulate(SimulateOptions(extra_opcode_budget=320_000))
            )
        case _:
            raise ValueError("")

    return result


# This simple test ensures that the code size of this library doesn't grow unexpectedly if we
#  start taking subroutine inlining and opcode assembly opportunities.
def test_library_size(lib_pcg32_exposer_client: LibPcg32ExposerClient):
    assert len(lib_pcg32_exposer_client.app_client.approval.teal.split("\n")) < 510


@pytest.mark.parametrize(
    "bit_size,expected_max_opup_calls", zip(BIT_SIZES, UNBOUNDED_MAX_OPUP_CALLS)
)
def test_unbounded_maximal_cost(
    lib_pcg32_exposer_client: LibPcg32ExposerClient,
    bit_size: int,
    expected_max_opup_calls: int,
) -> None:
    expected_maximal_sequence_length = (1024 - 4 - 2) // (bit_size >> 3)

    result = __bit_size_to_method(
        lib_pcg32_exposer_client, bit_size, 0, 0, expected_maximal_sequence_length
    )

    assert result.abi_results[0].return_value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * expected_max_opup_calls
    )


@pytest.mark.parametrize(
    "bit_size,expected_max_opup_calls", zip(BIT_SIZES, BOUNDED_MAX_OPUP_CALLS)
)
def test_bounded_maximal_cost(
    lib_pcg32_exposer_client: LibPcg32ExposerClient,
    bit_size: int,
    expected_max_opup_calls: int,
) -> None:
    expected_maximal_sequence_length = (1024 - 4 - 2) // (bit_size >> 3)

    result = __bit_size_to_method(
        lib_pcg32_exposer_client,
        bit_size,
        1,
        2**bit_size - 1,
        expected_maximal_sequence_length,
    )

    assert result.abi_results[0].return_value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * expected_max_opup_calls
    )


@pytest.mark.parametrize(
    "bit_size,expected_sequence", zip(BIT_SIZES, UNBOUNDED_SEQUENCE)
)
def test_unbounded_sequence(
    lib_pcg32_exposer_client: LibPcg32ExposerClient,
    bit_size: int,
    expected_sequence: [int],
) -> None:
    result = __bit_size_to_method(lib_pcg32_exposer_client, bit_size, 0, 0, 100)

    assert result.abi_results[0].return_value == expected_sequence


@pytest.mark.parametrize(
    "bit_size,expected_sequence", zip(BIT_SIZES, LOWER_BOUNDED_SEQUENCE)
)
def test_lower_bounded_sequence(
    lib_pcg32_exposer_client: LibPcg32ExposerClient,
    bit_size: int,
    expected_sequence: [int],
) -> None:
    result = __bit_size_to_method(
        lib_pcg32_exposer_client, bit_size, 2 ** (bit_size - 1) - 1, 0, 100
    )

    assert result.abi_results[0].return_value == expected_sequence


@pytest.mark.parametrize(
    "bit_size,expected_sequence", zip(BIT_SIZES, UPPER_BOUNDED_SEQUENCE)
)
def test_upper_bounded_sequence(
    lib_pcg32_exposer_client: LibPcg32ExposerClient,
    bit_size: int,
    expected_sequence: [int],
) -> None:
    result = __bit_size_to_method(
        lib_pcg32_exposer_client, bit_size, 0, 2 ** (bit_size - 1) + 1, 100
    )

    assert result.abi_results[0].return_value == expected_sequence


@pytest.mark.parametrize(
    "bit_size,expected_sequence", zip(BIT_SIZES, UPPER_LOWER_BOUNDED_SEQUENCE)
)
def test_upper_lower_bounded_sequence(
    lib_pcg32_exposer_client: LibPcg32ExposerClient,
    bit_size: int,
    expected_sequence: [int],
) -> None:
    result = __bit_size_to_method(
        lib_pcg32_exposer_client,
        bit_size,
        2 ** (bit_size >> 2),
        2 ** ((bit_size >> 2) * 3),
        100,
    )

    assert result.abi_results[0].return_value == expected_sequence


# This test covers regression in the pcg32_init function of a bug in the code.
# The bug was that the addition on initial_state was performed without truncation.
def test_correct_initstate_addition_pcg32_init(
    lib_pcg32_exposer_client: LibPcg32ExposerClient,
):
    result = lib_pcg32_exposer_client.bounded_rand_uint32(
        seed=int.from_bytes(b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"),
        lower_bound=0,
        upper_bound=0,
        length=1,
    )

    assert result
