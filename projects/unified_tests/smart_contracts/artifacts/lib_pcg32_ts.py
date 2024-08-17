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
        "createApplication()void": {
            "call_config": {
                "no_op": "CREATE"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgovLyBUaGlzIFRFQUwgd2FzIGdlbmVyYXRlZCBieSBURUFMU2NyaXB0IHYwLjg4LjEKLy8gaHR0cHM6Ly9naXRodWIuY29tL2FsZ29yYW5kZm91bmRhdGlvbi9URUFMU2NyaXB0CgovLyBUaGlzIGNvbnRyYWN0IGlzIGNvbXBsaWFudCB3aXRoIGFuZC9vciBpbXBsZW1lbnRzIHRoZSBmb2xsb3dpbmcgQVJDczogWyBBUkM0IF0KCi8vIFRoZSBmb2xsb3dpbmcgdGVuIGxpbmVzIG9mIFRFQUwgaGFuZGxlIGluaXRpYWwgcHJvZ3JhbSBmbG93Ci8vIFRoaXMgcGF0dGVybiBpcyB1c2VkIHRvIG1ha2UgaXQgZWFzeSBmb3IgYW55b25lIHRvIHBhcnNlIHRoZSBzdGFydCBvZiB0aGUgcHJvZ3JhbSBhbmQgZGV0ZXJtaW5lIGlmIGEgc3BlY2lmaWMgYWN0aW9uIGlzIGFsbG93ZWQKLy8gSGVyZSwgYWN0aW9uIHJlZmVycyB0byB0aGUgT25Db21wbGV0ZSBpbiBjb21iaW5hdGlvbiB3aXRoIHdoZXRoZXIgdGhlIGFwcCBpcyBiZWluZyBjcmVhdGVkIG9yIGNhbGxlZAovLyBFdmVyeSBwb3NzaWJsZSBhY3Rpb24gZm9yIHRoaXMgY29udHJhY3QgaXMgcmVwcmVzZW50ZWQgaW4gdGhlIHN3aXRjaCBzdGF0ZW1lbnQKLy8gSWYgdGhlIGFjdGlvbiBpcyBub3QgaW1wbGVtZW50ZWQgaW4gdGhlIGNvbnRyYWN0LCBpdHMgcmVzcGVjdGl2ZSBicmFuY2ggd2lsbCBiZSAiKk5PVF9JTVBMRU1FTlRFRCIgd2hpY2gganVzdCBjb250YWlucyAiZXJyIgp0eG4gQXBwbGljYXRpb25JRAohCmludCA2CioKdHhuIE9uQ29tcGxldGlvbgorCnN3aXRjaCAqTk9UX0lNUExFTUVOVEVEICpOT1RfSU1QTEVNRU5URUQgKk5PVF9JTVBMRU1FTlRFRCAqTk9UX0lNUExFTUVOVEVEICpOT1RfSU1QTEVNRU5URUQgKk5PVF9JTVBMRU1FTlRFRCAqY3JlYXRlX05vT3AgKk5PVF9JTVBMRU1FTlRFRCAqTk9UX0lNUExFTUVOVEVEICpOT1RfSU1QTEVNRU5URUQgKk5PVF9JTVBMRU1FTlRFRCAqTk9UX0lNUExFTUVOVEVECgoqTk9UX0lNUExFTUVOVEVEOgoJZXJyCgovLyBfX3R3b3NDb21wbGVtZW50KHZhbHVlOiB1aW50NjQpOiB1aW50NjQKX190d29zQ29tcGxlbWVudDoKCXByb3RvIDEgMQoKCS8vIFB1c2ggZW1wdHkgYnl0ZXMgYWZ0ZXIgdGhlIGZyYW1lIHBvaW50ZXIgdG8gcmVzZXJ2ZSBzcGFjZSBmb3IgbG9jYWwgdmFyaWFibGVzCglieXRlIDB4CglkdXBuIDMKCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NgoJLy8gYWRkd1Jlc3VsdCA9IGFkZHcofnZhbHVlLCAxKQoJZnJhbWVfZGlnIC0xIC8vIHZhbHVlOiB1aW50NjQKCX4KCWludCAxCglhZGR3CglmcmFtZV9idXJ5IDIgLy8gYWRkd1Jlc3VsdCBsb3c6IHVpbnQ2NAoJZnJhbWVfYnVyeSAzIC8vIGFkZHdSZXN1bHQgaGlnaDogdWludDY0CgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjcKCS8vIHJldHVybiBhZGR3UmVzdWx0LmxvdzsKCWZyYW1lX2RpZyAyIC8vIGFkZHdSZXN1bHQgbG93OiB1aW50NjQKCgkvLyBzZXQgdGhlIHN1YnJvdXRpbmUgcmV0dXJuIHZhbHVlCglmcmFtZV9idXJ5IDAKCgkvLyBwb3AgYWxsIGxvY2FsIHZhcmlhYmxlcyBmcm9tIHRoZSBzdGFjawoJcG9wbiAzCglyZXRzdWIKCi8vIF9fbWFza1RvVWludDMyKHZhbHVlOiB1aW50NjQpOiB1aW50NjQKX19tYXNrVG9VaW50MzI6Cglwcm90byAxIDEKCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6MTEKCS8vIHJldHVybiB2YWx1ZSAmIDQyOTQ5NjcyOTU7CglmcmFtZV9kaWcgLTEgLy8gdmFsdWU6IHVpbnQ2NAoJaW50IDQyOTQ5NjcyOTUKCSYKCXJldHN1YgoKLy8gX19wY2czMlN0ZXAoc3RhdGU6IHVpbnQ2NCwgaW5jcjogdWludDY0KTogdWludDY0Cl9fcGNnMzJTdGVwOgoJcHJvdG8gMiAxCgoJLy8gUHVzaCBlbXB0eSBieXRlcyBhZnRlciB0aGUgZnJhbWUgcG9pbnRlciB0byByZXNlcnZlIHNwYWNlIGZvciBsb2NhbCB2YXJpYWJsZXMKCWJ5dGUgMHgKCWR1cG4gNwoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czoxNQoJLy8gbXVsd1Jlc3VsdCA9IG11bHcoc3RhdGUsIDYzNjQxMzYyMjM4NDY3OTMwMDUpCglmcmFtZV9kaWcgLTEgLy8gc3RhdGU6IHVpbnQ2NAoJaW50IDYzNjQxMzYyMjM4NDY3OTMwMDUKCW11bHcKCWZyYW1lX2J1cnkgMiAvLyBtdWx3UmVzdWx0IGxvdzogdWludDY0CglmcmFtZV9idXJ5IDMgLy8gbXVsd1Jlc3VsdCBoaWdoOiB1aW50NjQKCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6MTYKCS8vIGFkZHdSZXN1bHQgPSBhZGR3KG11bHdSZXN1bHQubG93LCBpbmNyKQoJZnJhbWVfZGlnIDIgLy8gbXVsd1Jlc3VsdCBsb3c6IHVpbnQ2NAoJZnJhbWVfZGlnIC0yIC8vIGluY3I6IHVpbnQ2NAoJYWRkdwoJZnJhbWVfYnVyeSA2IC8vIGFkZHdSZXN1bHQgbG93OiB1aW50NjQKCWZyYW1lX2J1cnkgNyAvLyBhZGR3UmVzdWx0IGhpZ2g6IHVpbnQ2NAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czoxOAoJLy8gcmV0dXJuIGFkZHdSZXN1bHQubG93OwoJZnJhbWVfZGlnIDYgLy8gYWRkd1Jlc3VsdCBsb3c6IHVpbnQ2NAoKCS8vIHNldCB0aGUgc3Vicm91dGluZSByZXR1cm4gdmFsdWUKCWZyYW1lX2J1cnkgMAoKCS8vIHBvcCBhbGwgbG9jYWwgdmFyaWFibGVzIGZyb20gdGhlIHN0YWNrCglwb3BuIDcKCXJldHN1YgoKLy8gX19wY2czMlJvdGF0aW9uKHZhbHVlOiB1aW50NjQsIHJvdDogdWludDY0KTogdWludDY0Cl9fcGNnMzJSb3RhdGlvbjoKCXByb3RvIDIgMQoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czoyMgoJLy8gcmV0dXJuICh2YWx1ZSA+PiByb3QpIHwgdGhpcy5fX21hc2tUb1VpbnQzMih2YWx1ZSA8PCAodGhpcy5fX3R3b3NDb21wbGVtZW50KHJvdCkgJiAzMSkpOwoJZnJhbWVfZGlnIC0xIC8vIHZhbHVlOiB1aW50NjQKCWZyYW1lX2RpZyAtMiAvLyByb3Q6IHVpbnQ2NAoJc2hyCglmcmFtZV9kaWcgLTEgLy8gdmFsdWU6IHVpbnQ2NAoJZnJhbWVfZGlnIC0yIC8vIHJvdDogdWludDY0CgljYWxsc3ViIF9fdHdvc0NvbXBsZW1lbnQKCWludCAzMQoJJgoJc2hsCgljYWxsc3ViIF9fbWFza1RvVWludDMyCgl8CglyZXRzdWIKCi8vIF9fcGNnMzJPdXRwdXQoc3RhdGU6IHVpbnQ2NCk6IHVpbnQ2NApfX3BjZzMyT3V0cHV0OgoJcHJvdG8gMSAxCgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjI2CgkvLyByZXR1cm4gdGhpcy5fX3BjZzMyUm90YXRpb24odGhpcy5fX21hc2tUb1VpbnQzMigoKHN0YXRlID4+IDE4KSBeIHN0YXRlKSA+PiAyNyksIHN0YXRlID4+IDU5KTsKCWZyYW1lX2RpZyAtMSAvLyBzdGF0ZTogdWludDY0CglpbnQgNTkKCXNocgoJZnJhbWVfZGlnIC0xIC8vIHN0YXRlOiB1aW50NjQKCWludCAxOAoJc2hyCglmcmFtZV9kaWcgLTEgLy8gc3RhdGU6IHVpbnQ2NAoJXgoJaW50IDI3CglzaHIKCWNhbGxzdWIgX19tYXNrVG9VaW50MzIKCWNhbGxzdWIgX19wY2czMlJvdGF0aW9uCglyZXRzdWIKCi8vIF9fcGNnMzJSYW5kb20oc3RhdGU6IHVpbnQ2NCk6IFt1aW50NjQsIHVpbnQ2NF0KX19wY2czMlJhbmRvbToKCXByb3RvIDEgMQoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czozMAoJLy8gcmV0dXJuIFt0aGlzLl9fcGNnMzJTdGVwKHN0YXRlLCAxNDQyNjk1MDQwODg4OTYzNDA3KSwgdGhpcy5fX3BjZzMyT3V0cHV0KHN0YXRlKV07CglpbnQgMTQ0MjY5NTA0MDg4ODk2MzQwNwoJZnJhbWVfZGlnIC0xIC8vIHN0YXRlOiB1aW50NjQKCWNhbGxzdWIgX19wY2czMlN0ZXAKCWl0b2IKCWZyYW1lX2RpZyAtMSAvLyBzdGF0ZTogdWludDY0CgljYWxsc3ViIF9fcGNnMzJPdXRwdXQKCWl0b2IKCWNvbmNhdAoJcmV0c3ViCgovLyBfX3BjZzMySW5pdChpbml0aWFsU3RhdGU6IHVpbnQ2NCwgaW5jcjogdWludDY0KTogdWludDY0Cl9fcGNnMzJJbml0OgoJcHJvdG8gMiAxCgoJLy8gUHVzaCBlbXB0eSBieXRlcyBhZnRlciB0aGUgZnJhbWUgcG9pbnRlciB0byByZXNlcnZlIHNwYWNlIGZvciBsb2NhbCB2YXJpYWJsZXMKCWJ5dGUgMHgKCWR1cG4gNAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czozNAoJLy8gc3RhdGUgPSB0aGlzLl9fcGNnMzJTdGVwKDAsIGluY3IpCglmcmFtZV9kaWcgLTIgLy8gaW5jcjogdWludDY0CglpbnQgMAoJY2FsbHN1YiBfX3BjZzMyU3RlcAoJZnJhbWVfYnVyeSAwIC8vIHN0YXRlOiB1aW50NjQKCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6MzUKCS8vIGFkZHdSZXN1bHQgPSBhZGR3KHN0YXRlLCBpbml0aWFsU3RhdGUpCglmcmFtZV9kaWcgMCAvLyBzdGF0ZTogdWludDY0CglmcmFtZV9kaWcgLTEgLy8gaW5pdGlhbFN0YXRlOiB1aW50NjQKCWFkZHcKCWZyYW1lX2J1cnkgMyAvLyBhZGR3UmVzdWx0IGxvdzogdWludDY0CglmcmFtZV9idXJ5IDQgLy8gYWRkd1Jlc3VsdCBoaWdoOiB1aW50NjQKCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6MzcKCS8vIHJldHVybiB0aGlzLl9fcGNnMzJTdGVwKGFkZHdSZXN1bHQubG93LCBpbmNyKTsKCWZyYW1lX2RpZyAtMiAvLyBpbmNyOiB1aW50NjQKCWZyYW1lX2RpZyAzIC8vIGFkZHdSZXN1bHQgbG93OiB1aW50NjQKCWNhbGxzdWIgX19wY2czMlN0ZXAKCgkvLyBzZXQgdGhlIHN1YnJvdXRpbmUgcmV0dXJuIHZhbHVlCglmcmFtZV9idXJ5IDAKCgkvLyBwb3AgYWxsIGxvY2FsIHZhcmlhYmxlcyBmcm9tIHRoZSBzdGFjawoJcG9wbiA0CglyZXRzdWIKCi8vIHBjZzMySW5pdChpbml0aWFsU3RhdGU6IHVpbnQ2NCk6IHVpbnQ2NApwY2czMkluaXQ6Cglwcm90byAxIDEKCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NDEKCS8vIHJldHVybiB0aGlzLl9fcGNnMzJJbml0KGluaXRpYWxTdGF0ZSwgMTQ0MjY5NTA0MDg4ODk2MzQwNyk7CglpbnQgMTQ0MjY5NTA0MDg4ODk2MzQwNwoJZnJhbWVfZGlnIC0xIC8vIGluaXRpYWxTdGF0ZTogdWludDY0CgljYWxsc3ViIF9fcGNnMzJJbml0CglyZXRzdWIKCi8vIHBjZzMyUmFuZG9tKHN0YXRlOiB1aW50NjQsIGJpdFNpemU6IHVpbnQ2NCwgbG93ZXJCb3VuZDogdWludDY0LCB1cHBlckJvdW5kOiB1aW50NjQsIGxlbmd0aDogdWludDY0KTogW3VpbnQ2NCwgYnl0ZXNdCnBjZzMyUmFuZG9tOgoJcHJvdG8gNSAxCgoJLy8gUHVzaCBlbXB0eSBieXRlcyBhZnRlciB0aGUgZnJhbWUgcG9pbnRlciB0byByZXNlcnZlIHNwYWNlIGZvciBsb2NhbCB2YXJpYWJsZXMKCWJ5dGUgMHgKCWR1cG4gOAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo1MQoJLy8gcmVzdWx0OiBieXRlcyA9ICcnCglieXRlIDB4IC8vICIiCglmcmFtZV9idXJ5IDAgLy8gcmVzdWx0OiBieXRlcwoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo1NQoJLy8gYXNzZXJ0KGxlbmd0aCA8IDY1NTM2KQoJZnJhbWVfZGlnIC01IC8vIGxlbmd0aDogdWludDY0CglpbnQgNjU1MzYKCTwKCWFzc2VydAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo1NwoJLy8gYXNzZXJ0KGJpdFNpemUgPT09IDggfHwgYml0U2l6ZSA9PT0gMTYgfHwgYml0U2l6ZSA9PT0gMzIpCglmcmFtZV9kaWcgLTIgLy8gYml0U2l6ZTogdWludDY0CglpbnQgOAoJPT0KCWR1cAoJYm56ICpza2lwX29yMAoJZnJhbWVfZGlnIC0yIC8vIGJpdFNpemU6IHVpbnQ2NAoJaW50IDE2Cgk9PQoJfHwKCipza2lwX29yMDoKCWR1cAoJYm56ICpza2lwX29yMQoJZnJhbWVfZGlnIC0yIC8vIGJpdFNpemU6IHVpbnQ2NAoJaW50IDMyCgk9PQoJfHwKCipza2lwX29yMToKCWFzc2VydAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo1OAoJLy8gYnl0ZVNpemUgPSBiaXRTaXplID4+IDMKCWZyYW1lX2RpZyAtMiAvLyBiaXRTaXplOiB1aW50NjQKCWludCAzCglzaHIKCWZyYW1lX2J1cnkgMyAvLyBieXRlU2l6ZTogdWludDY0CgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjU5CgkvLyB0cnVuY2F0ZVN0YXJ0Q2FjaGVkID0gOCAtIGJ5dGVTaXplCglpbnQgOAoJZnJhbWVfZGlnIDMgLy8gYnl0ZVNpemU6IHVpbnQ2NAoJLQoJZnJhbWVfYnVyeSA0IC8vIHRydW5jYXRlU3RhcnRDYWNoZWQ6IHVpbnQ2NAoKCS8vICppZjBfY29uZGl0aW9uCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NjEKCS8vIGxvd2VyQm91bmQgPT09IDAgJiYgdXBwZXJCb3VuZCA9PT0gMAoJZnJhbWVfZGlnIC0zIC8vIGxvd2VyQm91bmQ6IHVpbnQ2NAoJaW50IDAKCT09CglkdXAKCWJ6ICpza2lwX2FuZDAKCWZyYW1lX2RpZyAtNCAvLyB1cHBlckJvdW5kOiB1aW50NjQKCWludCAwCgk9PQoJJiYKCipza2lwX2FuZDA6CglieiAqaWYwX2Vsc2UKCgkvLyAqaWYwX2NvbnNlcXVlbnQKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo2MgoJLy8gZm9yIChsZXQgaSA9IDA7IGkgPCBsZW5ndGg7IGkgPSBpICsgMSkKCWludCAwCglmcmFtZV9idXJ5IDUgLy8gaTogdWludDY0CgoqZm9yXzA6CgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NjIKCS8vIGkgPCBsZW5ndGgKCWZyYW1lX2RpZyA1IC8vIGk6IHVpbnQ2NAoJZnJhbWVfZGlnIC01IC8vIGxlbmd0aDogdWludDY0Cgk8CglieiAqZm9yXzBfZW5kCgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjYzCgkvLyBwcm4gPSB0aGlzLl9fcGNnMzJSYW5kb20oc3RhdGUpCglmcmFtZV9kaWcgLTEgLy8gc3RhdGU6IHVpbnQ2NAoJY2FsbHN1YiBfX3BjZzMyUmFuZG9tCglmcmFtZV9idXJ5IDYgLy8gcHJuOiAodWludDY0LHVpbnQ2NCkKCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NjQKCS8vIHN0YXRlID0gcHJuWzBdCglmcmFtZV9kaWcgNiAvLyBwcm46ICh1aW50NjQsdWludDY0KQoJZXh0cmFjdCAwIDgKCWJ0b2kKCWZyYW1lX2J1cnkgLTEgLy8gc3RhdGU6IHVpbnQ2NAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo2NQoJLy8gcmVzdWx0ICs9IGV4dHJhY3QzKGl0b2IocHJuWzFdKSwgdHJ1bmNhdGVTdGFydENhY2hlZCwgYnl0ZVNpemUpCglmcmFtZV9kaWcgMCAvLyByZXN1bHQ6IGJ5dGVzCglmcmFtZV9kaWcgNiAvLyBwcm46ICh1aW50NjQsdWludDY0KQoJZXh0cmFjdCA4IDgKCWJ0b2kKCWl0b2IKCWZyYW1lX2RpZyA0IC8vIHRydW5jYXRlU3RhcnRDYWNoZWQ6IHVpbnQ2NAoJZnJhbWVfZGlnIDMgLy8gYnl0ZVNpemU6IHVpbnQ2NAoJZXh0cmFjdDMKCWNvbmNhdAoJZnJhbWVfYnVyeSAwIC8vIHJlc3VsdDogYnl0ZXMKCipmb3JfMF9jb250aW51ZToKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo2MgoJLy8gaSA9IGkgKyAxCglmcmFtZV9kaWcgNSAvLyBpOiB1aW50NjQKCWludCAxCgkrCglmcmFtZV9idXJ5IDUgLy8gaTogdWludDY0CgliICpmb3JfMAoKKmZvcl8wX2VuZDoKCWIgKmlmMF9lbmQKCippZjBfZWxzZToKCS8vICppZjFfY29uZGl0aW9uCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NjgKCS8vIHVwcGVyQm91bmQgIT09IDAKCWZyYW1lX2RpZyAtNCAvLyB1cHBlckJvdW5kOiB1aW50NjQKCWludCAwCgkhPQoJYnogKmlmMV9lbHNlCgoJLy8gKmlmMV9jb25zZXF1ZW50CgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NjkKCS8vIGFzc2VydCh1cHBlckJvdW5kID4gMSkKCWZyYW1lX2RpZyAtNCAvLyB1cHBlckJvdW5kOiB1aW50NjQKCWludCAxCgk+Cglhc3NlcnQKCgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NzAKCS8vIGFzc2VydCh1cHBlckJvdW5kIDwgMSA8PCBiaXRTaXplKQoJZnJhbWVfZGlnIC00IC8vIHVwcGVyQm91bmQ6IHVpbnQ2NAoJaW50IDEKCWZyYW1lX2RpZyAtMiAvLyBiaXRTaXplOiB1aW50NjQKCXNobAoJPAoJYXNzZXJ0CgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjcyCgkvLyBhc3NlcnQobG93ZXJCb3VuZCA8IHVwcGVyQm91bmQgLSAxKQoJZnJhbWVfZGlnIC0zIC8vIGxvd2VyQm91bmQ6IHVpbnQ2NAoJZnJhbWVfZGlnIC00IC8vIHVwcGVyQm91bmQ6IHVpbnQ2NAoJaW50IDEKCS0KCTwKCWFzc2VydAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo3NAoJLy8gYWJzb2x1dGVCb3VuZCA9IHVwcGVyQm91bmQgLSBsb3dlckJvdW5kCglmcmFtZV9kaWcgLTQgLy8gdXBwZXJCb3VuZDogdWludDY0CglmcmFtZV9kaWcgLTMgLy8gbG93ZXJCb3VuZDogdWludDY0CgktCglmcmFtZV9idXJ5IDEgLy8gYWJzb2x1dGVCb3VuZDogdWludDY0CgliICppZjFfZW5kCgoqaWYxX2Vsc2U6CgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6NzYKCS8vIGFzc2VydChsb3dlckJvdW5kIDwgKDEgPDwgYml0U2l6ZSkgLSAxKQoJZnJhbWVfZGlnIC0zIC8vIGxvd2VyQm91bmQ6IHVpbnQ2NAoJaW50IDEKCWZyYW1lX2RpZyAtMiAvLyBiaXRTaXplOiB1aW50NjQKCXNobAoJaW50IDEKCS0KCTwKCWFzc2VydAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo3OAoJLy8gYWJzb2x1dGVCb3VuZCA9ICgxIDw8IGJpdFNpemUpIC0gbG93ZXJCb3VuZAoJaW50IDEKCWZyYW1lX2RpZyAtMiAvLyBiaXRTaXplOiB1aW50NjQKCXNobAoJZnJhbWVfZGlnIC0zIC8vIGxvd2VyQm91bmQ6IHVpbnQ2NAoJLQoJZnJhbWVfYnVyeSAxIC8vIGFic29sdXRlQm91bmQ6IHVpbnQ2NAoKKmlmMV9lbmQ6CgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6ODEKCS8vIHRocmVzaG9sZCA9IHRoaXMuX19tYXNrVG9VaW50MzIodGhpcy5fX3R3b3NDb21wbGVtZW50KGFic29sdXRlQm91bmQpKSAlIGFic29sdXRlQm91bmQKCWZyYW1lX2RpZyAxIC8vIGFic29sdXRlQm91bmQ6IHVpbnQ2NAoJY2FsbHN1YiBfX3R3b3NDb21wbGVtZW50CgljYWxsc3ViIF9fbWFza1RvVWludDMyCglmcmFtZV9kaWcgMSAvLyBhYnNvbHV0ZUJvdW5kOiB1aW50NjQKCSUKCWZyYW1lX2J1cnkgMiAvLyB0aHJlc2hvbGQ6IHVpbnQ2NAoKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo4MwoJLy8gZm9yIChsZXQgaSA9IDA7IGkgPCBsZW5ndGg7IGkgPSBpICsgMSkKCWludCAwCglmcmFtZV9idXJ5IDcgLy8gaTogdWludDY0CgoqZm9yXzE6CgkvLyBjb250cmFjdHNcbGliLXBjZzMyLXRzLmFsZ28udHM6ODMKCS8vIGkgPCBsZW5ndGgKCWZyYW1lX2RpZyA3IC8vIGk6IHVpbnQ2NAoJZnJhbWVfZGlnIC01IC8vIGxlbmd0aDogdWludDY0Cgk8CglieiAqZm9yXzFfZW5kCgoqd2hpbGVfMDoKCip3aGlsZV8wX2NvbnRpbnVlOgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjg2CgkvLyB0cnVlCglpbnQgMQoJYnogKndoaWxlXzBfZW5kCgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjg3CgkvLyBwcm4gPSB0aGlzLl9fcGNnMzJSYW5kb20oc3RhdGUpCglmcmFtZV9kaWcgLTEgLy8gc3RhdGU6IHVpbnQ2NAoJY2FsbHN1YiBfX3BjZzMyUmFuZG9tCglmcmFtZV9idXJ5IDggLy8gcHJuOiBbdWludDY0LCB1aW50NjRdCgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjg4CgkvLyBzdGF0ZSA9IHByblswXQoJZnJhbWVfZGlnIDggLy8gcHJuOiBbdWludDY0LCB1aW50NjRdCglleHRyYWN0IDAgOAoJYnRvaQoJZnJhbWVfYnVyeSAtMSAvLyBzdGF0ZTogdWludDY0CgoJLy8gKmlmMl9jb25kaXRpb24KCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo4OQoJLy8gcHJuWzFdID49IHRocmVzaG9sZAoJZnJhbWVfZGlnIDggLy8gcHJuOiBbdWludDY0LCB1aW50NjRdCglleHRyYWN0IDggOAoJYnRvaQoJZnJhbWVfZGlnIDIgLy8gdGhyZXNob2xkOiB1aW50NjQKCT49CglieiAqaWYyX2VuZAoKCS8vICppZjJfY29uc2VxdWVudAoJYiAqd2hpbGVfMF9lbmQKCippZjJfZW5kOgoJYiAqd2hpbGVfMAoKKndoaWxlXzBfZW5kOgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjk0CgkvLyByZXN1bHQgKz0gZXh0cmFjdDMoaXRvYigocHJuWzFdICUgYWJzb2x1dGVCb3VuZCkgKyBsb3dlckJvdW5kKSwgdHJ1bmNhdGVTdGFydENhY2hlZCwgYnl0ZVNpemUpCglmcmFtZV9kaWcgMCAvLyByZXN1bHQ6IGJ5dGVzCglmcmFtZV9kaWcgOCAvLyBwcm46IFt1aW50NjQsIHVpbnQ2NF0KCWV4dHJhY3QgOCA4CglidG9pCglmcmFtZV9kaWcgMSAvLyBhYnNvbHV0ZUJvdW5kOiB1aW50NjQKCSUKCWZyYW1lX2RpZyAtMyAvLyBsb3dlckJvdW5kOiB1aW50NjQKCSsKCWl0b2IKCWZyYW1lX2RpZyA0IC8vIHRydW5jYXRlU3RhcnRDYWNoZWQ6IHVpbnQ2NAoJZnJhbWVfZGlnIDMgLy8gYnl0ZVNpemU6IHVpbnQ2NAoJZXh0cmFjdDMKCWNvbmNhdAoJZnJhbWVfYnVyeSAwIC8vIHJlc3VsdDogYnl0ZXMKCipmb3JfMV9jb250aW51ZToKCS8vIGNvbnRyYWN0c1xsaWItcGNnMzItdHMuYWxnby50czo4MwoJLy8gaSA9IGkgKyAxCglmcmFtZV9kaWcgNyAvLyBpOiB1aW50NjQKCWludCAxCgkrCglmcmFtZV9idXJ5IDcgLy8gaTogdWludDY0CgliICpmb3JfMQoKKmZvcl8xX2VuZDoKCippZjBfZW5kOgoJLy8gY29udHJhY3RzXGxpYi1wY2czMi10cy5hbGdvLnRzOjk4CgkvLyByZXR1cm4gW3N0YXRlLCByZXN1bHRdOwoJYnl0ZSAweCAvLyBpbml0aWFsIGhlYWQKCWJ5dGUgMHggLy8gaW5pdGlhbCB0YWlsCglieXRlIDB4MDAwYSAvLyBpbml0aWFsIGhlYWQgb2Zmc2V0CglmcmFtZV9kaWcgLTEgLy8gc3RhdGU6IHVpbnQ2NAoJaXRvYgoJY2FsbHN1YiAqcHJvY2Vzc19zdGF0aWNfdHVwbGVfZWxlbWVudAoJZnJhbWVfZGlnIDAgLy8gcmVzdWx0OiBieXRlcwoJZHVwCglsZW4KCWl0b2IKCWV4dHJhY3QgNiAyCglzd2FwCgljb25jYXQKCWNhbGxzdWIgKnByb2Nlc3NfZHluYW1pY190dXBsZV9lbGVtZW50Cglwb3AgLy8gcG9wIGhlYWQgb2Zmc2V0Cgljb25jYXQgLy8gY29uY2F0IGhlYWQgYW5kIHRhaWwKCgkvLyBzZXQgdGhlIHN1YnJvdXRpbmUgcmV0dXJuIHZhbHVlCglmcmFtZV9idXJ5IDAKCgkvLyBwb3AgYWxsIGxvY2FsIHZhcmlhYmxlcyBmcm9tIHRoZSBzdGFjawoJcG9wbiA4CglyZXRzdWIKCiphYmlfcm91dGVfY3JlYXRlQXBwbGljYXRpb246CglpbnQgMQoJcmV0dXJuCgoqY3JlYXRlX05vT3A6CgltZXRob2QgImNyZWF0ZUFwcGxpY2F0aW9uKCl2b2lkIgoJdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMAoJbWF0Y2ggKmFiaV9yb3V0ZV9jcmVhdGVBcHBsaWNhdGlvbgoJZXJyCgoqcHJvY2Vzc19zdGF0aWNfdHVwbGVfZWxlbWVudDoKCXByb3RvIDQgMwoJZnJhbWVfZGlnIC00IC8vIHR1cGxlIGhlYWQKCWZyYW1lX2RpZyAtMSAvLyBlbGVtZW50Cgljb25jYXQKCWZyYW1lX2RpZyAtMyAvLyB0dXBsZSB0YWlsCglmcmFtZV9kaWcgLTIgLy8gaGVhZCBvZmZzZXQKCXJldHN1YgoKKnByb2Nlc3NfZHluYW1pY190dXBsZV9lbGVtZW50OgoJcHJvdG8gNCAzCglmcmFtZV9kaWcgLTQgLy8gdHVwbGUgaGVhZAoJZnJhbWVfZGlnIC0yIC8vIGhlYWQgb2Zmc2V0Cgljb25jYXQKCWZyYW1lX2J1cnkgLTQgLy8gdHVwbGUgaGVhZAoJZnJhbWVfZGlnIC0xIC8vIGVsZW1lbnQKCWR1cAoJbGVuCglmcmFtZV9kaWcgLTIgLy8gaGVhZCBvZmZzZXQKCWJ0b2kKCSsKCWl0b2IKCWV4dHJhY3QgNiAyCglmcmFtZV9idXJ5IC0yIC8vIGhlYWQgb2Zmc2V0CglmcmFtZV9kaWcgLTMgLy8gdHVwbGUgdGFpbAoJc3dhcAoJY29uY2F0CglmcmFtZV9idXJ5IC0zIC8vIHR1cGxlIHRhaWwKCWZyYW1lX2RpZyAtNCAvLyB0dXBsZSBoZWFkCglmcmFtZV9kaWcgLTMgLy8gdHVwbGUgdGFpbAoJZnJhbWVfZGlnIC0yIC8vIGhlYWQgb2Zmc2V0CglyZXRzdWI=",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEw"
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
        "local": {
            "declared": {},
            "reserved": {}
        },
        "global": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "LibPcg32Ts",
        "methods": [
            {
                "name": "createApplication",
                "args": [],
                "returns": {
                    "type": "void"
                }
            }
        ],
        "networks": {},
        "desc": ""
    },
    "bare_call_config": {}
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


@dataclasses.dataclass(kw_only=True)
class DeployCreate(algokit_utils.DeployCreateCallArgs, _TArgsHolder[_TArgs], typing.Generic[_TArgs]):
    pass


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
class CreateApplicationArgs(_ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "createApplication()void"


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

    def create_create_application(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `createApplication()void` ABI method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = CreateApplicationArgs()
        self.app_client.compose_create(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
            **_as_dict(args, convert_all=True),
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


class LibPcg32TsClient:
    """A class for interacting with the LibPcg32Ts app providing high productivity and
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
        LibPcg32TsClient can be created with an app_id to interact with an existing application, alternatively
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

    def create_create_application(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `createApplication()void` ABI method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = CreateApplicationArgs()
        result = self.app_client.create(
            call_abi_method=args.method(),
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
            **_as_dict(args, convert_all=True),
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
        create_args: DeployCreate[CreateApplicationArgs],
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
        :param DeployCreate[CreateApplicationArgs] create_args: Arguments used when creating an application
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