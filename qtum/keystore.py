#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from bitcoin.keystore import deserialize_privkey, serialize_privkey
from bitcoin.params import BitcoinTestnet
from qtum.params import QtumTestnet
import binascii


def key_convert():
    p = 'cVuzKWCszfvjkoJyUasvsrRdECriz8hSd1BDinRNzytwnXmX7m1g'
    txin_type, secret_bytes, compressed = deserialize_privkey(p, BitcoinTestnet.WIF_PREFIX)
    print(binascii.b2a_hex(secret_bytes))
    pp = serialize_privkey(secret_bytes, compressed, txin_type, False, QtumTestnet.WIF_PREFIX)
    print(pp)


def bytes_to_wif():
    secret_bytes = binascii.a2b_hex("f89f117243702dc1d6185914692d85ce856c1e957b726ba8fb675bdf748f770e")
    compressed = True
    txin_type = 'p2pkh'
    pp = serialize_privkey(secret_bytes, compressed, txin_type, False, QtumTestnet.WIF_PREFIX)
    print(pp)


if __name__ == '__main__':
    bytes_to_wif()
    # key_convert()