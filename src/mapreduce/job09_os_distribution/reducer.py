#!/usr/bin/env python3
"""
MapReduce Job 09: OS Distribution
Reducer - Tổng hợp phân bố hệ điều hành
Input: os \t price
Output: os \t count \t market_share_percent \t avg_price
"""

import sys
from collections import defaultdict

def reducer():
    os_data = defaultdict(lambda: {'total_price': 0.0, 'count': 0})
    
    # First pass: collect data
    for line in sys.stdin:
        line = line.strip()
        
        try:
            os, price = line.split('\t')
            price = float(price)
            
            os_data[os]['total_price'] += price
            os_data[os]['count'] += 1
            
        except (ValueError, IndexError):
            continue
    
    # Calculate total count for market share
    total_count = sum(data['count'] for data in os_data.values())
    
    # Xuất kết quả, sort theo count giảm dần
    results = []
    for os, data in os_data.items():
        count = data['count']
        avg_price = data['total_price'] / count if count > 0 else 0
        market_share = (count / total_count * 100) if total_count > 0 else 0
        results.append((os, count, market_share, avg_price))
    
    # Sort theo count giảm dần
    for os, count, market_share, avg_price in sorted(results, key=lambda x: x[1], reverse=True):
        print(f"{os}\t{count}\t{market_share:.1f}%\t{avg_price:.0f}")

if __name__ == "__main__":
    reducer()
