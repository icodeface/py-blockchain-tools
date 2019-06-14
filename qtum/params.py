#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""


class QtumMainnet(object):
    ADDRTYPE_P2PKH = 0x3a
    ADDRTYPE_P2SH = 0x32
    SEGWIT_HRP = "qc"
    LN_SEGWIT_HRP = 'lnqc'
    GENESIS = "000075aef83cf2853580f8ae8ce6f8c3096cfa21d98334d6e3f95e5582ed986c"
    XPRV_HEADERS = {
        'standard': 0x0488ade4,
        'p2wpkh-p2sh': 0x049d7878,
        'p2wsh-p2sh': 0x295b005,
        'p2wpkh': 0x4b2430c,
        'p2wsh': 0x2aa7a99
    }
    XPUB_HEADERS = {
        'standard': 0x0488b21e,
        'p2wpkh-p2sh': 0x049d7cb2,
        'p2wsh-p2sh': 0x295b43f,
        'p2wpkh': 0x4b24746,
        'p2wsh': 0x2aa7ed3
    }

    MSG_MAGIC = b"\x15Qtum Signed Message:\n"


class QtumTestnet(QtumMainnet):
    ADDRTYPE_P2PKH = 120
    ADDRTYPE_P2SH = 110
    SEGWIT_HRP = "tq"
    LN_SEGWIT_HRP = 'lntq'
    WIF_PREFIX = 0xef
    GENESIS = "0000e803ee215c0684ca0d2f9220594d3f828617972aad66feb2ba51f5e14222"
    XPRV_HEADERS = {
        'standard': 0x04358394,
        'p2wpkh-p2sh': 0x044a4e28,
        'p2wsh-p2sh': 0x024285b5,
        'p2wpkh': 0x045f18bc,
        'p2wsh': 0x02575048
    }
    XPUB_HEADERS = {
        'standard': 0x043587cf,
        'p2wpkh-p2sh': 0x044a5262,
        'p2wsh-p2sh': 0x024289ef,
        'p2wpkh': 0x045f1cf6,
        'p2wsh': 0x02575483
    }


class QtumRegtest(QtumTestnet):
    SEGWIT_HRP = "qcrt"
    LN_SEGWIT_HRP = 'lnqcrt'
    GENESIS = "0x665ed5b402ac0b44efc37d8926332994363e8a7278b7ee9a58fb972efadae943"