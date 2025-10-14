#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 03 - Mapper
Nhiệm vụ: Đếm số lượng sản phẩm trong từng khoảng giá
Phân khúc: Dưới 15M, 15-25M, Trên 25M
Đầu vào: CSV files (có current_price)
Đầu ra: price_range \t 1
"""

import sys
import csv

def clean_price(price_str):
    """Làm sạch giá từ string sang số"""
    if not price_str or price_str == 'N/A' or 'Liên hệ' in price_str:
        return None
    price_cleaned = price_str.replace('đ', '').replace('.', '').replace(',', '').strip()
    try:
        return float(price_cleaned)
    except ValueError:
        return None

def get_price_range(price):
    """
    Phân loại giá vào các khoảng
    
    Tham số:
        price (float): Giá sản phẩm (VND)
    
    Trả về:
        str: Tên khoảng giá
    """
    price_m = price / 1000000  # Chuyển đổi sang triệu VND
    
    if price_m < 15:
        return "Duoi_15_trieu"
    elif price_m < 25:
        return "15_25_trieu"
    else:
        return "Tren_25_trieu"

def main():
    """
    Hàm chính của Mapper
    Đọc CSV, phân loại giá vào khoảng, xuất ra: price_range \t 1
    """
    # Thiết lập encoding UTF-8 cho Hadoop Streaming
    import io
    if hasattr(sys.stdin, 'buffer'):
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    
    reader = csv.DictReader(sys.stdin)
    
    for row in reader:
        try:
            # Lấy giá hiện tại (xử lý cả 2 tên cột)
            current_price_raw = row.get('current_price') or row.get('current_price_raw', '')
            price = clean_price(current_price_raw)
            
            # Bỏ qua sản phẩm không có giá
            if price is None:
                continue
            
            # Phân loại vào khoảng giá
            price_range = get_price_range(price)
            
            # Xuất: khoảng_giá \t 1 (để reducer đếm)
            print(f"{price_range}\t1")
            
        except Exception:
            continue

if __name__ == '__main__':
    main()
