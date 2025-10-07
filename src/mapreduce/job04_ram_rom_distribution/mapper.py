#!/usr/bin/env python3
"""
MapReduce Job 04: RAM/Storage Distribution
Mapper - Phân tích phân bố cấu hình RAM và Storage
Input: CSV file với cột ram và storage
Output: ram_storage_config \t 1
"""

import sys
import csv
import re

def extract_capacity(value):
    """Extract số từ chuỗi dạng '16GB', '512GB', '1TB'"""
    if not value or value == 'N/A':
        return None
    
    value = value.upper().strip()
    match = re.search(r'(\d+)\s*(GB|TB|MB)', value)
    
    if match:
        num = int(match.group(1))
        unit = match.group(2)
        
        # Chuẩn hóa về GB
        if unit == 'TB':
            num = num * 1024
        elif unit == 'MB':
            num = num / 1024
            
        return num
    return None

def mapper():
    # Sử dụng csv.reader để parse đúng CSV có dấu phẩy trong trường
    reader = csv.reader(sys.stdin)
    
    # Đọc và bỏ qua header
    next(reader, None)
    
    for fields in reader:
        try:
            # Format: id,product_name,current_price,list_price,brand,category,cpu,ram,storage,...
            if len(fields) < 9:
                continue
            
            # ram là cột 8 (index 7), storage là cột 9 (index 8)
            ram_str = fields[7].strip()
            storage_str = fields[8].strip()
            
            ram = extract_capacity(ram_str)
            storage = extract_capacity(storage_str)
            
            if ram and storage:
                # Format: RAM_STORAGE (e.g., 16GB_512GB)
                ram_label = f"{int(ram)}GB" if ram < 1024 else f"{int(ram/1024)}TB"
                storage_label = f"{int(storage)}GB" if storage < 1024 else f"{int(storage/1024)}TB"
                
                config = f"{ram_label}_{storage_label}"
                print(f"{config}\t1")
                
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    mapper()
