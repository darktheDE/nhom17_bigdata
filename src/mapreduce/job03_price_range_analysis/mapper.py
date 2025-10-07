#!/usr/bin/env python3
"""
MapReduce Job 03: Price Range Analysis
Mapper - Phân loại laptop theo phân khúc giá
Input: CSV file với cột current_price
Output: price_range \t current_price
"""

import sys

def get_price_range(price):
    """Phân loại giá vào các phân khúc"""
    if price < 15000000:
        return "Under_15M_Budget"
    elif price < 25000000:
        return "15-25M_Mid-range"
    elif price < 35000000:
        return "25-35M_Premium"
    else:
        return "Above_35M_High-end"

def mapper():
    for line in sys.stdin:
        line = line.strip()
        
        # Bỏ qua header
        if line.startswith('id,'):
            continue
        
        try:
            fields = line.split(',')
            
            if len(fields) < 3:
                continue
            
            # current_price là cột thứ 3 (index 2)
            current_price_str = fields[2].strip().strip('"')
            
            if current_price_str and current_price_str != 'N/A':
                current_price = float(current_price_str)
                price_range = get_price_range(current_price)
                
                # Emit: price_range \t current_price
                print(f"{price_range}\t{current_price}")
                
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    mapper()
