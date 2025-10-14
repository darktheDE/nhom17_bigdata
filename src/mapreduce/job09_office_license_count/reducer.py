#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Job 09 - Reducer: Sum counts"""
import sys, io
from itertools import groupby

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stdin, 'buffer'):
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

data = []
for line in sys.stdin:
    line = line.strip()
    if line:
        parts = line.split('\t')
        if len(parts) == 2:
            category, count = parts
            data.append((category, int(count)))

data.sort(key=lambda x: x[0])

for category, group in groupby(data, key=lambda x: x[0]):
    total = sum(count for _, count in group)
    print(f"{category}\t{total}")
