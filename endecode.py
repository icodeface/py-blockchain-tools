#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
import binascii


def reverse_str(encoded: str):
    i = len(encoded) // 2
    while True:
        if i <= 0:
            break
        x = encoded[i*2-2:i*2]
        print(f'{x}', end='')
        i -= 1


def reverse_str_to_hex_print(encoded: str):
    i = len(encoded) // 2
    while True:
        if i <= 0:
            break
        x = encoded[i*2-2:i*2]
        if (i - 1) % 8 == 0:
            print(f'0x{x}', end=', \n')
        else:
            print(f'0x{x}', end=', ')
        i -= 1


def str_to_hex_print(encoded: str):
    for i in range(len(encoded) // 2):
        i = i * 2
        x = encoded[i:i + 2]
        # print(x)
        if (i // 2 + 1) % 8 == 0:
            print(f'0x{x}', end=', \n')
        else:
            print(f'0x{x}', end=', ')


def transfer(s: str):
    encoded = binascii.b2a_hex(s.encode()).decode()
    str_to_hex_print(encoded)


btc = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"

qtum = "Sep 02, 2017 Bitcoin breaks $5,000 in latest price frenzy"

#transfer(qtum)
reverse_str('067ce78100994c2e1a69d544e519570d166440a066c92f4c88dc01683912b1e0')

# print('\n')

# str_to_hex_print('3045022100beac3b081a8be617827412c1b876dfab2a1b64801ffb5da1afdc94052bf0753702203718e6f6ed4476bca28e7aa99c10780f223951f1f91fe0554377170c192379ba')




