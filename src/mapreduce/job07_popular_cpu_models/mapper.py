#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MapReduce Job 11 - Mapper
Nhiệm vụ: Thống kê các dòng CPU phổ biến nhất trên thị trường
Đầu vào: CSV files (tgdd.csv, cellphones.csv)
Đầu ra: cpu_model \t 1
"""

import sys
import csv
import re

def extract_cpu_model(specs_string, cpu_column=None):
    """
    Trích xuất mã hiệu CPU từ chuỗi cấu hình hoặc cột CPU
    
    Hỗ trợ các định dạng:
    - Intel: i3, i5, i7, i9 (ví dụ: i5-13420H, i7-1360P)
    - AMD Ryzen: R3, R5, R7, R9 (ví dụ: R5-7520U, R7-7730U)
    - Apple: M1, M2, M3, M4 (ví dụ: M4 Pro)
    - Intel Core: Core 5, Core 7 (ví dụ: Core 5-210H)
    - Intel Ultra: U9 (ví dụ: U9-288V)
    
    Tham số:
        specs_string (str): Chuỗi cấu hình sản phẩm
        cpu_column (str): Cột CPU riêng (nếu có)
    
    Trả về:
        str: Mã CPU đã chuẩn hóa, hoặc None nếu không tìm thấy
    """
    text = specs_string if specs_string else ""
    if cpu_column:
        text = cpu_column + " " + text
    
    if not text or text == 'N/A':
        return None
    
    # Pattern cho Intel Core i-series (i3, i5, i7, i9)
    intel_pattern = r'\b[iI](\d)[-\s]?(\d{4,5})([A-Z]{1,3})\b'
    match = re.search(intel_pattern, text)
    if match:
        gen = match.group(1)
        model = match.group(2)
        suffix = match.group(3).upper()
        return f"I{gen}-{model}{suffix}"
    
    # Pattern cho AMD Ryzen (R3, R5, R7, R9)
    amd_pattern = r'\b[rR](\d)[-\s]?(\d{4,5})([A-Z]{1,3})\b'
    match = re.search(amd_pattern, text)
    if match:
        gen = match.group(1)
        model = match.group(2)
        suffix = match.group(3).upper()
        return f"R{gen}-{model}{suffix}"
    
    # Pattern cho Intel Core (Core 5, Core 7)
    core_pattern = r'\b[cC][oO][rR][eE][-\s]?(\d)[-\s]?(\d{3,5})([A-Z]{1,3})\b'
    match = re.search(core_pattern, text)
    if match:
        gen = match.group(1)
        model = match.group(2)
        suffix = match.group(3).upper()
        return f"CORE{gen}-{model}{suffix}"
    
    # Pattern cho Intel Ultra (U9)
    ultra_pattern = r'\b[uU](\d{1,2})[-\s]?(\d{3})([A-Z]{1,2})\b'
    match = re.search(ultra_pattern, text)
    if match:
        gen = match.group(1)
        model = match.group(2)
        suffix = match.group(3).upper()
        return f"U{gen}-{model}{suffix}"
    
    # Pattern cho Apple Silicon (M1, M2, M3, M4)
    apple_pattern = r'\b[mM](\d)(\s[pP][rR][oO]|\s[mM][aA][xX]|\s[uU][lL][tT][rR][aA])?\b'
    match = re.search(apple_pattern, text)
    if match:
        gen = match.group(1)
        variant = match.group(2).strip().upper() if match.group(2) else ""
        if variant:
            return f"M{gen}-{variant}"
        return f"M{gen}"
    
    return None

def main():
    """
    Hàm chính của Mapper
    Đọc file CSV, trích xuất CPU model và xuất ra định dạng key-value
    """
    # Đọc từ stdin
    reader = csv.DictReader(sys.stdin)
    
    for row in reader:
        # Lấy thông tin cấu hình
        specs = row.get('raw_specs_string', '')
        cpu_col = row.get('cpu', '')
        
        # Trích xuất CPU model
        cpu_model = extract_cpu_model(specs, cpu_col)
        
        if cpu_model:
            # Xuất: cpu_model \t 1
            print(f"{cpu_model}\t1")

if __name__ == '__main__':
    main()
