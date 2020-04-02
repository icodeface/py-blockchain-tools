#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

BIN_PATH = '/home/i/bsc/src'
ARGS = '--datadir=/data/explorer/bsc'
FORK_HEIGHT = 623408


def run():
    tip = os.popen(f'{BIN_PATH}/bsc-cli {ARGS} getblockcount').readline().rstrip()
    for height in list(range(FORK_HEIGHT, int(tip)))[::-1]:
        try:
            block_hash = os.popen(f'{BIN_PATH}/bsc-cli {ARGS} getblockhash {height}').readline().rstrip()
            os.system(f"{BIN_PATH}/bsc-cli {ARGS} invalidateblock {block_hash}")
        except BaseException as e:
            print(e)
            return


if __name__ == '__main__':
    run()
