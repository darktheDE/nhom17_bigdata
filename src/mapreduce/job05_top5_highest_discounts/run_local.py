#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Test Runner cho Job 05: Top 5 Highest Discounts
Mô phỏng MapReduce workflow với sort GIẢM DẦN
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
    Chạy MapReduce job local với subprocess
    
    Flow:
    1. Mapper: Đọc CSV → output discount% \t product_info
    2. Sort: Sắp xếp theo discount% GIẢM DẦN (reverse)
    3. Reducer: Lấy top 5 records đầu tiên
    """
    print("=" * 70)
    print("Job 05: Top 5 Highest Discounts")
    print("=" * 70)
    
    # Đường dẫn
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
    
    mapper_path = os.path.join(script_dir, 'mapper.py')
    reducer_path = os.path.join(script_dir, 'reducer.py')
    
    # Input files
    input_files = [
        os.path.join(project_root, 'data', 'raw', 'tgdd_raw_data.csv'),
        os.path.join(project_root, 'data', 'raw', 'cellphones_raw_data.csv')
    ]
    
    # Output file
    output_dir = os.path.join(project_root, 'data', 'output_mapreduce')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'job05_top5_highest_discounts.txt')
    
    print(f"Starting MapReduce job...")
    print(f"Input files: {input_files}")
    print(f"Output: {output_file}")
    
    # Step 1: Run mapper
    print(f"Processing mapper...")
    mapper_output = []
    
    for input_file in input_files:
        print(f"  Processing {os.path.basename(input_file)}...")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            # Chạy mapper
            process = subprocess.Popen(
                ['python', mapper_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8'
            )
            
            stdout, stderr = process.communicate(input=f.read())
            
            if stderr:
                sys.stderr.write(f"Mapper stderr: {stderr}\n")
            
            # Lưu output
            mapper_output.extend(stdout.strip().split('\n') if stdout.strip() else [])
    
    print(f"  Mapper produced {len(mapper_output)} records")
    
    # Step 2: Sort (GIẢM DẦN - quan trọng cho Top-N!)
    print(f"  Sorting (descending order)...")
    # Sort theo key (phần trước \t), REVERSE để giảm dần
    sorted_output = sorted(mapper_output, reverse=True)
    
    # Step 3: Run reducer
    print(f"  Reducing (get top 5)...")
    
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
    
    print(f"✓ Job completed successfully!")
    print(f"✓ Output saved to: {output_file}")
    print()
    print("=" * 70)
    print("TOP 5 HIGHEST DISCOUNTS:")
    print("=" * 70)
    print(final_output)

if __name__ == '__main__':
    run_mapreduce_job()
