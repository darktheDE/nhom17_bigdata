#!/usr/bin/env python3
"""
MapReduce Job 01: Brand Count
Mapper - Đếm số lượng sản phẩm theo thương hiệu
Input: CSV file với cột brand
Output: brand \t 1
"""

import sys
import csv

def mapper():
    # Sử dụng csv.reader để parse đúng CSV có dấu phẩy trong trường
    reader = csv.reader(sys.stdin)
    
    # Đọc và bỏ qua header
    next(reader, None)
    
    for fields in reader:
        try:
            # Format: id,product_name,current_price,list_price,brand,...
            if len(fields) < 5:
                continue
            
            # Brand là cột thứ 5 (index 4)
            brand = fields[4].strip()
            
            if brand and brand != '' and brand != 'N/A':
                # Emit: brand \t 1
                print(f"{brand}\t1")
                
        except Exception as e:
            # Bỏ qua dòng lỗi
            continue

if __name__ == "__main__":
    mapper()
