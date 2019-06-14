#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from bitcoin.lightning import lnencode, LnAddr, lndecode
import binascii
from copy import deepcopy
from .address import addr_convert


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


def convert_payment(paymet: str, fromNet, toNet, privkey: str):
    dd = lndecode(a=paymet, verbose=True, expected_hrp=None, net=fromNet)
    print(dd)
    addr = convert_addr(dd, fromNet, toNet)
    priv = binascii.a2b_hex(privkey)
    ee = lnencode(addr, priv, net=toNet)
    return ee
