#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from bitcoin.keystore import deserialize_privkey, serialize_privkey
from bitcoin.params import BitcoinTestnet
from qtum.params import QtumTestnet


def key_convert():
    p = 'cVuzKWCszfvjkoJyUasvsrRdECriz8hSd1BDinRNzytwnXmX7m1g'
    txin_type, secret_bytes, compressed = deserialize_privkey(p, BitcoinTestnet.WIF_PREFIX)
    pp = serialize_privkey(secret_bytes, compressed, txin_type, False, QtumTestnet.WIF_PREFIX)
    print(pp)


if __name__ == '__main__':
    key_convert()