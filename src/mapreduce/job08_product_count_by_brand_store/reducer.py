#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 14 - Reducer
Nhiệm vụ: Đếm tổng số sản phẩm cho mỗi cặp (brand, source)
Đầu vào: brand,source \t 1 (đã được sort theo brand,source)
Đầu ra: brand \t source \t product_count
"""

import sys

def main():
    """
    Hàm chính của Reducer
    Nhận dữ liệu đã được sort theo composite key, đếm số lượng
    """
    current_key = None
    count = 0
    
    # Đọc từng dòng từ stdin (output của mapper đã được sort)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            # Tách composite key và value
            key, value = line.split('\t')
            value = int(value)
            
            if current_key == key:
                # Cùng key với dòng trước => cộng dồn
                count += value
            else:
                # Gặp key mới => xuất kết quả của key trước đó
                if current_key is not None:
                    # Tách brand và source từ composite key
                    brand, source = current_key.split(',')
                    print(f"{brand}\t{source}\t{count}")
                
                # Reset cho key mới
                current_key = key
                count = value
        
        except ValueError:
            # Bỏ qua dòng lỗi định dạng
            continue
    
    # Xuất kết quả của key cuối cùng
    if current_key is not None:
        brand, source = current_key.split(',')
        print(f"{brand}\t{source}\t{count}")

if __name__ == '__main__':
    main()
