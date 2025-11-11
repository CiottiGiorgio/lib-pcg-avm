from algokit_utils import (
    AlgorandClient,
    OnSchemaBreak,
    OnUpdate,
    SendAtomicTransactionComposerResults,
    SigningAccount,
)
from algokit_utils.applications.app_client import MAX_SIMULATE_OPCODE_BUDGET

from smart_contracts.artifacts.lib_pcg32_test_harness_algo_py import (
    LibPcg32TestHarnessAlgoPyClient,
    LibPcg32TestHarnessAlgoPyFactory,
)

from .adapter import ILibPCG32TestHarnessAdapter


class LibPCG32TestHarnessAdapter(ILibPCG32TestHarnessAdapter):
    app_client: LibPcg32TestHarnessAlgoPyClient

    def deploy(self, algorand_client: AlgorandClient, deployer: SigningAccount) -> None:
        self.app_client, _ = LibPcg32TestHarnessAlgoPyFactory(
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

    def get_pcg32_sequence_arc4_uint32_return(
        self, seed: bytes, lower_bound: int, upper_bound: int, length: int
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .get_pcg32_sequence_arc4_uint32_return(
                (seed, lower_bound, upper_bound, length)
            )
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def get_pcg32_sequence_arc4_uint16_return(
        self, seed: bytes, lower_bound: int, upper_bound: int, length: int
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .get_pcg32_sequence_arc4_uint16_return(
                (seed, lower_bound, upper_bound, length)
            )
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def get_pcg32_sequence_arc4_uint8_return(
        self, seed: bytes, lower_bound: int, upper_bound: int, length: int
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .get_pcg32_sequence_arc4_uint8_return(
                (seed, lower_bound, upper_bound, length)
            )
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def runtime_asserts_pcg32_stack_array(
        self,
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .runtime_asserts_pcg32_stack_array()
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def runtime_asserts_pcg16_stack_array(
        self,
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .runtime_asserts_pcg16_stack_array()
            .simulate(extra_opcode_budget=MAX_SIMULATE_OPCODE_BUDGET)
        )

    def runtime_asserts_pcg8_stack_array(
        self,
    ) -> SendAtomicTransactionComposerResults:
        return (
            self.app_client.new_group()
            .runtime_asserts_pcg8_stack_array()
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
