#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local test runner for Job 02 - Discount Rate by Brand
"""

import subprocess
import sys
import os
import io

# Fix encoding cho Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_mapreduce_local(input_files, output_file, mapper_script, reducer_script):
    """Run MapReduce job locally"""
    print(f"Starting MapReduce job...")
    print(f"Input files: {input_files}")
    print(f"Output: {output_file}")
    
    # Step 1: Run mapper
    mapper_output = []
    for input_file in input_files:
        print(f"  Processing {os.path.basename(input_file)}...")
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
                print(f"Mapper error: {stderr}")
                return False
            mapper_output.extend(stdout.strip().split('\n') if stdout.strip() else [])
    
    print(f"  Mapper produced {len(mapper_output)} records")
    
    # Step 2: Sort
    print(f"  Sorting...")
    mapper_output.sort()
    
    # Step 3: Run reducer
    print(f"  Reducing...")
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
        print(f"Reducer error: {stderr}")
        return False
    
    # Step 4: Write output
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stdout)
    
    print(f"✓ Job completed successfully!")
    print(f"✓ Output saved to: {output_file}")
    return True

if __name__ == '__main__':
    base_dir = r'd:\HCMUTE\HCMUTE_HK5\BDES333877_BigData\nhom17_bigdata'
    
    input_files = [
        os.path.join(base_dir, 'data', 'raw', 'tgdd_raw_data.csv'),
        os.path.join(base_dir, 'data', 'raw', 'cellphones_raw_data.csv')
    ]
    
    output_file = os.path.join(base_dir, 'data', 'output_mapreduce', 'job02_discount_rate_by_brand.txt')
    
    print("=" * 70)
    print("Job 02: Discount Rate by Brand")
    print("=" * 70)
    
    success = run_mapreduce_local(input_files, output_file, 'mapper.py', 'reducer.py')
    sys.exit(0 if success else 1)
