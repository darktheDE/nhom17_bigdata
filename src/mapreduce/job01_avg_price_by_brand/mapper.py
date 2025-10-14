#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 01 - Mapper
Nhiệm vụ: Tính giá bán trung bình theo từng hãng sản xuất laptop
Đầu vào: CSV files (tgdd.csv, cellphones.csv)
Đầu ra: brand \t price
"""

import sys
import csv
import re

def clean_price(price_str):
    """
    Làm sạch và chuyển đổi giá từ chuỗi sang số thực
    
    Xử lý 2 định dạng giá khác nhau:
    - CellphoneS: "22.990.000đ" -> 22990000
    - TGDD: "13190000.0" -> 13190000
    
    Tham số:
        price_str (str): Chuỗi giá cần chuyển đổi
    
    Trả về:
        float: Giá dạng số, hoặc None nếu không hợp lệ
    """
    # Kiểm tra các trường hợp không hợp lệ
    if not price_str or price_str == 'N/A' or 'Liên hệ' in price_str:
        return None
    
    # Loại bỏ ký tự 'đ', dấu chấm, dấu phẩy và khoảng trắng
    price_cleaned = price_str.replace('đ', '').replace('.', '').replace(',', '').strip()
    try:
        return float(price_cleaned)
    except ValueError:
        # Nếu không convert được sang số thì trả về None
        return None

def extract_brand(product_name):
    """
    Trích xuất tên hãng sản xuất từ tên sản phẩm
    
    Chiến lược:
    1. Lấy từ thứ 2 (sau "Laptop") hoặc từ đầu tiên làm brand
    2. Chỉ chuẩn hóa các aliases phổ biến (Vivobook->Asus, IdeaPad->Lenovo)
    3. KHÔNG loại bỏ brands không nằm trong danh sách → tránh mất data
    
    Ví dụ:
        "Laptop HP 15 fc0085AU" -> "HP"
        "MacBook Pro 14 M4" -> "MacBook"
        "Laptop Asus Vivobook" -> "Asus"
        "Laptop BrandMới ABC123" -> "BrandMới" (GIỮ LẠI, không loại bỏ)
    
    Tham số:
        product_name (str): Tên đầy đủ của sản phẩm
    
    Trả về:
        str: Tên hãng đã chuẩn hóa
    """
    if not product_name:
        return "Unknown"
    
    words = product_name.split()
    
    # Bỏ qua từ "Laptop" nếu nó là từ đầu tiên
    # Vì tên sản phẩm thường có format: "Laptop [Hãng] [Model]..."
    if len(words) >= 2 and words[0].lower() == 'laptop':
        brand_word = words[1].strip()
    else:
        brand_word = words[0].strip() if words else "Unknown"
    
    # Bảng ánh xạ CHỈ để chuẩn hóa các model/series name thành brand chính
    # KHÔNG dùng để filter - nếu brand không có trong map thì GIỮ NGUYÊN
    brand_aliases = {
        # Chuẩn hóa các biến thể viết hoa/thường
        'ASUS': 'Asus',
        'asus': 'Asus',
        
        # Ánh xạ các dòng sản phẩm về brand chính
        'Vivobook': 'Asus',      # Asus Vivobook
        'IdeaPad': 'Lenovo',     # Lenovo IdeaPad
        'Ideapad': 'Lenovo',
        'Aspire': 'Acer',        # Acer Aspire
        'Inspiron': 'Dell',      # Dell Inspiron
        'Latitude': 'Dell',      # Dell Latitude
        'Prestige': 'MSI',       # MSI Prestige
        'Katana': 'MSI',         # MSI Katana
        'ROG': 'Asus',           # Asus ROG
        'TUF': 'Asus',           # Asus TUF
        'G6': 'Gigabyte',
        'V16': 'Asus',
        'ThinkPad': 'Lenovo',    # Lenovo ThinkPad
        'ThinkBook': 'Lenovo',
        'Pavilion': 'HP',        # HP Pavilion
        'Envy': 'HP',            # HP Envy
        'Nitro': 'Acer',         # Acer Nitro
        'Swift': 'Acer',         # Acer Swift
    }
    
    # Nếu có trong map thì chuẩn hóa, KHÔNG THÌ GIỮ NGUYÊN (key point!)
    return brand_aliases.get(brand_word, brand_word)

def main():
    """
    Hàm chính của Mapper
    Đọc dữ liệu CSV từ stdin, xử lý và xuất ra format: brand \t price
    """
    # Thiết lập encoding UTF-8 cho stdin (tương thích với Hadoop Streaming)
    # Hadoop Streaming pipe dữ liệu dạng binary UTF-8, cần decode thành text
    import io
    if hasattr(sys.stdin, 'buffer'):
        # Chế độ binary (Hadoop Streaming hoặc local test)
        # Wrap stdin.buffer với TextIOWrapper để đọc được text UTF-8
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    # Nếu không có .buffer attribute => stdin đã ở text mode (subprocess với text=True)
    
    # Sử dụng CSV DictReader để đọc file CSV với header
    reader = csv.DictReader(sys.stdin)
    
    for row in reader:
        try:
            # Lấy tên sản phẩm từ cột 'product_name'
            product_name = row.get('product_name', '')
            
            # Lấy giá hiện tại - xử lý cả 2 format tên cột
            # TGDD có cột 'current_price', CellphoneS có 'current_price_raw'
            current_price_raw = row.get('current_price') or row.get('current_price_raw', '')
            
            # Làm sạch và chuyển đổi giá sang số
            price = clean_price(current_price_raw)
            
            # Bỏ qua các sản phẩm không có giá hợp lệ
            if price is None:
                continue
            
            # Trích xuất tên hãng
            # Ưu tiên dùng cột 'brand' nếu có (TGDD), 
            # nếu không thì parse từ 'product_name' (CellphoneS)
            brand = row.get('brand', '').strip()
            if not brand:
                brand = extract_brand(product_name)
            
            # Xuất kết quả: brand \t price
            # Format này sẽ được Hadoop shuffle & sort theo key (brand)
            print(f"{brand}\t{price}")
            
        except Exception as e:
            # Bỏ qua các dòng có lỗi (ví dụ: dữ liệu bị corrupt)
            continue

if __name__ == '__main__':
    main()
