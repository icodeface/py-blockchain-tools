#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time


def mine():
    while True:
        try:
            os.system(f"./src/bsc-cli generatetoaddress 1 {sys.argv[1]} 100000000")
            time.sleep(10*60)
        except BaseException as e:
            print(e)
            return


if __name__ == '__main__':
    mine()
