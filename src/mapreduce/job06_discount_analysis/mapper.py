#!/usr/bin/env python3
"""
MapReduce Job 06: Discount Analysis
Mapper - Phân tích mức giảm giá theo thương hiệu
Input: CSV file với cột brand, current_price, list_price
Output: brand \t discount_percent
"""

import sys

def mapper():
    for line in sys.stdin:
        line = line.strip()
        
        # Bỏ qua header
        if line.startswith('id,'):
            continue
        
        try:
            fields = line.split(',')
            
            if len(fields) < 5:
                continue
            
            # brand là cột 5 (index 4)
            # current_price là cột 3 (index 2)
            # list_price là cột 4 (index 3)
            brand = fields[4].strip().strip('"')
            current_price_str = fields[2].strip().strip('"')
            list_price_str = fields[3].strip().strip('"')
            
            if (brand and brand != 'N/A' and 
                current_price_str and current_price_str != 'N/A' and
                list_price_str and list_price_str != 'N/A'):
                
                current_price = float(current_price_str)
                list_price = float(list_price_str)
                
                # Tính % giảm giá
                if list_price > 0 and list_price > current_price:
                    discount_percent = ((list_price - current_price) / list_price) * 100
                    
                    # Emit: brand \t discount_percent
                    print(f"{brand}\t{discount_percent:.2f}")
                
        except (ValueError, IndexError, ZeroDivisionError):
            continue

if __name__ == "__main__":
    mapper()
