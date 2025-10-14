#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 03 - Reducer
Đếm số lượng sản phẩm trong từng khoảng giá
"""

import sys

def main():
    current_range = None
    count = 0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            price_range, value = line.split('\t')
            value = int(value)
            
            if current_range == price_range:
                count += value
            else:
                if current_range is not None:
                    print(f"{current_range}\t{count}")
                current_range = price_range
                count = value
                
        except Exception:
            continue
    
    if current_range is not None:
        print(f"{current_range}\t{count}")

if __name__ == '__main__':
    main()
