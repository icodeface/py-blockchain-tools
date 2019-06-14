#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from bitcoin.addr import b58_address_to_hash160, hash160_to_b58_address, script_to_address, address_to_script
from bitcoin.params import BitcoinMainnet, BitcoinTestnet, BitcoinRegtest
from qtum.params import QtumMainnet, QtumRegtest, QtumTestnet
from bitcoin.addr import hash_to_segwit_addr, pubkey_to_address, address_from_private_key


def addr_convert(addr:str, fromnet, tonet):
    if len(addr) == 34 or len(addr) == 35:
        addr_type, hash160 = b58_address_to_hash160(addr)
        if addr_type == fromnet.ADDRTYPE_P2PKH:
            return hash160_to_b58_address(hash160, addrtype=tonet.ADDRTYPE_P2PKH)
        elif addr_type == fromnet.ADDRTYPE_P2SH:
            return hash160_to_b58_address(hash160, addrtype=tonet.ADDRTYPE_P2SH)
    elif addr.startswith(fromnet.SEGWIT_HRP):
        script = address_to_script(addr, fromnet)
        return script_to_address(script, tonet)
    else:
        raise BaseException('unknown address type', addr)

if __name__ == '__main__':
    # print(addr_convert('1C5bSj1iEGUgSTbziymG7Cn18ENQuT36vv', BitcoinMainnet, QtumMainnet))
    # print(addr_convert('', BitcoinTestnet, QtumTestnet))
    print(addr_convert('mvHPesWqLXXy7hntNa7vbAoVwqN5PnrwJd', BitcoinTestnet, QtumTestnet))

    print(address_from_private_key('cRumXueoZHjhGXrZWeFoEBkeDHu2m8dW5qtFBCqSAt4LDR2Hnd8Q', net=BitcoinTestnet))

    # print(script_to_address('0014751e76e8199196d454941c45d1b3a323f1433bd6', QtumRegtest))
    # print(script_to_address('000000c4a5cad46221b2a187905e5266362b99d5e91c6ce24d165dab93e86433', BitcoinTestnet))
    # print(script_to_address('00201863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262', QtumTestnet))
    # print(address_to_script('tq1qqqqqp399et2xygdj5xreqhjjvcmzhxw4aywxecjdzew6hylgvsesswsl2d', QtumTestnet))

    # print(address_to_script('qc1qwm5pnyvk632fg8z96xe6xgl3gvaavw78unl', QtumMainnet))

    # print(script_to_address('0014751e76e8199196d454941c45d1b3a323f1433bd6', QtumMainnet))
    # print(address_to_script('bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4', BitcoinMainnet))

    # print('qc1qw508d6qejxtdg4y5r3zarvary0c5xw7kq52at0'.upper())

    # print(hash_to_segwit_addr(bytes.fromhex('000000c4a5cad46221b2a187905e5266362b99d5e91c6ce24d165dab93e86433'),
    #                           0, net=QtumTestnet))

    # print(pubkey_to_address('p2wpkh', '03025324888e429ab8e3dbaf1f7802648b9cd01e9b418485c5fa4c1b9b5700e1a6', net=QtumMainnet))
    #

    # raw = '000000206c98ed82555ef9e3d63483d921fa6c09c3f8e68caef8803585f23cf8ae7500007cedea072eb141887b85795cff161c8be553d5d26ed5abef70f35830a4d5412ef92db259ffff001fd4fc0000e965ffd002cd6ad0e2dc402b8044de833e06b23127ea8c3d80aec9141077149556e81f171bcc55a6ff8345e692c0f86e5b48e01b996cadc001622fb5e363b4210000000000000000000000000000000000000000000000000000000000000000ffffffff000102000000010000000000000000000000000000000000000000000000000000000000000000ffffffff03510101ffffffff0200204aa9d101000023210327cc6528042455febfee353d2a888b38cc3ba0bac0f5566aa9eb7e70b576a6efac0000000000000000266a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf900000000'
    # with open("qtum-block1.dat", 'wb') as f:
    #     f.write(bytes.fromhex(raw))
    #
    # with open('/Users/face/Projects/qtum-scala-lib/src/test/resources/block1.dat', 'rb') as f:
    #     print(f.read(2048).hex())