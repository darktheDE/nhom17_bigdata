#!/usr/bin/env python3
"""
MapReduce Job 05: Rating by Brand
Mapper - Thu thập rating theo thương hiệu
Input: CSV file với cột brand và average_rating
Output: brand \t rating
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
            
            if len(fields) < 14:
                continue
            
            # brand là cột 5 (index 4), average_rating là cột 14 (index 13)
            brand = fields[4].strip().strip('"')
            rating_str = fields[13].strip().strip('"')
            
            if brand and brand != 'N/A' and rating_str and rating_str != 'N/A':
                rating = float(rating_str)
                
                # Emit: brand \t rating
                print(f"{brand}\t{rating}")
                
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    mapper()
