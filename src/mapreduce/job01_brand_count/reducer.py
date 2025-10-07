#!/usr/bin/env python3
"""
MapReduce Job 01: Brand Count
Reducer - Tổng hợp số lượng sản phẩm theo thương hiệu
Input: brand \t 1
Output: brand \t count
"""

import sys
from collections import defaultdict

def reducer():
    brand_counts = defaultdict(int)
    
    # Đọc từng dòng từ mapper
    for line in sys.stdin:
        line = line.strip()
        
        try:
            brand, count = line.split('\t')
            brand_counts[brand] += int(count)
        except:
            continue
    
    # Xuất kết quả
    for brand, count in sorted(brand_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{brand}\t{count}")

if __name__ == "__main__":
    reducer()
