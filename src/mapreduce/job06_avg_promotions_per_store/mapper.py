#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 06 - Mapper
Nhiệm vụ: So sánh số khuyến mãi trung bình giữa TGDĐ và CellphoneS
Đầu vào: JSON files (tgdd_promo.json, cellphones_promo.json)
Đầu ra: store_name \t num_promotions
"""

import sys
import json
import os

def detect_store_from_filename(filename):
    """
    Phát hiện tên cửa hàng từ tên file
    
    Tham số:
        filename (str): Tên file JSON
    
    Trả về:
        str: "TGDĐ" hoặc "CellphoneS"
    """
    filename_lower = filename.lower()
    
    if 'tgdd' in filename_lower or 'thegioididong' in filename_lower:
        return "TGDĐ"
    elif 'cellphone' in filename_lower:
        return "CellphoneS"
    else:
        return "Unknown"

def main():
    """
    Hàm chính của Mapper
    Đọc JSON, đếm số khuyến mãi mỗi sản phẩm, xuất: store \t count
    
    Chiến lược:
    1. Đọc JSON file (biết store từ tên file hoặc từ field trong data)
    2. Với mỗi sản phẩm, đếm số phần tử trong mảng promotions
    3. Xuất: store_name \t num_promotions (mỗi sản phẩm 1 dòng)
    """
    # Thiết lập encoding UTF-8
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    if hasattr(sys.stdin, 'buffer'):
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    
    # Đọc toàn bộ stdin (JSON file)
    try:
        content = sys.stdin.read()
        
        # Parse JSON
        data = json.loads(content)
        
        # Chuyển thành array nếu cần
        if not isinstance(data, list):
            data = [data]
        
        # Phát hiện store từ dữ liệu
        # Giả sử: nếu có field 'source' trong JSON, dùng nó
        # Nếu không, phải detect từ context (file name được pass qua env var)
        
        # Cách 1: Từ data (nếu có field 'source')
        store_name = None
        if len(data) > 0 and isinstance(data[0], dict):
            # Kiểm tra các field có thể chứa thông tin store
            first_item = data[0]
            if 'source' in first_item:
                store_name = first_item['source']
            elif 'store' in first_item:
                store_name = first_item['store']
        
        # Cách 2: Từ environment variable (được set trong run_local.py)
        if not store_name:
            store_name = os.environ.get('STORE_NAME', 'Unknown')
        
        # Xử lý từng sản phẩm
        for item in data:
            if not isinstance(item, dict):
                continue
            
            # Lấy mảng promotions
            promotions = item.get('promotions', [])
            
            # Đếm số khuyến mãi
            num_promotions = len(promotions) if isinstance(promotions, list) else 0
            
            # Xuất: store_name \t num_promotions
            print(f"{store_name}\t{num_promotions}")
            sys.stdout.flush()
    
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Lỗi parse JSON: {e}\n")
    except Exception as e:
        sys.stderr.write(f"Lỗi: {e}\n")

if __name__ == '__main__':
    main()
