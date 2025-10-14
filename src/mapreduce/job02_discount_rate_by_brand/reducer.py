#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 02 - Reducer
Tính tỷ lệ giảm giá trung bình theo từng hãng sản xuất
"""

import sys

def main():
    current_brand = None
    total_discount = 0
    count = 0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            brand, discount = line.split('\t')
            discount = float(discount)
            
            if current_brand == brand:
                # Same brand, accumulate
                total_discount += discount
                count += 1
            else:
                # New brand, output previous result
                if current_brand is not None:
                    avg_discount = total_discount / count
                    print(f"{current_brand}\t{avg_discount:.2f}%")
                
                # Reset for new brand
                current_brand = brand
                total_discount = discount
                count = 1
                
        except Exception as e:
            continue
    
    # Output last brand
    if current_brand is not None:
        avg_discount = total_discount / count
        print(f"{current_brand}\t{avg_discount:.2f}%")

if __name__ == '__main__':
    main()
