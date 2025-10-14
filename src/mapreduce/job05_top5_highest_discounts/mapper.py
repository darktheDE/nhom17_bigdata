#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 05 - Mapper
Nhiệm vụ: Tìm 5 laptop có tỷ lệ giảm giá cao nhất
Đầu vào: CSV files (tgdd.csv, cellphones.csv)
Đầu ra: discount_percent \t product_name|current_price|list_price|brand
"""

import sys
import csv
import re

def clean_price(price_str):
    """
    Làm sạch chuỗi giá thành số
    
    Xử lý 2 format:
    - TGDD: "13190000.0" (numeric string)
    - CellphoneS: "22.990.000đ" (formatted with dots)
    
    Tham số:
        price_str (str/float): Chuỗi hoặc số giá
    
    Trả về:
        float: Giá dạng số, hoặc None nếu không hợp lệ
    """
    if not price_str:
        return None
    
    # Nếu đã là số
    if isinstance(price_str, (int, float)):
        return float(price_str)
    
    # Chuyển về string
    price_str = str(price_str).strip()
    
    # Bỏ qua các giá trị không hợp lệ
    if price_str.lower() in ['n/a', 'null', '', 'liên hệ để báo giá', 'liên hệ']:
        return None
    
    # Loại bỏ ký tự không phải số (giữ lại dấu chấm và phấy)
    # Format CellphoneS: "22.990.000đ" → "22990000"
    price_clean = re.sub(r'[^\d.,]', '', price_str)
    
    # Xử lý dấu chấm và phấy
    # Nếu có nhiều dấu chấm → format kiểu "22.990.000" → bỏ dấu chấm
    if price_clean.count('.') > 1:
        price_clean = price_clean.replace('.', '')
    # Thay dấu phấy bằng chấm cho decimal
    price_clean = price_clean.replace(',', '.')
    
    try:
        return float(price_clean)
    except ValueError:
        return None

def extract_brand(product_name):
    """
    Trích xuất tên thương hiệu từ tên sản phẩm
    
    Chiến lược:
    - Bỏ qua từ "Laptop" ở đầu
    - Lấy từ tiếp theo làm brand
    - Normalize các model/series → parent brand
    """
    if not product_name:
        return "Unknown"
    
    words = product_name.split()
    
    # Bỏ qua từ "Laptop" ở đầu
    if len(words) >= 2 and words[0].lower() == 'laptop':
        brand_word = words[1].strip()
    else:
        brand_word = words[0].strip() if words else "Unknown"
    
    # Danh sách ALIAS: model/series → parent brand
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
    """
    Hàm chính của Mapper
    Đọc CSV, tính % giảm giá, xuất: discount% \t product_info
    """
    # Thiết lập encoding UTF-8 cho Hadoop Streaming
    import io
    if hasattr(sys.stdin, 'buffer'):
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    
    # Thiết lập encoding UTF-8 cho stdout
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    reader = csv.DictReader(sys.stdin)
    
    for row in reader:
        try:
            # Lấy thông tin sản phẩm
            product_name = row.get('product_name', '')
            
            # Lấy giá (xử lý cả 2 tên cột)
            current_price_raw = row.get('current_price') or row.get('current_price_raw', '')
            list_price_raw = row.get('list_price') or row.get('list_price_raw', '')
            
            # Làm sạch giá
            current_price = clean_price(current_price_raw)
            list_price = clean_price(list_price_raw)
            
            # Bỏ qua nếu thiếu giá hoặc không có giảm giá
            if current_price is None or list_price is None or list_price == 0:
                continue
            
            if current_price >= list_price:
                continue  # Không có giảm giá
            
            # Tính tỷ lệ giảm giá
            discount_percent = ((list_price - current_price) / list_price) * 100
            
            # Trích xuất brand
            brand = extract_brand(product_name)
            
            # Format giá cho output (dễ đọc)
            current_price_fmt = f"{int(current_price):,}đ".replace(',', '.')
            list_price_fmt = f"{int(list_price):,}đ".replace(',', '.')
            
            # Xuất: discount% (key) \t product_info (value)
            # Dùng | làm delimiter trong value vì sản phẩm có thể chứa tab
            product_info = f"{product_name}|{current_price_fmt}|{list_price_fmt}|{brand}"
            
            # Key: discount_percent (2 chữ số thập phân, pad 0 để sort đúng)
            # VD: 12.34 → "012.34" để sort string = sort number
            discount_key = f"{discount_percent:06.2f}"
            
            print(f"{discount_key}\t{product_info}")
            sys.stdout.flush()
        
        except Exception as e:
            # Ghi lỗi ra stderr (không ảnh hưởng output)
            sys.stderr.write(f"Lỗi xử lý dòng: {e}\n")
            continue

if __name__ == '__main__':
    main()
