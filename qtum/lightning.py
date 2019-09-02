#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from bitcoin.lightning import lnencode, LnAddr, lndecode, trim_to_bytes
import binascii
from copy import deepcopy
from qtum.address import addr_convert


def convert_addr(addr: LnAddr, fromNet, toNet) -> LnAddr:
    addr = deepcopy(addr)
    addr.currency = toNet.SEGWIT_HRP
    tags = []
    for key, tag in addr.tags:
        if key == 'f':
            fallback = str(tag)
            new_fallback = addr_convert(fallback, fromNet, toNet)
            tags.append(('f', new_fallback))
        else:
            tags.append((key, tag))
    addr.tags = tags
    return addr


def convert_payment(payment: str, fromNet, toNet, privkey: str):
    priv = binascii.a2b_hex(privkey)
    dd = lndecode(a=payment, verbose=False, expected_hrp=None, net=fromNet)
    addr = convert_addr(dd, fromNet, toNet)
    ee = lnencode(addr, priv, net=toNet)
    return ee


if __name__ == '__main__':
    from bitcoin.params import BitcoinMainnet, BitcoinTestnet
    from qtum.params import QtumMainnet, QtumTestnet

    pp = 'lntb30m1pw2f2yspp5s59w4a0kjecw3zyexm7zur8l8n4scw674w8sftjhwec33km882gsdpa2pshjmt9de6zqun9w96k2um5ypmkjargypkh2mr5d9cxzun5ypeh2ursdae8gxqruyqvzddp68gup69uhnzwfj9cejuvf3xshrwde68qcrswf0d46kcarfwpshyaplw3skw0tdw4k8g6tsv9e8g4a3hx0v945csrmpm7yxyaamgt2xu7mu4xyt3vp7045n4k4czxf9kj0vw0m8dr5t3pjxuek04rtgyy8uzss5eet5gcyekd6m7u0mzv5sp7mdsag'
    # priv = 'e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734'
    # converted = convert_payment(pp, BitcoinTestnet, QtumTestnet, priv)

    dd = lndecode(a=pp, verbose=False, expected_hrp=None, net=BitcoinTestnet)
    # print(dd.tags, dd.unknown_tags)
    for v in dd.unknown_tags:
        print(v[0], trim_to_bytes(v[1]).decode('utf-8'))
    # print(dd._min_final_cltv_expiry)
    # print(converted)