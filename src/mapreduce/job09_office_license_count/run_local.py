#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Job 09 Test Runner"""
import subprocess, os, sys, io

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))

input_file = os.path.join(project_root, 'data', 'raw', 'tgdd_raw_data.csv')
output_file = os.path.join(project_root, 'data', 'output_raw', 'job09_office_license_count.txt')
os.makedirs(os.path.dirname(output_file), exist_ok=True)

print("Job 09: Office License Count")
print("="*50)

with open(input_file, 'r', encoding='utf-8') as f:
    p1 = subprocess.Popen(['python', 'mapper.py'], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    mapper_out, _ = p1.communicate(input=f.read())

sorted_out = '\n'.join(sorted(mapper_out.strip().split('\n')))

p2 = subprocess.Popen(['python', 'reducer.py'], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
final_out, _ = p2.communicate(input=sorted_out)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_out)

print(f"Output: {output_file}")
print()
print(final_out)
