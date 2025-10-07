#!/usr/bin/env python3
"""
Job 12: Discount Comparison by Platform (So sánh tỷ lệ giảm giá theo sàn)
Mapper: Tính tỷ lệ giảm giá cho mỗi sản phẩm trên từng sàn
Input: CSV với các cột: current_price, list_price, source_website
Output: (source_website, discount_percent)
"""

import sys
import csv

def main():
    # Đọc CSV từ stdin
    reader = csv.DictReader(sys.stdin)
    
    for row in reader:
        try:
            source_website = row.get('source_website', '').strip()
            current_price = row.get('current_price', '').strip()
            list_price = row.get('list_price', '').strip()
            
            # Bỏ qua nếu thiếu dữ liệu
            if not source_website or not current_price or not list_price:
                continue
            
            # Chuyển đổi sang float
            current = float(current_price)
            listed = float(list_price)
            
            # Tính tỷ lệ giảm giá
            if listed > 0 and listed > current:
                discount_percent = ((listed - current) / listed) * 100
                print(f"{source_website}\t{discount_percent:.2f}")
            
        except (ValueError, KeyError, ZeroDivisionError) as e:
            continue

if __name__ == "__main__":
    main()
