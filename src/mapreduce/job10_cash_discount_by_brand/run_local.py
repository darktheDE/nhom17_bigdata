#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Job 10 Test Runner"""
import subprocess, os, sys, io

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))

input_files = [
    os.path.join(project_root, 'data', 'raw', 'tgdd_promotions_nosql.json'),
    os.path.join(project_root, 'data', 'raw', 'cellphones_promotions_nosql.json')
]
output_file = os.path.join(project_root, 'data', 'output_raw', 'job10_cash_discount_by_brand.txt')
os.makedirs(os.path.dirname(output_file), exist_ok=True)

print("Job 10: Cash Discount by Brand")
print("="*50)

mapper_out = []
for f in input_files:
    with open(f, 'r', encoding='utf-8') as file:
        p = subprocess.Popen(['python', 'mapper.py'], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        out, _ = p.communicate(input=file.read())
        mapper_out.extend(out.strip().split('\n') if out.strip() else [])

sorted_out = '\n'.join(sorted(mapper_out))

p2 = subprocess.Popen(['python', 'reducer.py'], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
final_out, _ = p2.communicate(input=sorted_out)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(final_out)

print(f"Output: {output_file}")
print(f"Mapper records: {len(mapper_out)}")
if final_out:
    print()
    print(final_out)
else:
    print("\nNo cash discount pattern found (Giam ngay X.XXX.XXXd)")

