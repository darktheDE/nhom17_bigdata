#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 01 - Reducer
Nhiệm vụ: Tính giá bán trung bình cho mỗi hãng
Đầu vào: brand \t price (đã được sort theo brand)
Đầu ra: brand \t average_price
"""

import sys

def main():
    """
    Hàm chính của Reducer
    Nhận dữ liệu đã được sort theo brand, tính tổng và trung bình giá
    """
    current_brand = None  # Hãng hiện tại đang xử lý
    total_price = 0       # Tổng giá của hãng hiện tại
    count = 0             # Số lượng sản phẩm của hãng hiện tại
    
    # Đọc từng dòng từ stdin (output của mapper đã được sort)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            # Tách brand và price từ mỗi dòng
            brand, price = line.split('\t')
            price = float(price)
            
            if current_brand == brand:
                # Cùng hãng với dòng trước => cộng dồn
                total_price += price
                count += 1
            else:
                # Gặp hãng mới => xuất kết quả của hãng trước đó
                if current_brand is not None:
                    avg_price = total_price / count
                    print(f"{current_brand}\t{avg_price:.2f}")
                
                # Reset để bắt đầu tính cho hãng mới
                current_brand = brand
                total_price = price
                count = 1
                
        except Exception as e:
            # Bỏ qua dòng lỗi
            continue
    
    # Xuất kết quả của hãng cuối cùng
    if current_brand is not None:
        avg_price = total_price / count
        print(f"{current_brand}\t{avg_price:.2f}")

if __name__ == '__main__':
    main()
