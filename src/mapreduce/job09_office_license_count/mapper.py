#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job 09 - Mapper: Đếm laptop có Office Home & Student
Input: CSV (chỉ xử lý tgdd.csv vì chỉ TGDĐ có cột 'software')
Output: "Office" \t 1 hoặc "No Office" \t 1
"""
import sys, csv, io

if hasattr(sys.stdin, 'buffer'):
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

reader = csv.DictReader(sys.stdin)

for row in reader:
    try:
        software = row.get('software', '')
        
        # Kiểm tra có Office Home & Student không
        if software and ('office' in software.lower() and ('home' in software.lower() or 'student' in software.lower())):
            print("Office\t1")
        else:
            print("No Office\t1")
        sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")

