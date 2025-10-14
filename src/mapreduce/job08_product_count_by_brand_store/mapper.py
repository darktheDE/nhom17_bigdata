#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 14 - Mapper
Nhiệm vụ: Đếm số lượng sản phẩm của từng thương hiệu tại mỗi cửa hàng
Đầu vào: CSV files (tgdd.csv, cellphones.csv)
Đầu ra: brand,source \t 1
"""

import sys
import csv
import os

def extract_brand(product_name):
    """
    Trích xuất tên hãng sản xuất từ tên sản phẩm
    """
    if not product_name:
        return None
    
    # Aliases mapping
    aliases = {
        'vivobook': 'Asus',
        'ideapad': 'Lenovo',
        'thinkpad': 'Lenovo',
        'thinkbook': 'Lenovo',
        'pavilion': 'HP',
        'elitebook': 'HP',
        'probook': 'HP',
        'victus': 'HP',
        'inspiron': 'Dell',
        'latitude': 'Dell',
        'vostro': 'Dell',
        'xps': 'Dell',
        'precision': 'Dell',
        'aspire': 'Acer',
        'swift': 'Acer',
        'nitro': 'Acer',
        'predator': 'Acer',
        'macbook': 'MacBook',
        'katana': 'MSI',
        'prestige': 'MSI',
        'modern': 'MSI',
        'gaming': 'MSI',
        'stealth': 'MSI',
        'rog': 'Asus',
        'tuf': 'Asus',
        'zenbook': 'Asus',
        'gram': 'LG',
        'surface': 'Microsoft',
        'gigabyte': 'Gigabyte'
    }
    
    # Tách từ
    words = product_name.split()
    if len(words) < 2:
        return words[0] if words else None
    
    # Bỏ qua "Laptop" nếu là từ đầu tiên
    start_idx = 1 if words[0].lower() == 'laptop' else 0
    
    if start_idx < len(words):
        potential_brand = words[start_idx]
        
        # Kiểm tra alias
        for key, value in aliases.items():
            if key in potential_brand.lower():
                return value
        
        return potential_brand
    
    return None

def detect_source_from_url(url):
    """
    Xác định nguồn từ URL sản phẩm
    """
    if 'thegioididong.com' in url:
        return 'thegioididong'
    elif 'cellphones.com.vn' in url:
        return 'cellphones'
    return 'unknown'

def main():
    """
    Hàm chính của Mapper
    Đọc file CSV, trích xuất brand và source, xuất composite key
    """
    # Đọc từ stdin
    reader = csv.DictReader(sys.stdin)
    
    for row in reader:
        # Lấy thông tin
        product_name = row.get('product_name', '')
        brand_col = row.get('brand', '')
        product_url = row.get('product_url', '')
        
        # Xác định brand
        if brand_col and brand_col != 'N/A':
            brand = brand_col
        else:
            brand = extract_brand(product_name)
        
        # Xác định source từ URL
        source = detect_source_from_url(product_url)
        
        if brand and source != 'unknown':
            # Xuất composite key: brand,source \t 1
            print(f"{brand},{source}\t1")

if __name__ == '__main__':
    main()
