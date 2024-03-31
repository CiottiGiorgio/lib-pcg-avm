import json

from pathlib import Path

import algokit_utils
import pytest
from algokit_utils import get_localnet_default_account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.lib_pcg64_exposer.client import (
    LibPcg64ExposerClient,
    SimulateOptions,
)


@pytest.fixture(scope="session")
def lib_pcg64_exposer_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcg64ExposerClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcg64ExposerClient(
        algod_client,
        creator=get_localnet_default_account(algod_client),
        indexer_client=indexer_client,
    )

    client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.ReplaceApp,
        on_update=algokit_utils.OnUpdate.UpdateApp,
    )
    return client


RNG_SEED = b"\x00\x00\x00\x00\x00\x00\x00\x2A" + b"\x00\x00\x00\x00\x00\x00\x00\x36"

EXPECTED_MAXIMAL_SEQUENCE_LENGTH = 127
UNBOUNDED_MAX_OPUP_CALLS = 30
BOUNDED_MAX_OPUP_CALLS = 32
# These sequences are generated using the reference C implementation.
p = Path(__file__).parent.parent.parent.parent / "test_vectors" / "64bit_sequences.json"
with open(p) as f:
    test_vectors = json.load(f)

UNBOUNDED_SEQUENCE = test_vectors["unbounded"]
LOWER_BOUNDED_SEQUENCE = test_vectors["lower_bounded"]
UPPER_BOUNDED_SEQUENCE = test_vectors["upper_bounded"]
UPPER_LOWER_BOUNDED_SEQUENCE = test_vectors["upper_lower_bounded"]


# This simple test ensures that the code size of this library doesn't grow unexpectedly if we
#  start taking subroutine inlining and opcode assembly opportunities.
def test_library_size(lib_pcg64_exposer_client: LibPcg64ExposerClient):
    assert len(lib_pcg64_exposer_client.app_client.approval.teal.split("\n")) < 550


def test_unbounded_maximal_cost(
    lib_pcg64_exposer_client: LibPcg64ExposerClient,
) -> None:
    result = (
        lib_pcg64_exposer_client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=0,
            upper_bound=0,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * UNBOUNDED_MAX_OPUP_CALLS
    )


def test_bounded_maximal_cost(lib_pcg64_exposer_client: LibPcg64ExposerClient) -> None:
    result = (
        lib_pcg64_exposer_client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=1,
            upper_bound=2**64 - 1,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value
    assert (
        result.simulate_response["txn-groups"][0]["app-budget-consumed"]
        < 700 * BOUNDED_MAX_OPUP_CALLS
    )


def test_unbounded_sequence(lib_pcg64_exposer_client: LibPcg64ExposerClient) -> None:
    result = (
        lib_pcg64_exposer_client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=0,
            upper_bound=0,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value == UNBOUNDED_SEQUENCE


def test_lower_bounded_sequence(
    lib_pcg64_exposer_client: LibPcg64ExposerClient,
) -> None:
    result = (
        lib_pcg64_exposer_client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=2**63 - 1,
            upper_bound=0,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value == LOWER_BOUNDED_SEQUENCE


def test_upper_bounded_sequence(
    lib_pcg64_exposer_client: LibPcg64ExposerClient,
) -> None:
    result = (
        lib_pcg64_exposer_client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=0,
            upper_bound=2**63 + 1,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value == UPPER_BOUNDED_SEQUENCE


def test_upper_lower_bounded_sequence(
    lib_pcg64_exposer_client: LibPcg64ExposerClient,
) -> None:
    result = (
        lib_pcg64_exposer_client.compose()
        .bounded_rand_uint64(
            seed=RNG_SEED,
            lower_bound=2**16,
            upper_bound=2**48,
            length=EXPECTED_MAXIMAL_SEQUENCE_LENGTH,
        )
        .simulate(SimulateOptions(extra_opcode_budget=320_000))
    )

    assert result.abi_results[0].return_value == UPPER_LOWER_BOUNDED_SEQUENCE
