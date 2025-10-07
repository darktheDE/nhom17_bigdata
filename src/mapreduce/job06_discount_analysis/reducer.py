#!/usr/bin/env python3
"""
MapReduce Job 06: Discount Analysis
Reducer - Tính mức giảm giá trung bình và max theo thương hiệu
Input: brand \t discount_percent
Output: brand \t avg_discount_percent \t max_discount_percent
"""

import sys
from collections import defaultdict

def reducer():
    brand_data = defaultdict(lambda: {'total_discount': 0.0, 'count': 0, 'max_discount': 0.0})
    
    for line in sys.stdin:
        line = line.strip()
        
        try:
            brand, discount = line.split('\t')
            discount = float(discount)
            
            brand_data[brand]['total_discount'] += discount
            brand_data[brand]['count'] += 1
            brand_data[brand]['max_discount'] = max(brand_data[brand]['max_discount'], discount)
            
        except (ValueError, IndexError):
            continue
    
    # Xuất kết quả, sort theo avg_discount giảm dần
    results = []
    for brand, data in brand_data.items():
        count = data['count']
        avg_discount = data['total_discount'] / count if count > 0 else 0
        max_discount = data['max_discount']
        results.append((brand, avg_discount, max_discount))
    
    # Sort theo avg_discount giảm dần
    for brand, avg_discount, max_discount in sorted(results, key=lambda x: x[1], reverse=True):
        print(f"{brand}\t{avg_discount:.2f}%\t{max_discount:.2f}%")

if __name__ == "__main__":
    reducer()
