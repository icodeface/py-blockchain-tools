#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
import os
from random import randint
from eth_keys import keys
from eth_utils.crypto import keccak
from ethereum.abi import eth_abi_encode
import binascii
from pprint import pprint


def generate_test_data(priv=None, msg=None):
    # return msg_hash, signature, pubkey
    if not priv:
        priv = os.urandom(32)
    pk = keys.PrivateKey(priv)
    if not msg:
        msg = os.urandom(randint(0, 1024))
    signature = pk.sign_msg(msg)
    return keccak(msg).hex(), str(signature)[2:], pk.public_key.to_address()[2:]


def run():
    abi = {
    "constant": False,
    "inputs": [
        {
          "name": "h",
          "type": "bytes32"
        },
        {
          "name": "v",
          "type": "uint8"
        },
        {
          "name": "r",
          "type": "bytes32"
        },
        {
          "name": "s",
          "type": "bytes32"
        }
    ],
    "name": "ecrecover_test",
    "outputs": [],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
    }

    result = []
    for i in range(50):
        msg_hash, sig, pubkey = generate_test_data()

        r = sig[0:64]
        s = sig[64:128]
        v = sig[128:130]

        result.append((eth_abi_encode(abi, [
            binascii.a2b_hex(msg_hash),
            int(v, 16) + 27,
            binascii.a2b_hex(r),
            binascii.a2b_hex(s)
        ])))
        result.append("000000000000000000000000" + pubkey)

    return result


if __name__ == '__main__':
    pprint(run())