#!/usr/bin/env python3
"""
MapReduce Job 05: Rating by Brand
Reducer - Tính đánh giá trung bình theo thương hiệu
Input: brand \t rating
Output: brand \t avg_rating \t product_count
"""

import sys
from collections import defaultdict

def reducer():
    brand_data = defaultdict(lambda: {'total_rating': 0.0, 'count': 0})
    
    for line in sys.stdin:
        line = line.strip()
        
        try:
            brand, rating = line.split('\t')
            rating = float(rating)
            
            brand_data[brand]['total_rating'] += rating
            brand_data[brand]['count'] += 1
            
        except (ValueError, IndexError):
            continue
    
    # Xuất kết quả, sort theo avg_rating giảm dần
    results = []
    for brand, data in brand_data.items():
        count = data['count']
        avg_rating = data['total_rating'] / count if count > 0 else 0
        results.append((brand, avg_rating, count))
    
    # Sort theo avg_rating giảm dần
    for brand, avg_rating, count in sorted(results, key=lambda x: x[1], reverse=True):
        print(f"{brand}\t{avg_rating:.2f}\t{count}")

if __name__ == "__main__":
    reducer()
