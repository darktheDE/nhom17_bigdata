#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 05 - Reducer
Nhiệm vụ: Lấy top 5 laptop có tỷ lệ giảm giá cao nhất
Đầu vào: discount_percent \t product_info (đã được sort giảm dần)
Đầu ra: rank \t product_name \t discount% \t current_price \t list_price \t brand
"""

import sys
import io

def main():
    """
    Hàm chính của Reducer
    
    Chiến lược Top-N:
    1. Hadoop đã sort theo discount_percent (giảm dần)
    2. Đọc tuần tự và chỉ lấy 5 records đầu tiên
    3. Output với rank (1-5)
    """
    # Thiết lập encoding UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    if hasattr(sys.stdin, 'buffer'):
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    
    # Đếm rank
    rank = 0
    
    # Đọc từng dòng từ stdin (đã được sort)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        # Parse dòng: discount_percent \t product_info
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        
        discount_percent_str, product_info = parts
        
        # Parse product_info: name|current_price|list_price|brand
        info_parts = product_info.split('|')
        if len(info_parts) != 4:
            continue
        
        product_name, current_price, list_price, brand = info_parts
        
        # Tăng rank
        rank += 1
        
        # Chuyển discount_percent về dạng số
        try:
            discount_percent = float(discount_percent_str)
        except ValueError:
            continue
        
        # Output: rank \t product_name \t discount% \t current_price \t list_price \t brand
        output = f"{rank}\t{product_name}\t{discount_percent:.2f}%\t{current_price}\t{list_price}\t{brand}"
        print(output)
        sys.stdout.flush()
        
        # QUAN TRỌNG: Chỉ lấy top 5
        if rank >= 5:
            break

if __name__ == '__main__':
    main()
