#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '.')

# Test mapper
with open(r'd:\HCMUTE\HCMUTE_HK5\BDES333877_BigData\nhom17_bigdata\data\sample\tgdd_promo.json', 'r', encoding='utf-8') as f:
    sys.stdin = f
    exec(open('mapper.py', 'r', encoding='utf-8').read())
