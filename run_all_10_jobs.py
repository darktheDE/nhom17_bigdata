#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chạy TOÀN BỘ 10 MapReduce jobs với dữ liệu lớn (RAW DATA)
Lưu kết quả vào data/output_raw/
"""

import subprocess
import os
import sys
import time
from datetime import datetime

def run_job(job_num, job_name, job_folder):
    """
    Chạy một MapReduce job
    
    Tham số:
        job_num (int): Số thứ tự job (1-10)
        job_name (str): Tên mô tả job
        job_folder (str): Thư mục chứa job
    
    Trả về:
        bool: True nếu thành công, False nếu thất bại
    """
    print("\n" + "=" * 80)
    print(f"[{job_num}/10] {job_name}")
    print("=" * 80)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    job_dir = os.path.join(current_dir, 'src', 'mapreduce', job_folder)
    run_script = os.path.join(job_dir, 'run_local.py')
    
    if not os.path.exists(run_script):
        print(f"❌ Không tìm thấy: {run_script}")
        return False
    
    try:
        start_time = time.time()
        
        # Chạy run_local.py
        result = subprocess.run(
            ['python', run_script],
            cwd=job_dir,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        elapsed = time.time() - start_time
        
        # Hiển thị output (chỉ hiển thị 15 dòng cuối)
        if result.stdout:
            output_lines = result.stdout.strip().split('\n')
            display_lines = output_lines[-15:] if len(output_lines) > 15 else output_lines
            for line in display_lines:
                print(line)
        
        # Kiểm tra kết quả
        if result.returncode == 0:
            print(f"\n✅ Job {job_num:02d} hoàn thành trong {elapsed:.2f}s")
            return True
        else:
            print(f"\n❌ Job {job_num:02d} thất bại")
            if result.stderr:
                print("Lỗi:", result.stderr[:500])
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi chạy job: {e}")
        return False


def main():
    """Hàm main - chạy tất cả 10 jobs"""
    print("=" * 80)
    print("CHẠY TOÀN BỘ 10 MAPREDUCE JOBS VỚI RAW DATA")
    print("=" * 80)
    
    start_time = time.time()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Thời gian bắt đầu: {now}")
    print("Output directory: data/output_raw/")
    print("=" * 80)
    
    # Danh sách 10 jobs
    jobs = [
        (1, "Tính giá bán trung bình theo hãng", "job01_avg_price_by_brand"),
        (2, "Tính tỷ lệ giảm giá theo hãng", "job02_discount_rate_by_brand"),
        (3, "Đếm sản phẩm trong từng khoảng giá", "job03_price_range_distribution"),
        (4, "Thống kê từ khóa khuyến mãi", "job04_promotion_keyword_frequency"),
        (5, "Top 5 laptop giảm giá cao nhất", "job05_top5_highest_discounts"),
        (6, "Số lượng khuyến mãi TB/sản phẩm", "job06_avg_promotions_per_store"),
        (7, "Thống kê CPU phổ biến nhất", "job07_popular_cpu_models"),
        (8, "Đếm sản phẩm theo Brand & Store", "job08_product_count_by_brand_store"),
        (9, "Đếm laptop có Office", "job09_office_license_count"),
        (10, "Giá trị giảm giá theo hãng", "job10_cash_discount_by_brand")
    ]
    
    # Chạy từng job
    results = []
    for job_num, job_name, job_folder in jobs:
        success = run_job(job_num, job_name, job_folder)
        results.append((job_num, job_name, success))
    
    # Tổng kết
    elapsed = time.time() - start_time
    success_count = sum(1 for _, _, success in results if success)
    fail_count = len(results) - success_count
    
    print("\n" + "=" * 80)
    print("TỔNG KẾT KẾT QUẢ")
    print("=" * 80)
    print(f"\nTổng thời gian: {elapsed:.2f}s ({elapsed/60:.1f} phút)")
    print(f"Thành công: {success_count}/10")
    print(f"Thất bại: {fail_count}/10")
    
    print("\nJob                     Kết quả")
    print("-" * 80)
    for job_num, job_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"Job {job_num:02d}                   {status}")
    
    # Hiển thị thông tin các file output
    print("\n" + "=" * 80)
    print("CÁC FILE KẾT QUẢ TRONG data/output_raw/")
    print("=" * 80 + "\n")
    
    output_dir = os.path.join(os.path.dirname(__file__), 'data', 'output_raw')
    if os.path.exists(output_dir):
        print(f"{'File':<60} {'Size':>10} {'Lines':>8}")
        print("-" * 80)
        
        total_size = 0
        for filename in sorted(os.listdir(output_dir)):
            filepath = os.path.join(output_dir, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                total_size += size
                
                # Đếm số dòng
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        lines = sum(1 for _ in f)
                except:
                    lines = 0
                
                # Format size
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:,.0f} B"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                
                print(f"{filename:<60} {size_str:>10} {lines:>8,}")
        
        print("-" * 80)
        if total_size < 1024:
            total_str = f"{total_size} B"
        elif total_size < 1024 * 1024:
            total_str = f"{total_size/1024:.1f} KB"
        else:
            total_str = f"{total_size/(1024*1024):.1f} MB"
        print(f"{'TỔNG CỘNG':<60} {total_str:>10}")
    
    print("\n" + "=" * 80)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Hoàn thành lúc: {now}")
    print("=" * 80 + "\n")
    
    # Exit code
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == '__main__':
    main()
