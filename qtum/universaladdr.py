#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
import os
import binascii
from bitcoin import bech32
from bitcoin.addr import address_from_private_key_bytes, hash_to_segwit_addr
from bitcoin.addr import b58_address_to_hash160, hash160_to_b58_address
from qtum.params import QtumRegtest


def generate():
    for i in range(10):
        h160 = os.urandom(20)
        addr = hash160_to_b58_address(h160, QtumRegtest.ADDRTYPE_TVM)
        # addr = hash_to_segwit_addr(data, 0, net=QtumRegtest)
        # addr = address_from_private_key_bytes(data, True, QtumRegtest)
        univer = '0480{}'.format(binascii.b2a_hex(h160).decode())
        # univer = '0200{}'.format(binascii.b2a_hex(b58_address_to_hash160(addr)[1]).decode())
        # print(addr, bytes(bech32.decode(QtumRegtest.SEGWIT_HRP, addr)[1]).hex())
        # univer = '0300{}'.format(bytes(bech32.decode(QtumRegtest.SEGWIT_HRP, addr)[1]).hex())
        print('["{}", "{}"],'.format(addr, univer))


if __name__ == '__main__':
    # hh = b58_address_to_hash160('xRHy9Em8QPe8WDHJLsAQU1qmcegqPH3bp8')
    # print(hh, len(hh[1]))
    # addr = hash160_to_b58_address(hh[1], hh[0])
    # print(addr)
    generate()