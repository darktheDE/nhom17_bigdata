#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess, sys, os, io

# Fix encoding cho Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_mapreduce_local(input_files, output_file, mapper_script, reducer_script):
    print(f"Starting MapReduce job...")
    mapper_output = []
    for input_file in input_files:
        print(f"  Processing {os.path.basename(input_file)}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            mapper_proc = subprocess.Popen([sys.executable, mapper_script], stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            stdout, stderr = mapper_proc.communicate()
            if mapper_proc.returncode != 0:
                print(f"Error: {stderr}")
                return False
            mapper_output.extend(stdout.strip().split('\n') if stdout.strip() else [])
    
    print(f"  Mapper produced {len(mapper_output)} records")
    mapper_output.sort()
    
    print(f"  Reducing...")
    reducer_proc = subprocess.Popen([sys.executable, reducer_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    stdout, stderr = reducer_proc.communicate(input='\n'.join(mapper_output))
    if reducer_proc.returncode != 0:
        print(f"Error: {stderr}")
        return False
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stdout)
    
    print(f"✓ Job completed! Output: {output_file}")
    return True

if __name__ == '__main__':
    base_dir = r'd:\HCMUTE\HCMUTE_HK5\BDES333877_BigData\nhom17_bigdata'
    input_files = [os.path.join(base_dir, 'data', 'raw', 'tgdd_raw_data.csv'), os.path.join(base_dir, 'data', 'raw', 'cellphones_raw_data.csv')]
    output_file = os.path.join(base_dir, 'data', 'output_mapreduce', 'job03_price_range_distribution.txt')
    
    print("=" * 70)
    print("Job 03: Price Range Distribution")
    print("=" * 70)
    success = run_mapreduce_local(input_files, output_file, 'mapper.py', 'reducer.py')
    sys.exit(0 if success else 1)
