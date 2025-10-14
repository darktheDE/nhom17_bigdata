#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 02 - Mapper
Nhiệm vụ: Tính tỷ lệ giảm giá trung bình theo từng hãng
Công thức: discount% = ((list_price - current_price) / list_price) * 100
Đầu vào: CSV files (có current_price và list_price)
Đầu ra: brand \t discount_percentage
"""

import sys
import csv
import io

def clean_price(price_str):
    """
    Chuyển đổi giá từ chuỗi sang số
    CellphoneS: "22.990.000đ" -> 22990000
    TGDD: "13190000.0" -> 13190000
    """
    if not price_str or price_str == 'N/A' or 'Liên hệ' in price_str:
        return None
    
    # Remove 'đ' and dots, then convert to float
    price_cleaned = price_str.replace('đ', '').replace('.', '').replace(',', '').strip()
    try:
        return float(price_cleaned)
    except ValueError:
        return None

def extract_brand(product_name):
    """
    Trích xuất tên thương hiệu từ tên sản phẩm
    
    Chiến lược SCALABLE:
    1. Bỏ qua từ "Laptop" ở đầu nếu có
    2. Lấy từ tiếp theo làm brand
    3. CHỈ normalize các model/series → parent brand (không filter)
    4. GIỮ NGUYÊN brand không nằm trong danh sách → tránh mất data
    
    Ví dụ:
    - "Laptop HP Pavilion" → "Hp"
    - "Vivobook S15" → "Asus" (normalize)
    - "XYZ Gaming" → "Xyz" (brand mới, giữ nguyên)
    """
    if not product_name:
        return "Unknown"
    
    words = product_name.split()
    
    # Bỏ qua từ "Laptop" ở đầu
    if len(words) >= 2 and words[0].lower() == 'laptop':
        brand_word = words[1].strip()
    else:
        brand_word = words[0].strip() if words else "Unknown"
    
    # Danh sách ALIAS: model/series → parent brand (KHÔNG phải whitelist)
    brand_aliases = {
        'vivobook': 'Asus',
        'zenbook': 'Asus',
        'tuf': 'Asus',
        'rog': 'Asus',
        'ideapad': 'Lenovo',
        'thinkpad': 'Lenovo',
        'legion': 'Lenovo',
        'yoga': 'Lenovo',
        'pavilion': 'HP',
        'envy': 'HP',
        'omen': 'HP',
        'victus': 'HP',
        'inspiron': 'Dell',
        'latitude': 'Dell',
        'xps': 'Dell',
        'alienware': 'Dell',
        'macbook': 'MacBook',
        'mac': 'MacBook',
        'aspire': 'Acer',
        'predator': 'Acer',
        'nitro': 'Acer',
        'prestige': 'MSI',
        'katana': 'MSI',
        'g6': 'Gigabyte',
        'v16': 'Asus'
    }
    
    # Normalize nếu là alias, GIỮ NGUYÊN nếu không
    brand = brand_aliases.get(brand_word.lower(), brand_word)
    
    return brand

def main():
    # Setup stdin encoding for Hadoop Streaming compatibility
    import io
    if hasattr(sys.stdin, 'buffer'):
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    
    reader = csv.DictReader(sys.stdin)
    
    for row in reader:
        try:
            # Extract product_name
            product_name = row.get('product_name', '')
            
            # Get current_price and list_price
            current_price_raw = row.get('current_price') or row.get('current_price_raw', '')
            list_price_raw = row.get('list_price') or row.get('list_price_raw', '')
            
            # Clean prices
            current_price = clean_price(current_price_raw)
            list_price = clean_price(list_price_raw)
            
            # Skip if missing prices or no discount
            if current_price is None or list_price is None or list_price == 0:
                continue
            
            # Calculate discount percentage
            discount_percentage = ((list_price - current_price) / list_price) * 100
            
            # Skip if no discount
            if discount_percentage <= 0:
                continue
            
            # Extract brand
            brand = row.get('brand', '').strip()
            if not brand:
                brand = extract_brand(product_name)
            
            # Output: brand \t discount_percentage
            print(f"{brand}\t{discount_percentage:.2f}")
            
        except Exception as e:
            # Skip problematic rows
            continue

if __name__ == '__main__':
    main()
