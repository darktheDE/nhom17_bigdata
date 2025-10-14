#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chạy MapReduce Job 07 ở chế độ local (test)
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
    
    print("=" * 60)
    print("MapReduce Job 07: Thống kê CPU phổ biến nhất")
    print("=" * 60)
    
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
    
    # Bước 2: Shuffle & Sort (mô phỏng bằng sort command)
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
    print("\n" + "=" * 60)
    print("KẾT QUẢ TOP 10 CPU PHỔ BIẾN NHẤT")
    print("=" * 60)
    
    # Sắp xếp theo số lượng giảm dần
    results = []
    for line in final_output.strip().split('\n'):
        if line:
            parts = line.split('\t')
            if len(parts) == 2:
                cpu_model, count = parts
                results.append((cpu_model, int(count)))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    print(f"{'CPU Model':<20} {'Số lượng':>15}")
    print("-" * 60)
    for cpu, count in results[:10]:
        print(f"{cpu:<20} {count:>15}")
    
    print("\n" + "=" * 60)
    print(f"✓ Kết quả đầy đủ đã được lưu tại: {output_file}")
    print(f"  Tổng số dòng CPU khác nhau: {len(results)}")
    print("=" * 60)

if __name__ == '__main__':
    # Xác định đường dẫn project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
    
    # File input (sử dụng sample data để test nhanh)
    input_files = [
        os.path.join(project_root, 'data', 'raw', 'tgdd_raw_data.csv'),
        os.path.join(project_root, 'data', 'raw', 'cellphones_raw_data.csv')
    ]
    
    # File output
    output_file = os.path.join(project_root, 'data', 'output_raw', 'job07_popular_cpu_models.txt')
    
    # Chạy MapReduce
    run_mapreduce(input_files, output_file)
