#!/usr/bin/env python3
"""
MapReduce Job 07: CPU Analysis
Reducer - Tổng hợp thống kê theo CPU family
Input: cpu_family \t price
Output: cpu_family \t count \t avg_price
"""

import sys
from collections import defaultdict

def reducer():
    cpu_data = defaultdict(lambda: {'total_price': 0.0, 'count': 0})
    
    for line in sys.stdin:
        line = line.strip()
        
        try:
            cpu_family, price = line.split('\t')
            price = float(price)
            
            cpu_data[cpu_family]['total_price'] += price
            cpu_data[cpu_family]['count'] += 1
            
        except (ValueError, IndexError):
            continue
    
    # Xuất kết quả, sort theo count giảm dần
    results = []
    for cpu_family, data in cpu_data.items():
        count = data['count']
        avg_price = data['total_price'] / count if count > 0 else 0
        results.append((cpu_family, count, avg_price))
    
    # Sort theo count giảm dần
    for cpu_family, count, avg_price in sorted(results, key=lambda x: x[1], reverse=True):
        print(f"{cpu_family}\t{count}\t{avg_price:.0f}")

if __name__ == "__main__":
    reducer()
