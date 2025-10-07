#!/usr/bin/env python3
"""
Job 12: Discount Comparison by Platform (So sánh tỷ lệ giảm giá theo sàn)
Reducer: Tính tỷ lệ giảm giá trung bình cho từng sàn
Input: (source_website, discount_percent) từ mapper (đã được sort)
Output: source_website\tavg_discount_percent\tcount\tmin_discount\tmax_discount
"""

import sys

def main():
    current_platform = None
    total_discount = 0
    count = 0
    min_discount = float('inf')
    max_discount = float('-inf')
    
    for line in sys.stdin:
        line = line.strip()
        
        try:
            parts = line.split('\t')
            if len(parts) != 2:
                continue
            
            platform = parts[0]
            discount = float(parts[1])
            
            if current_platform == platform:
                # Cùng platform, cộng dồn
                total_discount += discount
                count += 1
                min_discount = min(min_discount, discount)
                max_discount = max(max_discount, discount)
            else:
                # Platform mới, output kết quả platform cũ
                if current_platform is not None:
                    avg_discount = total_discount / count
                    print(f"{current_platform}\t{avg_discount:.2f}\t{count}\t{min_discount:.2f}\t{max_discount:.2f}")
                
                # Reset cho platform mới
                current_platform = platform
                total_discount = discount
                count = 1
                min_discount = discount
                max_discount = discount
                
        except (ValueError, IndexError) as e:
            continue
    
    # Output kết quả cuối cùng
    if current_platform is not None:
        avg_discount = total_discount / count
        print(f"{current_platform}\t{avg_discount:.2f}\t{count}\t{min_discount:.2f}\t{max_discount:.2f}")

if __name__ == "__main__":
    main()
