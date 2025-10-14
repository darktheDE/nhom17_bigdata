#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job 10 - Mapper: Extract cash discount from JSON promotions and JOIN with CSV
Strategy: 
  1. Đọc CSV trước, build dict: product_id → brand
  2. Đọc JSON, lookup brand theo product_id
  3. Extract cash discount từ promotions
Output: brand \t discount_amount
"""
import sys, json, re, io, csv, os

def extract_brand(product_name):
    """Extract brand from product_name"""
    if not product_name:
        return "Unknown"
    words = product_name.split()
    brand_word = words[1] if len(words) >= 2 and words[0].lower() == 'laptop' else (words[0] if words else "Unknown")
    
    aliases = {'vivobook':'Asus','zenbook':'Asus','ideapad':'Lenovo','thinkpad':'Lenovo',
               'pavilion':'HP','envy':'HP','inspiron':'Dell','macbook':'MacBook','aspire':'Acer'}
    return aliases.get(brand_word.lower(), brand_word)

def load_product_brands(csv_files):
    """
    Load product_id → brand mapping from CSV files
    CSV có cột 'id' (hoặc '\ufeffid' với BOM), JSON có 'product_id'
    Returns: dict {product_id: brand}
    """
    brand_map = {}
    for csv_file in csv_files:
        if not os.path.exists(csv_file):
            continue
        with open(csv_file, 'r', encoding='utf-8-sig', errors='replace') as f:  # utf-8-sig strips BOM
            reader = csv.DictReader(f)
            for row in reader:
                # CSV sử dụng cột 'id'
                product_id = row.get('id', '').strip()
                product_name = row.get('product_name', '').strip()
                if product_id and product_name:
                    brand = extract_brand(product_name)
                    brand_map[product_id] = brand
    return brand_map

def extract_cash_discount(promo_text):
    """
    Extract cash discount amount from text
    Patterns: 
    - "Giảm ngay 700,000đ" (TGDĐ: có dấu phẩy)
    - "Giảm ngay 500K" (CellphoneS: số + K)
    - "Giảm 1.000.000đ" (có dấu chấm)
    Returns: float or None
    """
    promo_lower = promo_text.lower()
    
    # Pattern 1: TGDĐ format "700,000đ" (dấu phẩy)
    match = re.search(r'giảm\s+ngay\s+([\d,]+)đ', promo_lower)
    if match:
        amount_str = match.group(1).replace(',', '')  # "700,000" → "700000"
        try:
            return float(amount_str)
        except ValueError:
            pass
    
    # Pattern 2: CellphoneS format "500K" (chữ K = 1000)
    match = re.search(r'giảm\s+ngay\s+(\d+)k\b', promo_lower)
    if match:
        amount_str = match.group(1)
        try:
            return float(amount_str) * 1000  # 500K → 500000
        except ValueError:
            pass
    
    # Pattern 3: Format với dấu chấm "1.000.000đ"
    match = re.search(r'giảm\s+(ngay\s+)?([\d\.]+)đ', promo_lower)
    if match:
        amount_str = match.group(2).replace('.', '')  # "1.000.000" → "1000000"
        try:
            return float(amount_str)
        except ValueError:
            pass
    
    return None

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stdin, 'buffer'):
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')

# Load brand mapping from CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', '..', 'data', 'raw')
csv_files = [
    os.path.join(data_dir, 'tgdd_raw_data.csv'),
    os.path.join(data_dir, 'cellphones_raw_data.csv')
]
brand_map = load_product_brands(csv_files)

try:
    data = json.loads(sys.stdin.read())
    if not isinstance(data, list):
        data = [data]
    
    for item in data:
        product_id = item.get('product_id', '').strip()
        promotions = item.get('promotions', [])
        
        # Lookup brand from CSV mapping
        brand = brand_map.get(product_id, "Unknown")
        
        for promo in promotions:
            if not promo:
                continue
            discount = extract_cash_discount(promo)
            if discount:
                print(f"{brand}\t{int(discount)}")
                sys.stdout.flush()
except Exception as e:
    sys.stderr.write(f"Error: {e}\n")
