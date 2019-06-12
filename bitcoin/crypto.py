#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
from typing import Union
from .util import to_bytes
import hashlib


def sha256(x: Union[bytes, str]) -> bytes:
    x = to_bytes(x, 'utf8')
    return bytes(hashlib.sha256(x).digest())


def sha256d(x: Union[bytes, str]) -> bytes:
    x = to_bytes(x, 'utf8')
    out = bytes(sha256(sha256(x)))
    return out


def hash_160(x: bytes) -> bytes:
    try:
        md = hashlib.new('ripemd160')
        md.update(sha256(x))
        return md.digest()
    except BaseException:
        from . import ripemd
        md = ripemd.new(sha256(x))
        return md.digest()