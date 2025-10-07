#!/usr/bin/env python3
"""
MapReduce Job 09: OS Distribution
Mapper - Phân tích phân bố hệ điều hành
Input: CSV file với cột os và current_price
Output: os \t current_price
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
            # Format: id,product_name,current_price,list_price,brand,category,cpu,ram,storage,screen_size,screen_resolution,os,...
            if len(fields) < 12:
                continue
            
            # os là cột 12 (index 11), current_price là cột 3 (index 2)
            os = fields[11].strip()
            price_str = fields[2].strip()
            
            if os and os != 'N/A' and price_str and price_str != 'N/A':
                price = float(price_str)
                
                # Chuẩn hóa OS name
                os = os.replace(' ', '_')
                
                # Emit: os \t price
                print(f"{os}\t{price}")
                
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    mapper()
