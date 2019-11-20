#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""

import binascii

def bxor(b1, b2): # use xor for bytes
    result = b""
    for b1, b2 in zip(b1, b2):
        result += bytes([b1 ^ b2])
    return result

a = binascii.a2b_hex("2ee5ede681ab7ee056b76e7de36b0b12c12aef7c38375af13cb280da07b4dd00")
b = binascii.a2b_hex("d67decfca42ff596d6468c01cfa5fc0791719dff3eb09112b29576cde99a62ae")
mask = binascii.a2b_hex("00"*32)

# result = []
#
# for index, x in enumerate(a):
#     result.append(x ^ 0)

print([aaa for aaa in a])

print([jjj for jjj in bxor(a, mask)])

print([iii for iii in b])
