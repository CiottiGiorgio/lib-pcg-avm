import algokit_utils
import pytest
from algokit_utils import get_localnet_default_account, TransactionParameters
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk.v2client.models import SimulateRequest

from smart_contracts.artifacts.lib_pcg_exposer.client import LibPcgExposerClient


@pytest.fixture(scope="session")
def lib_pcg_exposer_client(
    algod_client: AlgodClient, indexer_client: IndexerClient
) -> LibPcgExposerClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = LibPcgExposerClient(
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


demo_budget_test_vector = [
    (1, 1),
    (5, 1),
    (7, 1),
    (8, 2),
    (15, 2),
    (16, 2),
    (17, 3),
    (25, 3),
    (26, 4),
    (50, 6),
    (150, 17),
    (200, 22),
    (254, 30),
    # For the current iteration of contracts, 254 is the max amount of numbers possible due to
    #  log size constraints.
]


# This test validates for some arbitrary lengths what is exactly the minimum amount of inners that must be called.
@pytest.mark.parametrize("length,min_n_inners", demo_budget_test_vector)
def test_demo_budget(lib_pcg_exposer_client: LibPcgExposerClient, length, min_n_inners) -> None:
    composer = lib_pcg_exposer_client.compose().bounded_rand_uint32(lower_bound=0, upper_bound=0, length=length)
    result = composer.atc.simulate(
        composer.app_client.algod_client,
        SimulateRequest(txn_groups=[], extra_opcode_budget=320_000)
    )

    assert result.simulate_response["txn-groups"][0]["app-budget-consumed"] < 700 * min_n_inners

    composer = lib_pcg_exposer_client.compose().bounded_rand_uint32(lower_bound=0, upper_bound=0, length=length)
    result = composer.atc.simulate(
        composer.app_client.algod_client,
        SimulateRequest(txn_groups=[], extra_opcode_budget=320_000)
    )

    assert result.simulate_response["txn-groups"][0]["app-budget-consumed"] > 700 * (min_n_inners - 1)


def test_random_uint32_unbounded(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    result = lib_pcg_exposer_client.bounded_rand_uint32(lower_bound=0, upper_bound=0, length=6)

    assert result.return_value == [
        3270867926, 1795671209,
        1924641435, 1143034755,
        4121910957, 1757328946,
    ]


def test_random_uint32_lower_bounded(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    composer = lib_pcg_exposer_client.compose().bounded_rand_uint32(lower_bound=2**32-2, upper_bound=0, length=4)
    result = composer.atc.simulate(
        composer.app_client.algod_client,
        SimulateRequest(txn_groups=[], extra_opcode_budget=320_000)
    )

    assert result.abi_results[0].return_value == [
        2**32-2, 2**32-1,
        2**32-1, 2**32-1,
    ]


def test_random_uint32_upper_bounded(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    result = lib_pcg_exposer_client.bounded_rand_uint32(lower_bound=0, upper_bound=10, length=4)

    assert result.return_value == [6, 9, 5, 5]


def test_random_uint32_lower_upper_bounded(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    composer = lib_pcg_exposer_client.compose().bounded_rand_uint32(lower_bound=10, upper_bound=20, length=10)
    result = composer.atc.simulate(
        composer.app_client.algod_client,
        SimulateRequest(txn_groups=[], extra_opcode_budget=320_000)
    )

    assert result.abi_results[0].return_value == [
        16, 19, 15, 15, 17,
        16, 10, 11, 14, 13,
    ]


def test_random_uint16_unbounded(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    result = lib_pcg_exposer_client.bounded_rand_uint16(lower_bound=0, upper_bound=0, length=6)

    assert result.return_value == [
        31702, 50345, 45723,
        21379, 24237, 46642,
    ]


def test_random_uint16_lower_bounded(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    composer = lib_pcg_exposer_client.compose().bounded_rand_uint16(lower_bound=2**16-2, upper_bound=0, length=4)
    result = composer.atc.simulate(
        composer.app_client.algod_client,
        SimulateRequest(txn_groups=[], extra_opcode_budget=320_000)
    )

    assert result.abi_results[0].return_value == [
        2**16-2, 2**16-1,
        2**16-1, 2**16-1,
    ]


def test_random_uint16_upper_bounded(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    result = lib_pcg_exposer_client.bounded_rand_uint16(lower_bound=0, upper_bound=10, length=4)

    assert result.return_value == [6, 9, 5, 5]


def test_random_uint16_lower_upper_bounded(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    composer = lib_pcg_exposer_client.compose().bounded_rand_uint16(lower_bound=10, upper_bound=20, length=10)
    result = composer.atc.simulate(
        composer.app_client.algod_client,
        SimulateRequest(txn_groups=[], extra_opcode_budget=320_000)
    )

    assert result.abi_results[0].return_value == [
        16, 19, 15, 15, 17,
        16, 10, 11, 14, 13,
    ]


def test_coin_toss(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    result = lib_pcg_exposer_client.bounded_rand_uint32(lower_bound=0, upper_bound=2, length=4)

    assert result.return_value == [0, 1, 1, 1]


def test_shifted_coin_toss(lib_pcg_exposer_client: LibPcgExposerClient) -> None:
    result = lib_pcg_exposer_client.bounded_rand_uint32(lower_bound=1, upper_bound=3, length=4)

    assert result.return_value == [1, 2, 2, 2]
