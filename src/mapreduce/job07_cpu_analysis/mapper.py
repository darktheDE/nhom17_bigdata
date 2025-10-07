#!/usr/bin/env python3
"""
MapReduce Job 07: CPU Analysis
Mapper - Phân tích các loại CPU phổ biến
Input: CSV file với cột cpu và current_price
Output: cpu_family \t current_price
"""

import sys
import csv
import re

def extract_cpu_family(cpu_str):
    """Phân loại CPU thành các family chính"""
    if not cpu_str or cpu_str == 'N/A':
        return None
    
    cpu_str = cpu_str.upper()
    
    # Intel - cần check 'I' + số, không chỉ 'I5' vì có thể có format khác
    if 'CORE I3' in cpu_str or ' I3 ' in cpu_str or '-I3' in cpu_str or cpu_str.startswith('I3'):
        return 'Intel_i3'
    elif 'CORE I5' in cpu_str or ' I5 ' in cpu_str or '-I5' in cpu_str or cpu_str.startswith('I5'):
        return 'Intel_i5'
    elif 'CORE I7' in cpu_str or ' I7 ' in cpu_str or '-I7' in cpu_str or cpu_str.startswith('I7'):
        return 'Intel_i7'
    elif 'CORE I9' in cpu_str or ' I9 ' in cpu_str or '-I9' in cpu_str or cpu_str.startswith('I9'):
        return 'Intel_i9'
    
    # AMD Ryzen - check cả R + số và RYZEN + số
    elif 'RYZEN 3' in cpu_str or ' R3 ' in cpu_str or cpu_str.startswith('R3 '):
        return 'AMD_R3'
    elif 'RYZEN 5' in cpu_str or ' R5 ' in cpu_str or cpu_str.startswith('R5 '):
        return 'AMD_R5'
    elif 'RYZEN 7' in cpu_str or ' R7 ' in cpu_str or cpu_str.startswith('R7 '):
        return 'AMD_R7'
    elif 'RYZEN 9' in cpu_str or ' R9 ' in cpu_str or cpu_str.startswith('R9 '):
        return 'AMD_R9'
    
    # Apple Silicon
    elif 'M1' in cpu_str or 'M2' in cpu_str or 'M3' in cpu_str or 'M4' in cpu_str:
        return 'Apple_M_Series'
    
    # Other
    else:
        return 'Other'

def mapper():
    # Sử dụng csv.reader để parse đúng CSV có dấu phẩy trong trường
    reader = csv.reader(sys.stdin)
    
    # Đọc và bỏ qua header
    next(reader, None)
    
    for fields in reader:
        try:
            # Format: id,product_name,current_price,list_price,brand,category,cpu,...
            if len(fields) < 7:
                continue
            
            # cpu là cột 7 (index 6), current_price là cột 3 (index 2)
            cpu_str = fields[6].strip()
            price_str = fields[2].strip()
            
            cpu_family = extract_cpu_family(cpu_str)
            
            if cpu_family and price_str and price_str != 'N/A':
                price = float(price_str)
                
                # Emit: cpu_family \t price
                print(f"{cpu_family}\t{price}")
                
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    mapper()
