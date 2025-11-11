from algokit_utils import (
    AlgorandClient,
    OnSchemaBreak,
    OnUpdate,
    SendAtomicTransactionComposerResults,
    SigningAccount,
)
from algokit_utils.applications.app_client import MAX_SIMULATE_OPCODE_BUDGET

from smart_contracts.artifacts.lib_pcg128_test_harness_algo_py import (
    LibPcg128TestHarnessAlgoPyClient,
    LibPcg128TestHarnessAlgoPyFactory,
)

from .adapter import ILibPCG128TestHarnessAdapter


class LibPCG128TestHarnessAdapter(ILibPCG128TestHarnessAdapter):
    app_client: LibPcg128TestHarnessAlgoPyClient

    def deploy(self, algorand_client: AlgorandClient, deployer: SigningAccount) -> None:
        self.app_client, _ = LibPcg128TestHarnessAlgoPyFactory(
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

    def get_pcg128_sequence_native_biguint_return(
        self, seed: bytes, lower_bound: int, upper_bound: int, length: int
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .get_pcg128_sequence_native_biguint_return(
                (seed, lower_bound, upper_bound, length)
            )
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def get_pcg128_sequence_arc4_uint128_return(
        self, seed: bytes, lower_bound: int, upper_bound: int, length: int
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .get_pcg128_sequence_arc4_uint128_return(
                (seed, lower_bound, upper_bound, length)
            )
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def runtime_asserts_stack_array_native_biguint(
        self,
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .runtime_asserts_stack_array_native_biguint()
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def runtime_asserts_stack_array_arc4_uint128(
        self,
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .runtime_asserts_stack_array_arc4_uint128()
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
