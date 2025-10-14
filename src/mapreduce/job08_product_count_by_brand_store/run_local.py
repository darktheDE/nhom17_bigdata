#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chạy MapReduce Job 08 ở chế độ local (test)
Sử dụng subprocess để mô phỏng Hadoop Streaming
"""

import subprocess
import os
import sys
import io

# Fix encoding cho Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def run_mapreduce(input_files, output_file):
    """
    Chạy MapReduce job ở chế độ local
    
    Tham số:
        input_files (list): Danh sách đường dẫn đến file input
        output_file (str): Đường dẫn file output
    """
    # Đường dẫn tới mapper và reducer
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mapper_path = os.path.join(current_dir, 'mapper.py')
    reducer_path = os.path.join(current_dir, 'reducer.py')
    
    print("=" * 70)
    print("MapReduce Job 08: Đếm sản phẩm theo thương hiệu & cửa hàng")
    print("=" * 70)
    
    # Bước 1: Chạy Mapper
    print("\n[1/3] Đang chạy Mapper...")
    mapper_output = []
    for input_file in input_files:
        if not os.path.exists(input_file):
            print(f"⚠️  File không tồn tại: {input_file}")
            continue
        
        print(f"  - Xử lý: {os.path.basename(input_file)}")
        with open(input_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
            mapper_process = subprocess.Popen(
                ['python', mapper_path],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            output, error = mapper_process.communicate()
            
            if error:
                print(f"  ⚠️  Mapper warnings: {error}")
            
            mapper_output.append(output)
    
    # Gộp output từ tất cả các file
    all_mapper_output = '\n'.join(mapper_output)
    print(f"  ✓ Mapper hoàn thành. Số dòng output: {len(all_mapper_output.splitlines())}")
    
    # Bước 2: Shuffle & Sort
    print("\n[2/3] Đang shuffle & sort...")
    sort_process = subprocess.Popen(
        ['sort'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    sorted_output, sort_error = sort_process.communicate(input=all_mapper_output)
    
    if sort_error:
        print(f"  ⚠️  Sort warnings: {sort_error}")
    
    print(f"  ✓ Sort hoàn thành")
    
    # Bước 3: Chạy Reducer
    print("\n[3/3] Đang chạy Reducer...")
    reducer_process = subprocess.Popen(
        ['python', reducer_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    final_output, reducer_error = reducer_process.communicate(input=sorted_output)
    
    if reducer_error:
        print(f"  ⚠️  Reducer warnings: {reducer_error}")
    
    # Lưu kết quả ra file
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_output)
    
    print(f"  ✓ Reducer hoàn thành")
    
    # Hiển thị kết quả
    print("\n" + "=" * 70)
    print("KẾT QUẢ PHÂN TÍCH DANH MỤC SẢN PHẨM")
    print("=" * 70)
    
    results = {}
    for line in final_output.strip().split('\n'):
        if line:
            parts = line.split('\t')
            if len(parts) == 3:
                brand, source, count = parts
                count = int(count)
                
                if brand not in results:
                    results[brand] = {}
                results[brand][source] = count
    
    # Tính tổng
    print(f"\n{'Thương hiệu':<15} {'TGDĐ':>12} {'CellphoneS':>12} {'Tổng':>12} {'Khác biệt':>12}")
    print("-" * 70)
    
    for brand in sorted(results.keys()):
        tgdd_count = results[brand].get('thegioididong', 0)
        cellphones_count = results[brand].get('cellphones', 0)
        total = tgdd_count + cellphones_count
        diff = abs(tgdd_count - cellphones_count)
        
        print(f"{brand:<15} {tgdd_count:>12} {cellphones_count:>12} {total:>12} {diff:>12}")
    
    # Tổng kết
    total_tgdd = sum(r.get('thegioididong', 0) for r in results.values())
    total_cellphones = sum(r.get('cellphones', 0) for r in results.values())
    
    print("-" * 70)
    print(f"{'TỔNG':<15} {total_tgdd:>12} {total_cellphones:>12} {total_tgdd + total_cellphones:>12}")
    
    print("\n" + "=" * 70)
    print(f"✓ Kết quả đã được lưu tại: {output_file}")
    print(f"  Số thương hiệu: {len(results)}")
    print("=" * 70)

if __name__ == '__main__':
    # Xác định đường dẫn project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
    
    # File input
    input_files = [
        os.path.join(project_root, 'data', 'raw', 'tgdd_raw_data.csv'),
        os.path.join(project_root, 'data', 'raw', 'cellphones_raw_data.csv')
    ]
    
    # File output
    output_file = os.path.join(project_root, 'data', 'output_raw', 'job08_product_count_by_brand_store.txt')
    
    # Chạy MapReduce
    run_mapreduce(input_files, output_file)
