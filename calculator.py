#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""

COIN = 10**8


def coin_calc(init_coin, init_reward, min_reward, subside_block):
    total = init_coin
    reward = init_reward
    r = 0
    while reward >= min_reward:
        total += subside_block * reward
        reward = reward // 2
        r += 1
    print('round: ', r)
    return total


def hashrate_calc():
    diff = 2600779
    target = 0x00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff / diff
    times = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff / target
    print(times / 600 / 2**40, "TH/s")


if __name__ == '__main__':
    # hashrate_calc()

    # print("total QTUM: ", coin_calc(10**8*COIN, 4*COIN, 0.0625*COIN, 985500) // COIN)
    # print(985500 * 128 / 60 / 60 / 24 / 365, 'year')
    # print(4 * 985500 / 4 / (10**8))
    #
    # print("total BTC: ", coin_calc(0, 50*COIN, 1, 210000) / COIN)
    # print(210000 * 10 / 60 / 24 / 365, 'year')

    blocks_per_year = 365 * 24 * 60 * 60 // 64
    total = coin_calc(7 * 10**8 * COIN, 70 * COIN, 0.0625*COIN, blocks_per_year * 4)
    print("total K: ", total / COIN)
    first_year = 70 * blocks_per_year
    print('first_year:', first_year, first_year/(7 * 10**8))
    print("reward:", 7 * 10**8 * 0.05 / (985500*2/4))






