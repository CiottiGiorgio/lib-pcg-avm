from abc import ABC, abstractmethod

from algokit_utils import (
    AlgorandClient,
    SendAtomicTransactionComposerResults,
    SigningAccount,
)


class ILibPCG128TestHarnessAdapter(ABC):
    @abstractmethod
    def deploy(self, algorand_client: AlgorandClient, deployer: SigningAccount) -> None:
        pass

    @property
    @abstractmethod
    def bytecode_size(self) -> int:
        pass

    @abstractmethod
    def get_pcg128_sequence_native_biguint_return(
        self,
        seed: bytes,
        lower_bound: int,
        upper_bound: int,
        length: int,
    ) -> SendAtomicTransactionComposerResults:
        pass

    @abstractmethod
    def get_pcg128_sequence_arc4_uint128_return(
        self,
        seed: bytes,
        lower_bound: int,
        upper_bound: int,
        length: int,
    ) -> SendAtomicTransactionComposerResults:
        pass

    @abstractmethod
    def runtime_asserts(self) -> SendAtomicTransactionComposerResults:
        pass

    @abstractmethod
    def runtime_failure_stack_byteslice_overflow(
        self,
    ) -> SendAtomicTransactionComposerResults:
        pass
