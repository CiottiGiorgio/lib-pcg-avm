# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "bounded_rand_uint64(byte[16],uint64,uint64,uint16)uint64[]": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMSA2MzY0MTM2MjIzODQ2NzkzMDA1IDQyOTQ5NjcyOTUgMTQ0MjY5NTA0MDg4ODk2MzQwNyAxNDQyNjk1MDQwODg4OTYzNDA5CmJ5dGVjYmxvY2sgMHgKdHhuIE51bUFwcEFyZ3MKaW50Y18wIC8vIDAKPT0KYm56IG1haW5fbDQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHhiYTU2ODJjZSAvLyAiYm91bmRlZF9yYW5kX3VpbnQ2NChieXRlWzE2XSx1aW50NjQsdWludDY0LHVpbnQxNil1aW50NjRbXSIKPT0KYm56IG1haW5fbDMKZXJyCm1haW5fbDM6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CmNhbGxzdWIgYm91bmRlZHJhbmR1aW50NjRjYXN0ZXJfNgppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sNDoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQpibnogbWFpbl9sMTAKdHhuIE9uQ29tcGxldGlvbgpwdXNoaW50IDQgLy8gVXBkYXRlQXBwbGljYXRpb24KPT0KYm56IG1haW5fbDkKdHhuIE9uQ29tcGxldGlvbgpwdXNoaW50IDUgLy8gRGVsZXRlQXBwbGljYXRpb24KPT0KYm56IG1haW5fbDgKZXJyCm1haW5fbDg6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CmFzc2VydApjYWxsc3ViIGRlbGV0ZV80CmludGNfMSAvLyAxCnJldHVybgptYWluX2w5Ogp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQphc3NlcnQKY2FsbHN1YiB1cGRhdGVfMwppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sMTA6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCj09CmFzc2VydAppbnRjXzEgLy8gMQpyZXR1cm4KCi8vIHBjZzY0X2luaXQKcGNnNjRpbml0XzA6CnByb3RvIDMgMApmcmFtZV9kaWcgLTEKbGVuCnB1c2hpbnQgMTYgLy8gMTYKPT0KYXNzZXJ0CmZyYW1lX2RpZyAtMwppbnRjXzAgLy8gMApzdG9yZXMKZnJhbWVfZGlnIC0zCmludGMgNCAvLyAxNDQyNjk1MDQwODg4OTYzNDA3CmludGNfMiAvLyA2MzY0MTM2MjIzODQ2NzkzMDA1CmZyYW1lX2RpZyAtMwpsb2FkcwptdWx3CmJ1cnkgMQphZGR3CmJ1cnkgMQpzdG9yZXMKZnJhbWVfZGlnIC0zCmZyYW1lX2RpZyAtMwpsb2FkcwpmcmFtZV9kaWcgLTEKaW50Y18wIC8vIDAKZXh0cmFjdF91aW50NjQKYWRkdwpidXJ5IDEKc3RvcmVzCmZyYW1lX2RpZyAtMwppbnRjIDQgLy8gMTQ0MjY5NTA0MDg4ODk2MzQwNwppbnRjXzIgLy8gNjM2NDEzNjIyMzg0Njc5MzAwNQpmcmFtZV9kaWcgLTMKbG9hZHMKbXVsdwpidXJ5IDEKYWRkdwpidXJ5IDEKc3RvcmVzCmZyYW1lX2RpZyAtMgppbnRjXzAgLy8gMApzdG9yZXMKZnJhbWVfZGlnIC0yCmludGMgNSAvLyAxNDQyNjk1MDQwODg4OTYzNDA5CmludGNfMiAvLyA2MzY0MTM2MjIzODQ2NzkzMDA1CmZyYW1lX2RpZyAtMgpsb2FkcwptdWx3CmJ1cnkgMQphZGR3CmJ1cnkgMQpzdG9yZXMKZnJhbWVfZGlnIC0yCmZyYW1lX2RpZyAtMgpsb2FkcwpmcmFtZV9kaWcgLTEKcHVzaGludCA4IC8vIDgKZXh0cmFjdF91aW50NjQKYWRkdwpidXJ5IDEKc3RvcmVzCmZyYW1lX2RpZyAtMgppbnRjIDUgLy8gMTQ0MjY5NTA0MDg4ODk2MzQwOQppbnRjXzIgLy8gNjM2NDEzNjIyMzg0Njc5MzAwNQpmcmFtZV9kaWcgLTIKbG9hZHMKbXVsdwpidXJ5IDEKYWRkdwpidXJ5IDEKc3RvcmVzCnJldHN1YgoKLy8gcGNnNjRfcmFuZG9tCnBjZzY0cmFuZG9tXzE6CnByb3RvIDUgMQppbnRjXzAgLy8gMApmcmFtZV9kaWcgLTEKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCnB1c2hpbnQgNjU1MzYgLy8gNjU1MzYKPAphc3NlcnQKZnJhbWVfZGlnIDAKaXRvYgpleHRyYWN0IDYgMApzdG9yZSA0CmZyYW1lX2RpZyAtMwppbnRjXzAgLy8gMAo9PQpmcmFtZV9kaWcgLTIKaW50Y18wIC8vIDAKPT0KJiYKYm56IHBjZzY0cmFuZG9tXzFfbDEwCmZyYW1lX2RpZyAtMgppbnRjXzAgLy8gMAohPQpibnogcGNnNjRyYW5kb21fMV9sOQpmcmFtZV9kaWcgLTMKcHVzaGludCAxODQ0Njc0NDA3MzcwOTU1MTYxNSAvLyAxODQ0Njc0NDA3MzcwOTU1MTYxNQo8CmFzc2VydApwdXNoYnl0ZXMgMHgwMTAwMDAwMDAwMDAwMDAwMDAgLy8gMHgwMTAwMDAwMDAwMDAwMDAwMDAKZnJhbWVfZGlnIC0zCml0b2IKYi0KYnRvaQpzdG9yZSAyCnBjZzY0cmFuZG9tXzFfbDM6CmxvYWQgMgp+CmludGNfMSAvLyAxCmFkZHcKYnVyeSAxCmxvYWQgMgolCnN0b3JlIDMKaW50Y18wIC8vIDAKc3RvcmUgNQpwY2c2NHJhbmRvbV8xX2w0Ogpsb2FkIDUKZnJhbWVfZGlnIC0xCjwKYnogcGNnNjRyYW5kb21fMV9sMTMKZnJhbWVfZGlnIC01CmZyYW1lX2RpZyAtNApjYWxsc3ViIHBjZzY0dW5ib3VuZGVkcmFuZG9tXzIKc3RvcmUgNgpwY2c2NHJhbmRvbV8xX2w2Ogpsb2FkIDYKbG9hZCAzCjwKYm56IHBjZzY0cmFuZG9tXzFfbDgKbG9hZCA0CmxvYWQgNgpsb2FkIDIKJQpmcmFtZV9kaWcgLTMKKwppdG9iCmNvbmNhdApzdG9yZSA0CmxvYWQgNQppbnRjXzEgLy8gMQorCnN0b3JlIDUKYiBwY2c2NHJhbmRvbV8xX2w0CnBjZzY0cmFuZG9tXzFfbDg6CmZyYW1lX2RpZyAtNQpmcmFtZV9kaWcgLTQKY2FsbHN1YiBwY2c2NHVuYm91bmRlZHJhbmRvbV8yCnN0b3JlIDYKYiBwY2c2NHJhbmRvbV8xX2w2CnBjZzY0cmFuZG9tXzFfbDk6CmZyYW1lX2RpZyAtMgppbnRjXzEgLy8gMQo+CmFzc2VydApmcmFtZV9kaWcgLTMKZnJhbWVfZGlnIC0yCmludGNfMSAvLyAxCi0KPAphc3NlcnQKZnJhbWVfZGlnIC0yCmZyYW1lX2RpZyAtMwotCnN0b3JlIDIKYiBwY2c2NHJhbmRvbV8xX2wzCnBjZzY0cmFuZG9tXzFfbDEwOgppbnRjXzAgLy8gMApzdG9yZSA1CnBjZzY0cmFuZG9tXzFfbDExOgpsb2FkIDUKZnJhbWVfZGlnIC0xCjwKYnogcGNnNjRyYW5kb21fMV9sMTMKbG9hZCA0CmZyYW1lX2RpZyAtNQpmcmFtZV9kaWcgLTQKY2FsbHN1YiBwY2c2NHVuYm91bmRlZHJhbmRvbV8yCml0b2IKY29uY2F0CnN0b3JlIDQKbG9hZCA1CmludGNfMSAvLyAxCisKc3RvcmUgNQpiIHBjZzY0cmFuZG9tXzFfbDExCnBjZzY0cmFuZG9tXzFfbDEzOgpsb2FkIDQKZnJhbWVfYnVyeSAwCnJldHN1YgoKLy8gX19wY2c2NF91bmJvdW5kZWRfcmFuZG9tCnBjZzY0dW5ib3VuZGVkcmFuZG9tXzI6CnByb3RvIDIgMQpmcmFtZV9kaWcgLTIKbG9hZHMKc3RvcmUgNwpmcmFtZV9kaWcgLTEKbG9hZHMKc3RvcmUgOApmcmFtZV9kaWcgLTIKaW50YyA0IC8vIDE0NDI2OTUwNDA4ODg5NjM0MDcKaW50Y18yIC8vIDYzNjQxMzYyMjM4NDY3OTMwMDUKZnJhbWVfZGlnIC0yCmxvYWRzCm11bHcKYnVyeSAxCmFkZHcKYnVyeSAxCnN0b3JlcwpmcmFtZV9kaWcgLTEKaW50YyA1IC8vIDE0NDI2OTUwNDA4ODg5NjM0MDkKZnJhbWVfZGlnIC0yCmxvYWRzCmludGNfMCAvLyAwCj09CnNobAppbnRjXzIgLy8gNjM2NDEzNjIyMzg0Njc5MzAwNQpmcmFtZV9kaWcgLTEKbG9hZHMKbXVsdwpidXJ5IDEKYWRkdwpidXJ5IDEKc3RvcmVzCmxvYWQgNwpwdXNoaW50IDE4IC8vIDE4CnNocgpsb2FkIDcKXgpwdXNoaW50IDI3IC8vIDI3CnNocgppbnRjXzMgLy8gNDI5NDk2NzI5NQomCnN0b3JlIDkKbG9hZCA3CnB1c2hpbnQgNTkgLy8gNTkKc2hyCnN0b3JlIDEwCmxvYWQgOQpsb2FkIDEwCnNocgpsb2FkIDkKbG9hZCAxMAp+CmludGNfMSAvLyAxCmFkZHcKYnVyeSAxCnB1c2hpbnQgMzEgLy8gMzEKJgpzaGwKaW50Y18zIC8vIDQyOTQ5NjcyOTUKJgp8CnB1c2hpbnQgMzIgLy8gMzIKc2hsCmxvYWQgOApwdXNoaW50IDE4IC8vIDE4CnNocgpsb2FkIDgKXgpwdXNoaW50IDI3IC8vIDI3CnNocgppbnRjXzMgLy8gNDI5NDk2NzI5NQomCnN0b3JlIDExCmxvYWQgOApwdXNoaW50IDU5IC8vIDU5CnNocgpzdG9yZSAxMgpsb2FkIDExCmxvYWQgMTIKc2hyCmxvYWQgMTEKbG9hZCAxMgp+CmludGNfMSAvLyAxCmFkZHcKYnVyeSAxCnB1c2hpbnQgMzEgLy8gMzEKJgpzaGwKaW50Y18zIC8vIDQyOTQ5NjcyOTUKJgp8CnwKcmV0c3ViCgovLyB1cGRhdGUKdXBkYXRlXzM6CnByb3RvIDAgMAp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CnB1c2hpbnQgVE1QTF9VUERBVEFCTEUgLy8gVE1QTF9VUERBVEFCTEUKLy8gQ2hlY2sgYXBwIGlzIHVwZGF0YWJsZQphc3NlcnQKcmV0c3ViCgovLyBkZWxldGUKZGVsZXRlXzQ6CnByb3RvIDAgMAp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CnB1c2hpbnQgVE1QTF9ERUxFVEFCTEUgLy8gVE1QTF9ERUxFVEFCTEUKLy8gQ2hlY2sgYXBwIGlzIGRlbGV0YWJsZQphc3NlcnQKcmV0c3ViCgovLyBib3VuZGVkX3JhbmRfdWludDY0CmJvdW5kZWRyYW5kdWludDY0XzU6CnByb3RvIDQgMQpieXRlY18wIC8vICIiCmludGNfMCAvLyAwCmludGNfMSAvLyAxCmZyYW1lX2RpZyAtNApjYWxsc3ViIHBjZzY0aW5pdF8wCmludGNfMCAvLyAwCmludGNfMSAvLyAxCmZyYW1lX2RpZyAtMwpmcmFtZV9kaWcgLTIKZnJhbWVfZGlnIC0xCmNhbGxzdWIgcGNnNjRyYW5kb21fMQpmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBib3VuZGVkX3JhbmRfdWludDY0X2Nhc3Rlcgpib3VuZGVkcmFuZHVpbnQ2NGNhc3Rlcl82Ogpwcm90byAwIDAKYnl0ZWNfMCAvLyAiIgpkdXAKaW50Y18wIC8vIDAKZHVwbiAyCnR4bmEgQXBwbGljYXRpb25BcmdzIDEKZnJhbWVfYnVyeSAxCnR4bmEgQXBwbGljYXRpb25BcmdzIDIKYnRvaQpmcmFtZV9idXJ5IDIKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMwpidG9pCmZyYW1lX2J1cnkgMwp0eG5hIEFwcGxpY2F0aW9uQXJncyA0CmludGNfMCAvLyAwCmV4dHJhY3RfdWludDE2CmZyYW1lX2J1cnkgNApmcmFtZV9kaWcgMQpmcmFtZV9kaWcgMgpmcmFtZV9kaWcgMwpmcmFtZV9kaWcgNApjYWxsc3ViIGJvdW5kZWRyYW5kdWludDY0XzUKZnJhbWVfYnVyeSAwCnB1c2hieXRlcyAweDE1MWY3Yzc1IC8vIDB4MTUxZjdjNzUKZnJhbWVfZGlnIDAKY29uY2F0CmxvZwpyZXRzdWI=",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
    },
    "state": {
        "global": {
            "num_byte_slices": 0,
            "num_uints": 0
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {},
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "lib_pcg64_exposer_pyteal",
        "methods": [
            {
                "name": "bounded_rand_uint64",
                "args": [
                    {
                        "type": "byte[16]",
                        "name": "seed"
                    },
                    {
                        "type": "uint64",
                        "name": "lower_bound"
                    },
                    {
                        "type": "uint64",
                        "name": "upper_bound"
                    },
                    {
                        "type": "uint16",
                        "name": "length"
                    }
                ],
                "returns": {
                    "type": "uint64[]"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "delete_application": "CALL",
        "no_op": "CREATE",
        "update_application": "CALL"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data) # type: ignore[call-overload]
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class BoundedRandUint64Args(_ArgsBase[list[int]]):
    seed: bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
    lower_bound: int
    upper_bound: int
    length: int

    @staticmethod
    def method() -> str:
        return "bounded_rand_uint64(byte[16],uint64,uint64,uint16)uint64[]"


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def bounded_rand_uint64(
        self,
        *,
        seed: bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int],
        lower_bound: int,
        upper_bound: int,
        length: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `bounded_rand_uint64(byte[16],uint64,uint64,uint16)uint64[]` ABI method
        
        :param bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int] seed: The `seed` ABI parameter
        :param int lower_bound: The `lower_bound` ABI parameter
        :param int upper_bound: The `upper_bound` ABI parameter
        :param int length: The `length` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = BoundedRandUint64Args(
            seed=seed,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            length=length,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def update_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a calls to the update_application bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_update(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return self

    def delete_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a calls to the delete_application bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_delete(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class LibPcg64ExposerPytealClient:
    """A class for interacting with the lib_pcg64_exposer_pyteal app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        LibPcg64ExposerPytealClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def bounded_rand_uint64(
        self,
        *,
        seed: bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int],
        lower_bound: int,
        upper_bound: int,
        length: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[list[int]]:
        """Calls `bounded_rand_uint64(byte[16],uint64,uint64,uint16)uint64[]` ABI method
        
        :param bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int] seed: The `seed` ABI parameter
        :param int lower_bound: The `lower_bound` ABI parameter
        :param int upper_bound: The `upper_bound` ABI parameter
        :param int length: The `length` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[list[int]]: The result of the transaction"""

        args = BoundedRandUint64Args(
            seed=seed,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            length=length,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def update_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the update_application bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.update(
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return result

    def delete_bare(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the delete_application bare method
        
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.delete(
            call_abi_method=False,
            transaction_parameters=_convert_transaction_parameters(transaction_parameters),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())
