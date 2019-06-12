#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from .script import opcodes, script_GetOp, match_decoded, push_script, add_number_to_script
from typing import Tuple
from .params import BitcoinMainnet
from .util import to_bytes
from .b58 import base_decode, base_encode
from .crypto import sha256d, hash_160, sha256
from . import bech32, ecc
from .keystore import deserialize_privkey


TYPE_ADDRESS = 0
TYPE_PUBKEY  = 1
TYPE_SCRIPT  = 2


def is_segwit_address(addr, *, net=None):
    if net is None: net = BitcoinMainnet
    try:
        witver, witprog = bech32.decode(net.SEGWIT_HRP, addr)
    except Exception as e:
        return False
    return witprog is not None


def is_b58_address(addr, *, net=None):
    if net is None: net = BitcoinMainnet
    try:
        addrtype, h = b58_address_to_hash160(addr)
    except Exception as e:
        return False
    if addrtype not in [net.ADDRTYPE_P2PKH, net.ADDRTYPE_P2SH]:
        return False
    return addr == hash160_to_b58_address(h, addrtype)


def is_address(addr, *, net=None):
    if net is None: net = BitcoinMainnet
    return is_segwit_address(addr, net=net) \
           or is_b58_address(addr, net=net)


def b58_address_to_hash160(addr):
    addr = to_bytes(addr, 'ascii')
    _bytes = base_decode(addr, 25, base=58)
    return _bytes[0], _bytes[1:21]


def hash160_to_b58_address(h160: bytes, addrtype, witness_program_version=1):
    s = bytes([addrtype])
    s += h160
    return base_encode(s+sha256d(s)[0:4], base=58)


def hash160_to_p2pkh(h160: bytes, net=None) -> str:
    if net is None: net = BitcoinMainnet
    return hash160_to_b58_address(h160, net.ADDRTYPE_P2PKH)


def hash160_to_p2sh(h160: bytes, net=None) -> str:
    if net is None: net = BitcoinMainnet
    return hash160_to_b58_address(h160, net.ADDRTYPE_P2SH)


def public_key_to_p2pkh(public_key: bytes, net=None) -> str:
    if net is None: net = BitcoinMainnet
    return hash160_to_p2pkh(hash_160(public_key), net=net)


def hash_to_segwit_addr(h: bytes, witver: int, *, net=None) -> str:
    if net is None: net = BitcoinMainnet
    return bech32.encode(net.SEGWIT_HRP, witver, h)

def public_key_to_p2wpkh(public_key: bytes, *, net=None) -> str:
    if net is None: net = BitcoinMainnet
    return hash_to_segwit_addr(hash_160(public_key), witver=0, net=net)


def script_to_p2wsh(script: str, *, net=None) -> str:
    if net is None: net = BitcoinMainnet
    return hash_to_segwit_addr(sha256(bytes.fromhex(script)), witver=0, net=net)


def p2wpkh_nested_script(pubkey):
    pkh = hash_160(bytes.fromhex(pubkey)).hex()
    return '00' + push_script(pkh)


def p2wsh_nested_script(witness_script):
    wsh = sha256(bytes.fromhex(witness_script)).hex()
    return '00' + push_script(wsh)


def get_address_from_output_script(_bytes: bytes, *, net=None) -> Tuple[int, str]:
    try:
        decoded = [x for x in script_GetOp(_bytes)]
    except BaseException:
        decoded = None

    # The Genesis Block, self-payments, and pay-by-IP-address payments look like:
    # 65 BYTES:... CHECKSIG
    match = [opcodes.OP_PUSHDATA4, opcodes.OP_CHECKSIG]
    if match_decoded(decoded, match):
        return TYPE_PUBKEY, decoded[0][1].hex()

    # Pay-by-Bitcoin-address TxOuts look like:
    # DUP HASH160 20 BYTES:... EQUALVERIFY CHECKSIG
    match = [opcodes.OP_DUP, opcodes.OP_HASH160, opcodes.OP_PUSHDATA4, opcodes.OP_EQUALVERIFY, opcodes.OP_CHECKSIG]
    if match_decoded(decoded, match):
        return TYPE_ADDRESS, hash160_to_p2pkh(decoded[2][1], net=net)

    # p2sh
    match = [ opcodes.OP_HASH160, opcodes.OP_PUSHDATA4, opcodes.OP_EQUAL ]
    if match_decoded(decoded, match):
        return TYPE_ADDRESS, hash160_to_p2sh(decoded[1][1], net=net)

    # segwit address
    possible_witness_versions = [opcodes.OP_0] + list(range(opcodes.OP_1, opcodes.OP_16 + 1))

    for witver, opcode in enumerate(possible_witness_versions):
        # return TYPE_ADDRESS, hash_to_segwit_addr(decoded[1][1], witver=witver, net=net)
        match = [opcode, opcodes.OP_PUSHDATA4]
        if match_decoded(decoded, match):
            return TYPE_ADDRESS, hash_to_segwit_addr(decoded[1][1], witver=witver, net=net)

    return TYPE_SCRIPT, _bytes.hex()


def script_to_address(script: str, net=None) -> str:
    t, addr = get_address_from_output_script(bytes.fromhex(script), net=net)
    assert t == TYPE_ADDRESS
    return addr


def address_to_script(addr: str, net=None) -> str:
    if net is None: net = BitcoinMainnet
    if not is_address(addr, net=net):
        raise Exception(f"invalid bitcoin address: {addr}")
    witver, witprog = bech32.decode(net.SEGWIT_HRP, addr)
    if witprog is not None:
        if not (0 <= witver <= 16):
            raise Exception(f'impossible witness version: {witver}')
        script = add_number_to_script(witver).hex()
        script += push_script(bytes(witprog).hex())
        return script
    addrtype, hash_160_ = b58_address_to_hash160(addr)
    if addrtype == net.ADDRTYPE_P2PKH:
        script = bytes([opcodes.OP_DUP, opcodes.OP_HASH160]).hex()
        script += push_script(hash_160_.hex())
        script += bytes([opcodes.OP_EQUALVERIFY, opcodes.OP_CHECKSIG]).hex()
    elif addrtype == net.ADDRTYPE_P2SH:
        script = opcodes.OP_HASH160.hex()
        script += push_script(hash_160_.hex())
        script += opcodes.OP_EQUAL.hex()
    else:
        raise Exception(f'unknown address type: {addrtype}')
    return script


def pubkey_to_address(txin_type: str, pubkey: str, *, net=None) -> str:
    if net is None: net = BitcoinMainnet
    if txin_type == 'p2pkh':
        return public_key_to_p2pkh(bytes.fromhex(pubkey), net=net)
    elif txin_type == 'p2wpkh':
        return public_key_to_p2wpkh(bytes.fromhex(pubkey), net=net)
    elif txin_type == 'p2wpkh-p2sh':
        scriptSig = p2wpkh_nested_script(pubkey)
        return hash160_to_p2sh(hash_160(bytes.fromhex(scriptSig)), net=net)
    else:
        raise NotImplementedError(txin_type)


def address_from_private_key(sec: str, net=None) -> str:
    if net is None:
        net = BitcoinMainnet
    txin_type, privkey, compressed = deserialize_privkey(sec, net.WIF_PREFIX)
    public_key = ecc.ECPrivkey(privkey).get_public_key_hex(compressed=compressed)
    address = pubkey_to_address(txin_type, public_key)
    return address