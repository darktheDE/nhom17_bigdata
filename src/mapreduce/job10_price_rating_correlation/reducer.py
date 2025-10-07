#!/usr/bin/env python3
"""
MapReduce Job 10: Price-Rating Correlation
Reducer - Tính đánh giá trung bình theo phân khúc giá
Input: price_range \t rating
Output: price_range \t avg_rating \t product_count
"""

import sys
from collections import defaultdict

def reducer():
    price_data = defaultdict(lambda: {'total_rating': 0.0, 'count': 0})
    
    for line in sys.stdin:
        line = line.strip()
        
        try:
            price_range, rating = line.split('\t')
            rating = float(rating)
            
            price_data[price_range]['total_rating'] += rating
            price_data[price_range]['count'] += 1
            
        except (ValueError, IndexError):
            continue
    
    # Xuất kết quả theo thứ tự phân khúc giá
    order = ["Under_15M", "15-25M", "25-35M", "Above_35M"]
    
    for price_range in order:
        if price_range in price_data:
            data = price_data[price_range]
            count = data['count']
            avg_rating = data['total_rating'] / count if count > 0 else 0
            
            print(f"{price_range}\t{avg_rating:.2f}\t{count}")

if __name__ == "__main__":
    reducer()
