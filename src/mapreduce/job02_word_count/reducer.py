#!/usr/bin/env python3
"""
MapReduce Job 02: Word Count
Reducer - Tổng hợp số lần xuất hiện của từ khóa
Input: word \t 1
Output: word \t count
"""

import sys
from collections import defaultdict

def reducer():
    word_counts = defaultdict(int)
    
    for line in sys.stdin:
        line = line.strip()
        
        try:
            word, count = line.split('\t')
            word_counts[word] += int(count)
        except:
            continue
    
    # Xuất kết quả (top keywords)
    for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True):
        if count >= 5:  # Chỉ lấy từ xuất hiện >= 5 lần
            print(f"{word}\t{count}")

if __name__ == "__main__":
    reducer()
