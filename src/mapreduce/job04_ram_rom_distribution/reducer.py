#!/usr/bin/env python3
"""
MapReduce Job 04: RAM/Storage Distribution
Reducer - Tổng hợp số lượng theo cấu hình
Input: ram_storage_config \t 1
Output: ram_storage_config \t count
"""

import sys
from collections import defaultdict

def reducer():
    config_counts = defaultdict(int)
    
    for line in sys.stdin:
        line = line.strip()
        
        try:
            config, count = line.split('\t')
            config_counts[config] += int(count)
        except (ValueError, IndexError):
            continue
    
    # Xuất kết quả, sort theo count giảm dần
    for config, count in sorted(config_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{config}\t{count}")

if __name__ == "__main__":
    reducer()
