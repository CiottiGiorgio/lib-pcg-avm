import logging

import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    from smart_contracts.artifacts.hello_world.client import (
        HelloWorldClient,
    )

    app_client = HelloWorldClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )
    is_mainnet = algokit_utils.is_mainnet(algod_client)
    app_client.deploy(
        on_schema_break=(
            algokit_utils.OnSchemaBreak.AppendApp
            if is_mainnet
            else algokit_utils.OnSchemaBreak.ReplaceApp
        ),
        on_update=(
            algokit_utils.OnUpdate.AppendApp
            if is_mainnet
            else algokit_utils.OnUpdate.UpdateApp
        ),
        allow_delete=not is_mainnet,
        allow_update=not is_mainnet,
    )

    name = "world"
    response = app_client.hello(name=name)
    logger.info(
        f"Called hello on {app_spec.contract.name} ({app_client.app_id}) "
        f"with name={name}, received: {response.return_value}"
    )
