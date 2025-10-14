#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 04 - Reducer
Nhiệm vụ: Đếm tổng số lần xuất hiện của mỗi từ khóa khuyến mãi
Đầu vào: keyword \t 1 (đã được sort theo keyword)
Đầu ra: keyword \t frequency
"""

import sys

def main():
    """
    Hàm chính của Reducer
    Nhận dữ liệu đã sort theo keyword, tính tổng số lần xuất hiện
    """
    current_keyword = None  # Từ khóa hiện tại đang xử lý
    count = 0               # Số lần xuất hiện của từ khóa hiện tại
    
    # Đọc từng dòng từ stdin (output của mapper đã được sort)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            # Tách keyword và value (luôn là 1)
            keyword, value = line.split('\t')
            value = int(value)
            
            if current_keyword == keyword:
                # Cùng keyword => tăng bộ đếm
                count += value
            else:
                # Gặp keyword mới => xuất kết quả của keyword trước
                if current_keyword is not None:
                    print(f"{current_keyword}\t{count}")
                
                # Reset cho keyword mới
                current_keyword = keyword
                count = value
                
        except Exception as e:
            # Bỏ qua dòng lỗi
            continue
    
    # Xuất kết quả của keyword cuối cùng
    if current_keyword is not None:
        print(f"{current_keyword}\t{count}")

if __name__ == '__main__':
    main()
