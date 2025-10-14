#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 06 - Reducer
Nhiệm vụ: Tính số khuyến mãi trung bình mỗi cửa hàng
Đầu vào: store_name \t num_promotions (đã sort theo store_name)
Đầu ra: store_name \t avg_promotions \t total_products
"""

import sys
import io
from itertools import groupby

def main():
    """
    Hàm chính của Reducer
    
    Chiến lược:
    1. Group theo store_name (Hadoop đã sort)
    2. Với mỗi store: sum promotions và count products
    3. Tính average = total_promotions / total_products
    """
    # Thiết lập encoding UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    if hasattr(sys.stdin, 'buffer'):
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    
    # Đọc và parse stdin
    data = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split('\t')
        if len(parts) != 2:
            continue
        
        store_name, num_promotions_str = parts
        
        try:
            num_promotions = int(num_promotions_str)
            data.append((store_name, num_promotions))
        except ValueError:
            continue
    
    # Group by store_name
    # Sort trước khi group (để groupby hoạt động đúng)
    data.sort(key=lambda x: x[0])
    
    for store_name, group in groupby(data, key=lambda x: x[0]):
        # Chuyển group thành list để tính toán
        promotions_list = [num_promo for _, num_promo in group]
        
        # Tính tổng và đếm sản phẩm
        total_promotions = sum(promotions_list)
        total_products = len(promotions_list)
        
        # Tính average
        avg_promotions = total_promotions / total_products if total_products > 0 else 0
        
        # Output: store_name \t avg_promotions \t total_products
        print(f"{store_name}\t{avg_promotions:.2f}\t{total_products}")
        sys.stdout.flush()

if __name__ == '__main__':
    main()
