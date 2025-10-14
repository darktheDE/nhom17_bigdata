#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Job 10 - Reducer: Sum cash discounts by brand"""
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
            brand, amount = parts
            data.append((brand, int(amount)))

data.sort(key=lambda x: x[0])

for brand, group in groupby(data, key=lambda x: x[0]):
    total = sum(amt for _, amt in group)
    count = len(list(groupby(data, key=lambda x: x[0] == brand)))
    
    # Format: brand \t total_discount \t (formatted)
    formatted = f"{total:,}đ".replace(',', '.')
    print(f"{brand}\t{total}\t{formatted}")
