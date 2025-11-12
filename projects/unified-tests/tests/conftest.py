import pytest
from algokit_utils import AlgoAmount, AlgorandClient, SigningAccount


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--language",
        action="store",
        help="Selects the implementation to be tested",
    )


@pytest.fixture(scope="session")
def algorand_client() -> AlgorandClient:
    return AlgorandClient.from_environment()


@pytest.fixture(scope="session")
def deployer(algorand_client: AlgorandClient) -> SigningAccount:
    account = algorand_client.account.from_environment("DEPLOYER")
    algorand_client.account.ensure_funded_from_environment(
        account_to_fund=account.address, min_spending_balance=AlgoAmount.from_algo(10)
    )
    return account
