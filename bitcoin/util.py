#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""

def inv_dict(d):
    return {v: k for k, v in d.items()}

def assert_bytes(*args):
    """
    porting helper, assert args type
    """
    try:
        for x in args:
            assert isinstance(x, (bytes, bytearray))
    except:
        print('assert bytes failed', list(map(type, args)))
        raise

def to_bytes(something, encoding='utf8') -> bytes:
    """
    cast string to bytes() like object, but for python2 support it's bytearray copy
    """
    if isinstance(something, bytes):
        return something
    if isinstance(something, str):
        return something.encode(encoding)
    elif isinstance(something, bytearray):
        return bytes(something)
    else:
        raise TypeError("Not a string or bytes like object")

