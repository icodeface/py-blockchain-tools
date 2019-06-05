#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from eth_abi import encode_abi
from eth_utils import function_abi_to_4byte_selector


def eth_abi_encode(abi: dict, args: list) -> str:
    """
    >> abi = {"constant":True,"inputs":[{"name":"","type":"address"}],
"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"}
    >> eth_abi_encode(abi, ['9d3d4cc1986d81f9109f2b091b7732e7d9bcf63b'])
    >> '70a082310000000000000000000000009d3d4cc1986d81f9109f2b091b7732e7d9bcf63b'
    ## address must be lower case
    :param abi: dict
    :param args: list
    :return: str
    """
    if not abi:
        return "00"
    types = list([inp['type'] for inp in abi.get('inputs', [])])
    if abi.get('name'):
        result = function_abi_to_4byte_selector(abi) + encode_abi(types, args)
    else:
        result = encode_abi(types, args)
    return result.hex()
