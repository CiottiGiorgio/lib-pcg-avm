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
        "bounded_rand_uint128(byte[32],uint128,uint128,uint16)uint128[]": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMubGliX3BjZzEyOF9leHBvc2VyLmNvbnRyYWN0LkxpYlBjZzEyOEV4cG9zZXJBbGdvcHkuYXBwcm92YWxfcHJvZ3JhbToKICAgIHR4biBOdW1BcHBBcmdzCiAgICBieiBtYWluX2JhcmVfcm91dGluZ0A1CiAgICBtZXRob2QgImJvdW5kZWRfcmFuZF91aW50MTI4KGJ5dGVbMzJdLHVpbnQxMjgsdWludDEyOCx1aW50MTYpdWludDEyOFtdIgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMAogICAgbWF0Y2ggbWFpbl9ib3VuZGVkX3JhbmRfdWludDEyOF9yb3V0ZUAyCiAgICBlcnIgLy8gcmVqZWN0IHRyYW5zYWN0aW9uCgptYWluX2JvdW5kZWRfcmFuZF91aW50MTI4X3JvdXRlQDI6CiAgICB0eG4gT25Db21wbGV0aW9uCiAgICAhCiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gaXMgbm90IGNyZWF0aW5nCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAyCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAzCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyA0CiAgICBjYWxsc3ViIGJvdW5kZWRfcmFuZF91aW50MTI4CiAgICBieXRlIDB4MTUxZjdjNzUKICAgIHN3YXAKICAgIGNvbmNhdAogICAgbG9nCiAgICBpbnQgMQogICAgcmV0dXJuCgptYWluX2JhcmVfcm91dGluZ0A1OgogICAgaW50IDAKICAgIGludCA0CiAgICB0eG4gT25Db21wbGV0aW9uCiAgICBtYXRjaCBtYWluX2NyZWF0ZUA2IG1haW5fdXBkYXRlQDcKICAgIGVyciAvLyByZWplY3QgdHJhbnNhY3Rpb24KCm1haW5fY3JlYXRlQDY6CiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgIQogICAgYXNzZXJ0IC8vIGlzIGNyZWF0aW5nCiAgICBpbnQgMQogICAgcmV0dXJuCgptYWluX3VwZGF0ZUA3OgogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBpcyBub3QgY3JlYXRpbmcKICAgIGNhbGxzdWIgdXBkYXRlCiAgICBpbnQgMQogICAgcmV0dXJuCgoKLy8gc21hcnRfY29udHJhY3RzLmxpYl9wY2cxMjhfZXhwb3Nlci5jb250cmFjdC5MaWJQY2cxMjhFeHBvc2VyQWxnb3B5LmJvdW5kZWRfcmFuZF91aW50MTI4KHNlZWQ6IGJ5dGVzLCBsb3dlcl9ib3VuZDogYnl0ZXMsIHVwcGVyX2JvdW5kOiBieXRlcywgbGVuZ3RoOiBieXRlcykgLT4gYnl0ZXM6CmJvdW5kZWRfcmFuZF91aW50MTI4OgogICAgcHJvdG8gNCAxCiAgICBmcmFtZV9kaWcgLTQKICAgIGNhbGxzdWIgcGNnMTI4X2luaXQKICAgIGNvdmVyIDMKICAgIGNvdmVyIDIKICAgIHN3YXAKICAgIGZyYW1lX2RpZyAtMQogICAgYnRvaQogICAgY292ZXIgMgogICAgc3dhcAogICAgdW5jb3ZlciAzCiAgICB1bmNvdmVyIDQKICAgIGZyYW1lX2RpZyAtMwogICAgZnJhbWVfZGlnIC0yCiAgICB1bmNvdmVyIDYKICAgIGNhbGxzdWIgcGNnMTI4X3JhbmRvbQogICAgY292ZXIgNAogICAgcG9wbiA0CiAgICByZXRzdWIKCgovLyBsaWJfcGNnLnBjZzEyOC5wY2cxMjhfaW5pdChzZWVkOiBieXRlcykgLT4gdWludDY0LCB1aW50NjQsIHVpbnQ2NCwgdWludDY0OgpwY2cxMjhfaW5pdDoKICAgIHByb3RvIDEgNAogICAgZnJhbWVfZGlnIC0xCiAgICBsZW4KICAgIGludCAzMgogICAgPT0KICAgIGFzc2VydAogICAgZnJhbWVfZGlnIC0xCiAgICBpbnQgMAogICAgZXh0cmFjdF91aW50NjQKICAgIGludCAxNDQyNjk1MDQwODg4OTYzNDA3CiAgICBjYWxsc3ViIF9fcGNnMzJfaW5pdAogICAgZnJhbWVfZGlnIC0xCiAgICBpbnQgOAogICAgZXh0cmFjdF91aW50NjQKICAgIGludCAxNDQyNjk1MDQwODg4OTYzNDA5CiAgICBjYWxsc3ViIF9fcGNnMzJfaW5pdAogICAgZnJhbWVfZGlnIC0xCiAgICBpbnQgMTYKICAgIGV4dHJhY3RfdWludDY0CiAgICBpbnQgMTQ0MjY5NTA0MDg4ODk2MzQxMQogICAgY2FsbHN1YiBfX3BjZzMyX2luaXQKICAgIGZyYW1lX2RpZyAtMQogICAgaW50IDI0CiAgICBleHRyYWN0X3VpbnQ2NAogICAgaW50IDE0NDI2OTUwNDA4ODg5NjM0MTMKICAgIGNhbGxzdWIgX19wY2czMl9pbml0CiAgICByZXRzdWIKCgovLyBsaWJfcGNnLnBjZzMyLl9fcGNnMzJfaW5pdChpbml0aWFsX3N0YXRlOiB1aW50NjQsIGluY3I6IHVpbnQ2NCkgLT4gdWludDY0OgpfX3BjZzMyX2luaXQ6CiAgICBwcm90byAyIDEKICAgIGludCAwCiAgICBmcmFtZV9kaWcgLTEKICAgIGNhbGxzdWIgX19wY2czMl9zdGVwCiAgICBmcmFtZV9kaWcgLTIKICAgIGFkZHcKICAgIGJ1cnkgMQogICAgZnJhbWVfZGlnIC0xCiAgICBjYWxsc3ViIF9fcGNnMzJfc3RlcAogICAgcmV0c3ViCgoKLy8gbGliX3BjZy5wY2czMi5fX3BjZzMyX3N0ZXAoc3RhdGU6IHVpbnQ2NCwgaW5jcjogdWludDY0KSAtPiB1aW50NjQ6Cl9fcGNnMzJfc3RlcDoKICAgIHByb3RvIDIgMQogICAgZnJhbWVfZGlnIC0yCiAgICBpbnQgNjM2NDEzNjIyMzg0Njc5MzAwNQogICAgbXVsdwogICAgYnVyeSAxCiAgICBmcmFtZV9kaWcgLTEKICAgIGFkZHcKICAgIGJ1cnkgMQogICAgcmV0c3ViCgoKLy8gbGliX3BjZy5wY2cxMjgucGNnMTI4X3JhbmRvbShzdGF0ZS4wOiB1aW50NjQsIHN0YXRlLjE6IHVpbnQ2NCwgc3RhdGUuMjogdWludDY0LCBzdGF0ZS4zOiB1aW50NjQsIGxvd2VyX2JvdW5kOiBieXRlcywgdXBwZXJfYm91bmQ6IGJ5dGVzLCBsZW5ndGg6IHVpbnQ2NCkgLT4gdWludDY0LCB1aW50NjQsIHVpbnQ2NCwgdWludDY0LCBieXRlczoKcGNnMTI4X3JhbmRvbToKICAgIHByb3RvIDcgNQogICAgaW50IDAKICAgIGR1cG4gMgogICAgYnl0ZSAiIgogICAgYnl0ZSAweDAwMDAKICAgIGZyYW1lX2RpZyAtMwogICAgYnl0ZSAweAogICAgYj09CiAgICBieiBwY2cxMjhfcmFuZG9tX2Vsc2VfYm9keUA3CiAgICBmcmFtZV9kaWcgLTIKICAgIGJ5dGUgMHgKICAgIGI9PQogICAgYnogcGNnMTI4X3JhbmRvbV9lbHNlX2JvZHlANwogICAgaW50IDAKICAgIGZyYW1lX2J1cnkgMwoKcGNnMTI4X3JhbmRvbV9mb3JfaGVhZGVyQDM6CiAgICBmcmFtZV9kaWcgMwogICAgZnJhbWVfZGlnIC0xCiAgICA8CiAgICBieiBwY2cxMjhfcmFuZG9tX2FmdGVyX2lmX2Vsc2VAMjAKICAgIGZyYW1lX2RpZyAtNwogICAgZnJhbWVfZGlnIC02CiAgICBmcmFtZV9kaWcgLTUKICAgIGZyYW1lX2RpZyAtNAogICAgY2FsbHN1YiBfX3BjZzEyOF91bmJvdW5kZWRfcmFuZG9tCiAgICBjb3ZlciA0CiAgICBmcmFtZV9idXJ5IC00CiAgICBmcmFtZV9idXJ5IC01CiAgICBmcmFtZV9idXJ5IC02CiAgICBmcmFtZV9idXJ5IC03CiAgICBmcmFtZV9kaWcgNAogICAgZXh0cmFjdCAyIDAKICAgIHN3YXAKICAgIGR1cAogICAgbGVuCiAgICBpbnQgMTYKICAgIDw9CiAgICBhc3NlcnQgLy8gb3ZlcmZsb3cKICAgIGludCAxNgogICAgYnplcm8KICAgIGJ8CiAgICBjb25jYXQKICAgIGR1cAogICAgbGVuCiAgICBpbnQgMTYKICAgIC8KICAgIGl0b2IKICAgIGV4dHJhY3QgNiAyCiAgICBzd2FwCiAgICBjb25jYXQKICAgIGZyYW1lX2J1cnkgNAogICAgZnJhbWVfZGlnIDMKICAgIGludCAxCiAgICArCiAgICBmcmFtZV9idXJ5IDMKICAgIGIgcGNnMTI4X3JhbmRvbV9mb3JfaGVhZGVyQDMKCnBjZzEyOF9yYW5kb21fZWxzZV9ib2R5QDc6CiAgICBmcmFtZV9kaWcgLTIKICAgIGJ5dGUgMHgKICAgIGIhPQogICAgYnogcGNnMTI4X3JhbmRvbV9lbHNlX2JvZHlAOQogICAgZnJhbWVfZGlnIC0yCiAgICBieXRlIDB4MDEKICAgIGI+CiAgICBhc3NlcnQKICAgIGZyYW1lX2RpZyAtMgogICAgYnl0ZSAweDAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAKICAgIGI8CiAgICBhc3NlcnQKICAgIGZyYW1lX2RpZyAtMgogICAgYnl0ZSAweDAxCiAgICBiLQogICAgZnJhbWVfZGlnIC0zCiAgICBiPgogICAgYXNzZXJ0CiAgICBmcmFtZV9kaWcgLTIKICAgIGZyYW1lX2RpZyAtMwogICAgYi0KICAgIGZyYW1lX2J1cnkgMAogICAgYiBwY2cxMjhfcmFuZG9tX2FmdGVyX2lmX2Vsc2VAMTAKCnBjZzEyOF9yYW5kb21fZWxzZV9ib2R5QDk6CiAgICBmcmFtZV9kaWcgLTMKICAgIGJ5dGUgMHg4MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMAogICAgYjwKICAgIGFzc2VydAogICAgYnl0ZSAweDAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAKICAgIGZyYW1lX2RpZyAtMwogICAgYi0KICAgIGZyYW1lX2J1cnkgMAoKcGNnMTI4X3JhbmRvbV9hZnRlcl9pZl9lbHNlQDEwOgogICAgZnJhbWVfZGlnIDAKICAgIGR1cAogICAgY2FsbHN1YiBfX3VpbnQxMjhfdHdvcwogICAgc3dhcAogICAgYiUKICAgIGZyYW1lX2J1cnkgMgogICAgaW50IDAKICAgIGZyYW1lX2J1cnkgMwoKcGNnMTI4X3JhbmRvbV9mb3JfaGVhZGVyQDExOgogICAgZnJhbWVfZGlnIDMKICAgIGZyYW1lX2RpZyAtMQogICAgPAogICAgYnogcGNnMTI4X3JhbmRvbV9hZnRlcl9mb3JAMTkKCnBjZzEyOF9yYW5kb21fd2hpbGVfdG9wQDEzOgogICAgZnJhbWVfZGlnIC03CiAgICBmcmFtZV9kaWcgLTYKICAgIGZyYW1lX2RpZyAtNQogICAgZnJhbWVfZGlnIC00CiAgICBjYWxsc3ViIF9fcGNnMTI4X3VuYm91bmRlZF9yYW5kb20KICAgIGR1cAogICAgY292ZXIgNQogICAgZnJhbWVfYnVyeSAxCiAgICBmcmFtZV9idXJ5IC00CiAgICBmcmFtZV9idXJ5IC01CiAgICBmcmFtZV9idXJ5IC02CiAgICBmcmFtZV9idXJ5IC03CiAgICBmcmFtZV9kaWcgMgogICAgYj49CiAgICBieiBwY2cxMjhfcmFuZG9tX3doaWxlX3RvcEAxMwogICAgZnJhbWVfZGlnIDQKICAgIGV4dHJhY3QgMiAwCiAgICBmcmFtZV9kaWcgMQogICAgZnJhbWVfZGlnIDAKICAgIGIlCiAgICBmcmFtZV9kaWcgLTMKICAgIGIrCiAgICBkdXAKICAgIGxlbgogICAgaW50IDE2CiAgICA8PQogICAgYXNzZXJ0IC8vIG92ZXJmbG93CiAgICBpbnQgMTYKICAgIGJ6ZXJvCiAgICBifAogICAgY29uY2F0CiAgICBkdXAKICAgIGxlbgogICAgaW50IDE2CiAgICAvCiAgICBpdG9iCiAgICBleHRyYWN0IDYgMgogICAgc3dhcAogICAgY29uY2F0CiAgICBmcmFtZV9idXJ5IDQKICAgIGZyYW1lX2RpZyAzCiAgICBpbnQgMQogICAgKwogICAgZnJhbWVfYnVyeSAzCiAgICBiIHBjZzEyOF9yYW5kb21fZm9yX2hlYWRlckAxMQoKcGNnMTI4X3JhbmRvbV9hZnRlcl9mb3JAMTk6CgpwY2cxMjhfcmFuZG9tX2FmdGVyX2lmX2Vsc2VAMjA6CiAgICBmcmFtZV9kaWcgLTcKICAgIGZyYW1lX2RpZyAtNgogICAgZnJhbWVfZGlnIC01CiAgICBmcmFtZV9kaWcgLTQKICAgIGZyYW1lX2RpZyA0CiAgICB1bmNvdmVyIDkKICAgIHVuY292ZXIgOQogICAgdW5jb3ZlciA5CiAgICB1bmNvdmVyIDkKICAgIHVuY292ZXIgOQogICAgcmV0c3ViCgoKLy8gbGliX3BjZy5wY2cxMjguX19wY2cxMjhfdW5ib3VuZGVkX3JhbmRvbShzdGF0ZS4wOiB1aW50NjQsIHN0YXRlLjE6IHVpbnQ2NCwgc3RhdGUuMjogdWludDY0LCBzdGF0ZS4zOiB1aW50NjQpIC0+IHVpbnQ2NCwgdWludDY0LCB1aW50NjQsIHVpbnQ2NCwgYnl0ZXM6Cl9fcGNnMTI4X3VuYm91bmRlZF9yYW5kb206CiAgICBwcm90byA0IDUKICAgIGZyYW1lX2RpZyAtNAogICAgaW50IDE0NDI2OTUwNDA4ODg5NjM0MDcKICAgIGNhbGxzdWIgX19wY2czMl9zdGVwCiAgICBkdXAKICAgICEKICAgIGludCAxNDQyNjk1MDQwODg4OTYzNDA5CiAgICBzd2FwCiAgICBzaGwKICAgIGZyYW1lX2RpZyAtMwogICAgc3dhcAogICAgY2FsbHN1YiBfX3BjZzMyX3N0ZXAKICAgIGR1cAogICAgIQogICAgaW50IDE0NDI2OTUwNDA4ODg5NjM0MTEKICAgIHN3YXAKICAgIHNobAogICAgZnJhbWVfZGlnIC0yCiAgICBzd2FwCiAgICBjYWxsc3ViIF9fcGNnMzJfc3RlcAogICAgZHVwCiAgICAhCiAgICBpbnQgMTQ0MjY5NTA0MDg4ODk2MzQxMwogICAgc3dhcAogICAgc2hsCiAgICBmcmFtZV9kaWcgLTEKICAgIHN3YXAKICAgIGNhbGxzdWIgX19wY2czMl9zdGVwCiAgICBmcmFtZV9kaWcgLTQKICAgIGNhbGxzdWIgX19wY2czMl9vdXRwdXQKICAgIGludCAzMgogICAgc2hsCiAgICBmcmFtZV9kaWcgLTMKICAgIGNhbGxzdWIgX19wY2czMl9vdXRwdXQKICAgIHwKICAgIGl0b2IKICAgIGZyYW1lX2RpZyAtMgogICAgY2FsbHN1YiBfX3BjZzMyX291dHB1dAogICAgaW50IDMyCiAgICBzaGwKICAgIGZyYW1lX2RpZyAtMQogICAgY2FsbHN1YiBfX3BjZzMyX291dHB1dAogICAgfAogICAgaXRvYgogICAgY29uY2F0CiAgICByZXRzdWIKCgovLyBsaWJfcGNnLnBjZzMyLl9fcGNnMzJfb3V0cHV0KHN0YXRlOiB1aW50NjQpIC0+IHVpbnQ2NDoKX19wY2czMl9vdXRwdXQ6CiAgICBwcm90byAxIDEKICAgIGZyYW1lX2RpZyAtMQogICAgaW50IDE4CiAgICBzaHIKICAgIGZyYW1lX2RpZyAtMQogICAgXgogICAgaW50IDI3CiAgICBzaHIKICAgIGludCA0Mjk0OTY3Mjk1CiAgICAmCiAgICBmcmFtZV9kaWcgLTEKICAgIGludCA1OQogICAgc2hyCiAgICBkdXAKICAgIH4KICAgIGludCAxCiAgICBhZGR3CiAgICBidXJ5IDEKICAgIGRpZyAyCiAgICB1bmNvdmVyIDIKICAgIHNocgogICAgY292ZXIgMgogICAgaW50IDMxCiAgICAmCiAgICBzaGwKICAgIGludCA0Mjk0OTY3Mjk1CiAgICAmCiAgICB8CiAgICByZXRzdWIKCgovLyBsaWJfcGNnLnBjZzEyOC5fX3VpbnQxMjhfdHdvcyh2YWx1ZTogYnl0ZXMpIC0+IGJ5dGVzOgpfX3VpbnQxMjhfdHdvczoKICAgIHByb3RvIDEgMQogICAgZnJhbWVfZGlnIC0xCiAgICBifgogICAgYnl0ZSAweDAxCiAgICBiKwogICAgYnl0ZSAweGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmCiAgICBiJgogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLmxpYl9wY2cxMjhfZXhwb3Nlci5jb250cmFjdC5MaWJQY2cxMjhFeHBvc2VyQWxnb3B5LnVwZGF0ZSgpIC0+IHZvaWQ6CnVwZGF0ZToKICAgIHByb3RvIDAgMAogICAgdHhuIFNlbmRlcgogICAgZ2xvYmFsIENyZWF0b3JBZGRyZXNzCiAgICA9PQogICAgYXNzZXJ0CiAgICByZXRzdWIK",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMubGliX3BjZzEyOF9leHBvc2VyLmNvbnRyYWN0LkxpYlBjZzEyOEV4cG9zZXJBbGdvcHkuY2xlYXJfc3RhdGVfcHJvZ3JhbToKICAgIGludCAxCiAgICByZXR1cm4K"
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
        "name": "LibPcg128ExposerAlgopy",
        "methods": [
            {
                "name": "bounded_rand_uint128",
                "args": [
                    {
                        "type": "byte[32]",
                        "name": "seed"
                    },
                    {
                        "type": "uint128",
                        "name": "lower_bound"
                    },
                    {
                        "type": "uint128",
                        "name": "upper_bound"
                    },
                    {
                        "type": "uint16",
                        "name": "length"
                    }
                ],
                "returns": {
                    "type": "uint128[]"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
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
class BoundedRandUint128Args(_ArgsBase[list[int]]):
    seed: bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
    lower_bound: int
    upper_bound: int
    length: int

    @staticmethod
    def method() -> str:
        return "bounded_rand_uint128(byte[32],uint128,uint128,uint16)uint128[]"


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

    def bounded_rand_uint128(
        self,
        *,
        seed: bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int],
        lower_bound: int,
        upper_bound: int,
        length: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `bounded_rand_uint128(byte[32],uint128,uint128,uint16)uint128[]` ABI method
        
        :param bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int] seed: The `seed` ABI parameter
        :param int lower_bound: The `lower_bound` ABI parameter
        :param int upper_bound: The `upper_bound` ABI parameter
        :param int length: The `length` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = BoundedRandUint128Args(
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


class LibPcg128ExposerAlgopyClient:
    """A class for interacting with the LibPcg128ExposerAlgopy app providing high productivity and
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
        LibPcg128ExposerAlgopyClient can be created with an app_id to interact with an existing application, alternatively
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

    def bounded_rand_uint128(
        self,
        *,
        seed: bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int],
        lower_bound: int,
        upper_bound: int,
        length: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[list[int]]:
        """Calls `bounded_rand_uint128(byte[32],uint128,uint128,uint16)uint128[]` ABI method
        
        :param bytes | bytearray | tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int] seed: The `seed` ABI parameter
        :param int lower_bound: The `lower_bound` ABI parameter
        :param int upper_bound: The `upper_bound` ABI parameter
        :param int length: The `length` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[list[int]]: The result of the transaction"""

        args = BoundedRandUint128Args(
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
