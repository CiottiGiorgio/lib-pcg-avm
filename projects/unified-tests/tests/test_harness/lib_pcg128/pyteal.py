from algokit_utils import (
    AlgorandClient,
    OnSchemaBreak,
    OnUpdate,
    SendAtomicTransactionComposerResults,
    SigningAccount,
)
from algokit_utils.applications.app_client import MAX_SIMULATE_OPCODE_BUDGET

from smart_contracts.artifacts.lib_pcg128_test_harness_pyteal import (
    LibPcg128TestHarnessPytealClient,
    LibPcg128TestHarnessPytealFactory,
)

from .adapter import ILibPCG128TestHarnessAdapter


class LibPCG128TestHarnessAdapter(ILibPCG128TestHarnessAdapter):
    app_client: LibPcg128TestHarnessPytealClient

    def deploy(self, algorand_client: AlgorandClient, deployer: SigningAccount) -> None:
        self.app_client, _ = LibPcg128TestHarnessPytealFactory(
            algorand_client, default_sender=deployer.address
        ).deploy(
            on_schema_break=OnSchemaBreak.AppendApp,
            on_update=OnUpdate.AppendApp,
        )

    @property
    def bytecode_size(self) -> int:
        if not self.app_client.app_client.app_spec.source:
            raise ValueError("App source not found")
        return len(self.app_client.app_client.app_spec.source.approval)

    def get_pcg128_sequence_arc4_uint128_return(
        self, seed: bytes, lower_bound: int, upper_bound: int, length: int
    ) -> SendAtomicTransactionComposerResults:
        result = (
            self.app_client.new_group()
            .get_pcg128_sequence_arc4_uint128_return(
                (
                    seed,
                    lower_bound.to_bytes(16, "big"),
                    upper_bound.to_bytes(16, "big"),
                    length,
                )
            )
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

        result.returns[0].value = [
            int.from_bytes(x, "big") for x in result.returns[0].value
        ]
        return result

    def runtime_asserts_pcg128_stack_array(
        self,
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .runtime_asserts_pcg128_stack_array()
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def runtime_failure_stack_byteslice_overflow(
        self,
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .runtime_failure_stack_byteslice_overflow()
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )
