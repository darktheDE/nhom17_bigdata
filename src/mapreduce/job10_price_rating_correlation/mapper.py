#!/usr/bin/env python3
"""
MapReduce Job 10: Price-Rating Correlation
Mapper - Phân tích mối tương quan giữa giá và đánh giá
Input: CSV file với cột current_price và average_rating
Output: price_range \t rating
"""

import sys

def get_price_range(price):
    """Phân loại giá vào các phân khúc"""
    if price < 15000000:
        return "Under_15M"
    elif price < 25000000:
        return "15-25M"
    elif price < 35000000:
        return "25-35M"
    else:
        return "Above_35M"

def mapper():
    for line in sys.stdin:
        line = line.strip()
        
        # Bỏ qua header
        if line.startswith('id,'):
            continue
        
        try:
            fields = line.split(',')
            
            if len(fields) < 14:
                continue
            
            # current_price là cột 3 (index 2), average_rating là cột 14 (index 13)
            price_str = fields[2].strip().strip('"')
            rating_str = fields[13].strip().strip('"')
            
            if (price_str and price_str != 'N/A' and 
                rating_str and rating_str != 'N/A'):
                
                price = float(price_str)
                rating = float(rating_str)
                
                price_range = get_price_range(price)
                
                # Emit: price_range \t rating
                print(f"{price_range}\t{rating}")
                
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    mapper()
