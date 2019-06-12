#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from bitcoin.addr import b58_address_to_hash160, hash160_to_b58_address, script_to_address, address_to_script
from bitcoin.params import BitcoinMainnet, BitcoinTestnet, BitcoinRegtest
from qtum.params import QtumMainnet, QtumRegtest, QtumTestnet
from bitcoin.addr import hash_to_segwit_addr, pubkey_to_address, address_from_private_key


def addr_convert(addr, fromnet, tonet):
    addr_type, hash160 = b58_address_to_hash160(addr)
    if addr_type == fromnet.ADDRTYPE_P2PKH:
        return hash160_to_b58_address(hash160, addrtype=tonet.ADDRTYPE_P2PKH)
    elif addr_type == fromnet.ADDRTYPE_P2SH:
        return hash160_to_b58_address(hash160, addrtype=tonet.ADDRTYPE_P2SH)


if __name__ == '__main__':
    # print(addr_convert('1C5bSj1iEGUgSTbziymG7Cn18ENQuT36vv', BitcoinMainnet, QtumMainnet))
    # print(addr_convert('', BitcoinTestnet, QtumTestnet))
    print(addr_convert('mvHPesWqLXXy7hntNa7vbAoVwqN5PnrwJd', BitcoinTestnet, QtumTestnet))

    print(address_from_private_key('cRp4uUnreGMZN8vB7nQFX6XWMHU5Lc73HMAhmcDEwHfbgRS66Cqp', BitcoinTestnet))

    # print(script_to_address('0014751e76e8199196d454941c45d1b3a323f1433bd6', QtumRegtest))
    # print(script_to_address('000000c4a5cad46221b2a187905e5266362b99d5e91c6ce24d165dab93e86433', BitcoinTestnet))
    # print(script_to_address('00201863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262', QtumTestnet))
    # print(address_to_script('tq1qqqqqp399et2xygdj5xreqhjjvcmzhxw4aywxecjdzew6hylgvsesswsl2d', QtumTestnet))

    # print(address_to_script('qc1qwm5pnyvk632fg8z96xe6xgl3gvaavw78unl', QtumMainnet))

    print(script_to_address('76a91465a16059864a2fdbc7c99a4723a8395bc6f188eb88ac', QtumMainnet))
    # print(address_to_script('bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4', BitcoinMainnet))

    # print('qc1qw508d6qejxtdg4y5r3zarvary0c5xw7kq52at0'.upper())

    # print(hash_to_segwit_addr(bytes.fromhex('000000c4a5cad46221b2a187905e5266362b99d5e91c6ce24d165dab93e86433'),
    #                           0, net=QtumTestnet))

    # print(pubkey_to_address('p2wpkh', '03025324888e429ab8e3dbaf1f7802648b9cd01e9b418485c5fa4c1b9b5700e1a6', net=QtumMainnet))
    #
