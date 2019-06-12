#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
import os
from random import randint
from eth_keys import keys
from eth_keys.datatypes import Signature, PrivateKey
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
    return keccak(msg).hex(), signature, pk.public_key.to_address()[2:]


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

    msg_hash, sig, pubkey = generate_test_data(priv=b"\x00"*32)

    print("msg_hash", msg_hash, "sig", sig, "pubkey", pubkey)

    sig_str = str(sig)[2:]

    r = sig_str[0:64]
    s = sig_str[64:128]
    v = sig_str[128:130]

    print("r s v", r, s, v)

    result.append((eth_abi_encode(abi, [
        binascii.a2b_hex(msg_hash),
        int(v, 16) + 27,
        binascii.a2b_hex(r),
        binascii.a2b_hex(s)
    ])))
    result.append("000000000000000000000000" + pubkey)

    print(result)

    pp = sig.recover_public_key_from_msg_hash(binascii.a2b_hex(msg_hash))

    print(pp, pp.to_address())


    # for i in range(50):
    #     msg_hash, sig, pubkey = generate_test_data()
    #
    #     r = sig[0:64]
    #     s = sig[64:128]
    #     v = sig[128:130]
    #
    #     result.append((eth_abi_encode(abi, [
    #         binascii.a2b_hex(msg_hash),
    #         int(v, 16) + 27,
    #         binascii.a2b_hex(r),
    #         binascii.a2b_hex(s)
    #     ])))
    #     result.append("000000000000000000000000" + pubkey)

    return result


def ecrecover():
    sig = "7c1886d96dc50f07a48fa7d72006809ac9f45d6b1c34b7a072ace679674c64a230aac08d000000000000000000000000000000000000000000000000000000000000001c9c88b967e65708ae5b744502ec117fae31b7f787753e63d8cea7047e789bd55d1d5557b6eca94f4f7473c862cfb5488980d7e1e3eb764f5f11b0fe2281931d2e"
    pubkey = "0000000000000000000000003f17f1962b36e491b30a40b2405849e597ba5fb5"

    sig = Signature(binascii.a2b_hex(sig))

    sig.recover_public_key_from_msg()




if __name__ == '__main__':
    run()
