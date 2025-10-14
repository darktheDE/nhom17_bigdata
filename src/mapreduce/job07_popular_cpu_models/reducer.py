#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 11 - Reducer
Nhiệm vụ: Đếm số lượng xuất hiện của mỗi dòng CPU
Đầu vào: cpu_model \t 1 (đã được sort theo cpu_model)
Đầu ra: cpu_model \t total_count
"""

import sys

def main():
    """
    Hàm chính của Reducer
    Nhận dữ liệu đã được sort theo cpu_model, đếm tổng số lần xuất hiện
    """
    current_cpu = None
    count = 0
    
    # Đọc từng dòng từ stdin (output của mapper đã được sort)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            # Tách cpu_model và count
            cpu_model, value = line.split('\t')
            value = int(value)
            
            if current_cpu == cpu_model:
                # Cùng CPU với dòng trước => cộng dồn
                count += value
            else:
                # Gặp CPU mới => xuất kết quả của CPU trước đó
                if current_cpu is not None:
                    print(f"{current_cpu}\t{count}")
                
                # Reset cho CPU mới
                current_cpu = cpu_model
                count = value
        
        except ValueError:
            # Bỏ qua dòng lỗi định dạng
            continue
    
    # Xuất kết quả của CPU cuối cùng
    if current_cpu is not None:
        print(f"{current_cpu}\t{count}")

if __name__ == '__main__':
    main()
