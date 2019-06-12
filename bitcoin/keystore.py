#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from .util import inv_dict
from .b58 import DecodeBase58Check
from typing import Tuple
from .params import BitcoinMainnet
from . import ecc


WIF_SCRIPT_TYPES = {
    'p2pkh': 0,
    'p2wpkh': 1,
    'p2wpkh-p2sh': 2,
    'p2sh': 5,
    'p2wsh': 6,
    'p2wsh-p2sh': 7
}
WIF_SCRIPT_TYPES_INV = inv_dict(WIF_SCRIPT_TYPES)


def is_segwit_script_type(txin_type: str) -> bool:
    return txin_type in ('p2wpkh', 'p2wpkh-p2sh', 'p2wsh', 'p2wsh-p2sh')


def deserialize_privkey(key: str, wif_prefix=BitcoinMainnet.WIF_PREFIX) -> Tuple[str, bytes, bool]:
    txin_type = None
    if ':' in key:
        txin_type, key = key.split(sep=':', maxsplit=1)
        assert txin_type in WIF_SCRIPT_TYPES
    try:
        vch = DecodeBase58Check(key)
    except BaseException:
        neutered_privkey = str(key)[:3] + '..' + str(key)[-2:]
        raise Exception("cannot deserialize", neutered_privkey)

    if txin_type is None:
        # keys exported in version 3.0.x encoded script type in first byte
        prefix_value = vch[0] - wif_prefix
        try:
            txin_type = WIF_SCRIPT_TYPES_INV[prefix_value]
        except KeyError:
            raise Exception('invalid prefix ({}) for WIF key (1)'.format(vch[0]))
    else:
        # all other keys must have a fixed first byte
        if vch[0] != wif_prefix:
            raise Exception('invalid prefix ({}) for WIF key (2)'.format(vch[0]))

    if len(vch) not in [33, 34]:
        raise Exception('invalid vch len for WIF key: {}'.format(len(vch)))
    compressed = False
    if len(vch) == 34:
        if vch[33] == 0x01:
            compressed = True
        else:
            raise Exception(f'invalid WIF key. length suggests compressed pubkey, '
                                   f'but last byte is {vch[33]} != 0x01')

    if is_segwit_script_type(txin_type) and not compressed:
        raise Exception('only compressed public keys can be used in segwit scripts')

    secret_bytes = vch[1:33]
    # we accept secrets outside curve range; cast into range here:
    secret_bytes = ecc.ECPrivkey.normalize_secret_bytes(secret_bytes)
    return txin_type, secret_bytes, compressed

