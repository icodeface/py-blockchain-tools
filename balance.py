#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'CodeFace'
"""
import csv


def run(path):
    total = 0
    with open(path) as f:
        r = csv.reader(f)
        count = 0
        for row in r:
            if count == 0:
                count += 1
                continue
            count += 1
            total += float(row[5])
    print(total)


run('/Users/face/Desktop/20191114wallet record.csv')