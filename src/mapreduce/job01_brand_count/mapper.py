#!/usr/bin/env python3
"""
MapReduce Job 01: Brand Count
Mapper - Đếm số lượng sản phẩm theo thương hiệu
Input: CSV file với cột brand
Output: brand \t 1
"""

import sys

def mapper():
    # Đọc từng dòng từ stdin
    for line in sys.stdin:
        line = line.strip()
        
        # Bỏ qua dòng header
        if line.startswith('id,'):
            continue
        
        try:
            # Parse CSV line
            # Format: id,product_name,current_price,list_price,brand,...
            fields = line.split(',')
            
            if len(fields) < 5:
                continue
            
            # Brand là cột thứ 5 (index 4)
            brand = fields[4].strip().strip('"')
            
            if brand and brand != '' and brand != 'N/A':
                # Emit: brand \t 1
                print(f"{brand}\t1")
                
        except Exception as e:
            # Bỏ qua dòng lỗi
            continue

if __name__ == "__main__":
    mapper()
