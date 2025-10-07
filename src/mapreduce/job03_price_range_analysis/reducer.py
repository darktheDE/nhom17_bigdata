#!/usr/bin/env python3
"""
MapReduce Job 03: Price Range Analysis
Reducer - Tổng hợp thống kê theo phân khúc giá
Input: price_range \t current_price
Output: price_range \t count \t avg_price
"""

import sys
from collections import defaultdict

def reducer():
    price_data = defaultdict(lambda: {'count': 0, 'total': 0.0})
    
    for line in sys.stdin:
        line = line.strip()
        
        try:
            price_range, price = line.split('\t')
            price = float(price)
            
            price_data[price_range]['count'] += 1
            price_data[price_range]['total'] += price
            
        except (ValueError, IndexError):
            continue
    
    # Xuất kết quả (sort theo thứ tự phân khúc giá)
    order = ["Under_15M_Budget", "15-25M_Mid-range", "25-35M_Premium", "Above_35M_High-end"]
    
    for price_range in order:
        if price_range in price_data:
            data = price_data[price_range]
            count = data['count']
            avg_price = data['total'] / count if count > 0 else 0
            
            print(f"{price_range}\t{count}\t{avg_price:.0f}")

if __name__ == "__main__":
    reducer()
