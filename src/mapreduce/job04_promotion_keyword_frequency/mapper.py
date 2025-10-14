#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 04 - Mapper
Nhiệm vụ: Thống kê tần suất xuất hiện của các từ khóa khuyến mãi
Đầu vào: JSON files (tgdd_promo.json, cellphones_promo.json)
Đầu ra: keyword \t 1
"""

import sys
import json
import re

# Danh sách từ khóa quan trọng cần thống kê
KEYWORDS = [
    'trả góp',
    'giảm ngay',
    'giảm',
    'tặng',
    'balo',
    'túi',
    'chuột',
    'voucher',
    'phiếu mua hàng',
    'bảo hành',
    'office',
    'microsoft',
    'win11',
    'windows',
    'ưu đãi',
    'khuyến mãi',
    'miễn phí',
    'tặng kèm',
    'quà tặng',
    'pin dự phòng',
    'tai nghe',
    'loa',
    'màn hình',
    'máy in',
    'thu cũ',
    'lên đời',
    '0%',
    'sim',
    'esim'
]

def extract_keywords(promo_text):
    """
    Trích xuất các từ khóa từ chuỗi khuyến mãi
    
    Tham số:
        promo_text (str): Chuỗi mô tả khuyến mãi
    
    Trả về:
        list: Danh sách từ khóa tìm thấy
    """
    # Chuyển text về lowercase để so sánh không phân biệt hoa thường
    promo_lower = promo_text.lower()
    
    found_keywords = []
    for keyword in KEYWORDS:
        # Tìm keyword trong text
        if keyword.lower() in promo_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def main():
    """
    Hàm chính của Mapper
    Đọc JSON từ stdin, tìm và xuất các từ khóa
    """
    # Thiết lập encoding UTF-8 cho stdout (để print được tiếng Việt)
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    # Thiết lập encoding UTF-8 cho stdin
    if hasattr(sys.stdin, 'buffer'):
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    
    # Đọc toàn bộ stdin (JSON có thể là một file lớn)
    try:
        # Đọc tất cả nội dung
        content = sys.stdin.read()
        
        # Parse JSON - file là một array lớn
        data = json.loads(content)
        
        # Nếu không phải array, chuyển thành array
        if not isinstance(data, list):
            data = [data]
        
        # Xử lý từng sản phẩm
        for item in data:
            # Lấy mảng promotions
            promotions = item.get('promotions', [])
            
            # Duyệt qua từng chuỗi khuyến mãi
            for promo_text in promotions:
                if not promo_text:  # Bỏ qua chuỗi rỗng
                    continue
                
                # Tìm các từ khóa trong text
                keywords = extract_keywords(promo_text)
                
                # Xuất từng keyword tìm thấy
                for keyword in keywords:
                    # Chuẩn hóa output (viết hoa chữ cái đầu)
                    keyword_normalized = keyword.title()
                    print(f"{keyword_normalized}\t1")
                    sys.stdout.flush()  # Flush để đảm bảo output ngay
    
    except Exception as e:
        # Nếu có lỗi parse JSON, ghi log ra stderr (không ảnh hưởng output)
        sys.stderr.write(f"Lỗi parse JSON: {e}\n")
        pass

if __name__ == '__main__':
    main()
