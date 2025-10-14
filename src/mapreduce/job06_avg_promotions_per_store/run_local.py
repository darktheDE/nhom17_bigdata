#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Test Runner cho Job 06: Avg Promotions per Store
"""

import subprocess
import os
import sys
import io

# Fix encoding cho Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_mapreduce_job():
    """
    Chạy MapReduce job local
    
    Flow:
    1. Mapper: Đọc JSON → count promotions per product → output store \t count
    2. Sort: Group theo store
    3. Reducer: Tính average promotions per store
    """
    print("=" * 70)
    print("Job 06: Average Promotions per Store")
    print("=" * 70)
    
    # Đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
    
    mapper_path = os.path.join(script_dir, 'mapper.py')
    reducer_path = os.path.join(script_dir, 'reducer.py')
    
    # Input files với store mapping
    input_files = [
        {
            'path': os.path.join(project_root, 'data', 'raw', 'tgdd_promotions_nosql.json'),
            'store': 'TGDĐ'
        },
        {
            'path': os.path.join(project_root, 'data', 'raw', 'cellphones_promotions_nosql.json'),
            'store': 'CellphoneS'
        }
    ]
    
    # Output file
    output_dir = os.path.join(project_root, 'data', 'output_mapreduce')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'job06_avg_promotions_per_store.txt')
    
    print(f"Bắt đầu MapReduce job...")
    print(f"Input files: {[f['path'] for f in input_files]}")
    print(f"Output: {output_file}")
    
    # Step 1: Run mapper
    print(f"Đang xử lý mapper...")
    mapper_output = []
    
    for file_info in input_files:
        file_path = file_info['path']
        store_name = file_info['store']
        
        print(f"  Đang xử lý {os.path.basename(file_path)} (Store: {store_name})...")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            # Set environment variable cho mapper
            env = os.environ.copy()
            env['STORE_NAME'] = store_name
            
            # Chạy mapper
            process = subprocess.Popen(
                ['python', mapper_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                env=env
            )
            
            stdout, stderr = process.communicate(input=f.read())
            
            if stderr:
                sys.stderr.write(f"Mapper stderr: {stderr}\n")
            
            # Lưu output
            mapper_output.extend(stdout.strip().split('\n') if stdout.strip() else [])
    
    print(f"  Mapper tạo ra {len(mapper_output)} records")
    
    # Step 2: Sort
    print(f"  Đang sắp xếp...")
    sorted_output = sorted(mapper_output)
    
    # Step 3: Run reducer
    print(f"  Đang reduce...")
    
    sorted_text = '\n'.join(sorted_output)
    
    process = subprocess.Popen(
        ['python', reducer_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'
    )
    
    final_output, stderr = process.communicate(input=sorted_text)
    
    if stderr:
        sys.stderr.write(f"Reducer stderr: {stderr}\n")
    
    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_output)
    
    print(f"✓ Job hoàn thành! Output: {output_file}")
    print()
    print("=" * 70)
    print("KẾT QUẢ SO SÁNH:")
    print("=" * 70)
    print("Cửa hàng\t\tSố KM trung bình\tTổng sản phẩm")
    print("-" * 70)
    print(final_output)

if __name__ == '__main__':
    run_mapreduce_job()
