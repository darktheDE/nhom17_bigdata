#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local test runner for Job 04 - Promotion Keyword Frequency
Xử lý file JSON khuyến mãi
"""

import subprocess
import sys
import os
import io

# Fix encoding cho Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_mapreduce_local(input_files, output_file, mapper_script, reducer_script):
    """Chạy MapReduce job trên máy local"""
    print(f"Bắt đầu MapReduce job...")
    print(f"Input files: {input_files}")
    print(f"Output: {output_file}")
    
    # Bước 1: Chạy mapper
    mapper_output = []
    for input_file in input_files:
        print(f"  Đang xử lý {os.path.basename(input_file)}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            mapper_proc = subprocess.Popen(
                [sys.executable, mapper_script],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            stdout, stderr = mapper_proc.communicate()
            if mapper_proc.returncode != 0:
                print(f"Lỗi mapper: {stderr}")
                return False
            mapper_output.extend(stdout.strip().split('\n') if stdout.strip() else [])
    
    print(f"  Mapper tạo ra {len(mapper_output)} records")
    
    # Bước 2: Sort (shuffle & sort)
    print(f"  Đang sắp xếp...")
    mapper_output.sort()
    
    # Bước 3: Chạy reducer
    print(f"  Đang reduce...")
    reducer_proc = subprocess.Popen(
        [sys.executable, reducer_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    stdout, stderr = reducer_proc.communicate(input='\n'.join(mapper_output))
    
    if reducer_proc.returncode != 0:
        print(f"Lỗi reducer: {stderr}")
        return False
    
    # Bước 4: Ghi output
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stdout)
    
    print(f"✓ Job hoàn thành! Output: {output_file}")
    return True

if __name__ == '__main__':
    base_dir = r'd:\HCMUTE\HCMUTE_HK5\BDES333877_BigData\nhom17_bigdata'
    
    # Input: JSON files chứa khuyến mãi
    input_files = [
        os.path.join(base_dir, 'data', 'raw', 'tgdd_promotions_nosql.json'),
        os.path.join(base_dir, 'data', 'raw', 'cellphones_promotions_nosql.json')
    ]
    
    output_file = os.path.join(base_dir, 'data', 'output_mapreduce', 'job04_promotion_keyword_frequency.txt')
    
    print("=" * 70)
    print("Job 04: Thống kê tần suất từ khóa khuyến mãi")
    print("=" * 70)
    
    success = run_mapreduce_local(input_files, output_file, 'mapper.py', 'reducer.py')
    sys.exit(0 if success else 1)
