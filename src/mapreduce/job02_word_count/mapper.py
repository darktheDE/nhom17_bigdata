#!/usr/bin/env python3
"""
MapReduce Job 02: Word Count
Mapper - Đếm từ khóa trong tên sản phẩm
Input: CSV file với cột product_name
Output: word \t 1
"""

import sys
import re

def mapper():
    # Từ cần loại bỏ (stop words)
    stop_words = {'gb', 'mb', 'tb', 'inch', 'mah', 'và', 'của', 'cho', 'với'}
    
    for line in sys.stdin:
        line = line.strip()
        
        # Bỏ qua dòng header
        if line.startswith('id,'):
            continue
        
        try:
            fields = line.split(',')
            
            if len(fields) < 2:
                continue
            
            product_name = fields[1].strip().strip('"').lower()
            
            # Tách từ
            words = re.findall(r'\b[a-z0-9]+\b', product_name)
            
            for word in words:
                if word not in stop_words and len(word) > 2:
                    print(f"{word}\t1")
                    
        except:
            continue

if __name__ == "__main__":
    mapper()
