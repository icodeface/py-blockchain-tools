#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
import os
import binascii
from bitcoin import bech32
from bitcoin.addr import address_from_private_key_bytes, hash_to_segwit_addr
from bitcoin.addr import b58_address_to_hash160
from qtum.params import QtumRegtest


def generate():
    for i in range(10):
        data = os.urandom(32)
        addr = hash_to_segwit_addr(data, 0, net=QtumRegtest)
        univer = '0400{}'.format(binascii.b2a_hex(data).decode())
        # univer = '0200{}'.format(binascii.b2a_hex(b58_address_to_hash160(addr)[1]).decode())
        # print(addr, bytes(bech32.decode(QtumRegtest.SEGWIT_HRP, addr)[1]).hex())
        # univer = '0300{}'.format(bytes(bech32.decode(QtumRegtest.SEGWIT_HRP, addr)[1]).hex())
        print('["{}", "{}"],'.format(addr, univer))


if __name__ == '__main__':
    generate()