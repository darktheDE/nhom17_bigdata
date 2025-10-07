# MapReduce Jobs - Hướng Dẫn

## 📋 Danh Sách 10 Jobs

### ✅ Job 01: Brand Count
- **Mục đích:** Đếm số lượng laptop theo thương hiệu
- **Input:** raw/laptops.csv
- **Output:** brand \t count
- **Ví dụ:** HP \t 150, Dell \t 120, Asus \t 100
- **Status:** ✅ Đã có template

### ✅ Job 02: Word Count  
- **Mục đích:** Phân tích từ khóa phổ biến trong tên sản phẩm laptop
- **Input:** raw/laptops.csv
- **Output:** keyword \t frequency
- **Ví dụ:** inspiron \t 45, ideapad \t 38, vivobook \t 32
- **Status:** ✅ Đã có template

### ⏳ Job 03: Price Range Analysis
- **Mục đích:** Phân loại laptop theo phân khúc giá
- **Input:** raw/laptops.csv
- **Output:** price_range \t count \t avg_price
- **Phân khúc:** Dưới 15tr (Budget), 15-25tr (Mid-range), 25-35tr (Premium), Trên 35tr (High-end)

### ⏳ Job 04: RAM/Storage Distribution
- **Mục đích:** Phân tích phân bố cấu hình RAM và Storage
- **Input:** raw/laptops.csv
- **Output:** ram_storage_config \t count
- **Ví dụ:** 16GB_512GB \t 350, 8GB_256GB \t 180

### ⏳ Job 05: Rating by Brand
- **Mục đích:** Tính đánh giá trung bình theo thương hiệu
- **Input:** raw/laptops.csv
- **Output:** brand \t avg_rating \t product_count
- **Ví dụ:** MacBook \t 4.95 \t 25, Dell \t 4.88 \t 120

### ⏳ Job 06: Discount Analysis
- **Mục đích:** Phân tích mức giảm giá (list_price - current_price)
- **Input:** raw/laptops.csv
- **Output:** brand \t avg_discount_percent \t max_discount
- **Ví dụ:** HP \t 11.2% \t 20%

### ⏳ Job 07: CPU Analysis
- **Mục đích:** Thống kê các loại CPU phổ biến (Intel i3/i5/i7, AMD R5/R7, Apple M)
- **Input:** raw/laptops.csv
- **Output:** cpu_family \t count \t avg_price
- **Ví dụ:** Intel i5 \t 280, AMD R5 \t 150, Apple M \t 45

### ⏳ Job 09: OS Distribution
- **Mục đích:** Phân bố hệ điều hành (Windows 11 vs macOS)
- **Input:** raw/laptops.csv
- **Output:** os \t count \t market_share_percent \t avg_price
- **Ví dụ:** Windows 11 \t 850 \t 85% \t 18500000

### ⏳ Job 10: Price-Rating Correlation
- **Mục đích:** Phân tích mối tương quan giữa giá và đánh giá
- **Input:** raw/laptops.csv
- **Output:** price_range \t avg_rating \t product_count
- **Ví dụ:** 25-35tr \t 4.92 \t 120

### ⏳ Job 08: Discount Comparison by Platform
- **Mục đích:** So sánh tỷ lệ giảm giá giữa các sàn thương mại điện tử
- **Input:** raw/laptops.csv
- **Output:** source_website \t avg_discount_percent \t max_discount
- **Ví dụ:** thegioididong.com \t 12.5% \t 25%, cellphones.com.vn \t 10.8% \t 22%

---

## 🚀 Cách Chạy MapReduce Job

### 1. Chuẩn Bị
```bash
# Upload dữ liệu lên HDFS
hdfs dfs -mkdir -p /user/bigdata/laptops/raw
hdfs dfs -put data/raw/laptops.csv /user/bigdata/laptops/raw/

# Kiểm tra
hdfs dfs -ls /user/bigdata/laptops/raw/
```

### 2. Chạy Job (Ví dụ Job 01)
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files src/mapreduce/job01_brand_count/mapper.py,src/mapreduce/job01_brand_count/reducer.py \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /user/bigdata/laptops/raw/laptops.csv \
  -output /user/bigdata/laptops/output/job01_brand_count
```

### 3. Xem Kết Quả
```bash
# Xem output
hdfs dfs -cat /user/bigdata/laptops/output/job01_brand_count/part-00000

# Hoặc download về
hdfs dfs -get /user/bigdata/laptops/output/job01_brand_count/ ./output/
```

### 4. Chạy Tất Cả Jobs (Script)
```bash
#!/bin/bash
# run_all_jobs.sh

for i in {01..10}; do
    echo "Running Job $i..."
    
    job_dir="src/mapreduce/job${i}_*"
    output_dir="/user/bigdata/laptops/output/job${i}_*"
    
    # Xóa output cũ nếu có
    hdfs dfs -rm -r $output_dir
    
    # Chạy job
    hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
      -files ${job_dir}/mapper.py,${job_dir}/reducer.py \
      -mapper "python3 mapper.py" \
      -reducer "python3 reducer.py" \
      -input /user/bigdata/laptops/raw/laptops.csv \
      -output $output_dir
    
    echo "Job $i completed!"
done
```

---

## 📝 Template Mapper/Reducer

### Mapper Template
```python
#!/usr/bin/env python3
import sys

def mapper():
    for line in sys.stdin:
        line = line.strip()
        
        # Bỏ qua header
        if line.startswith('id,'):
            continue
        
        try:
            fields = line.split(',')
            # Xử lý dữ liệu
            # ...
            # Emit: key \t value
            print(f"{key}\t{value}")
        except:
            continue

if __name__ == "__main__":
    mapper()
```

### Reducer Template
```python
#!/usr/bin/env python3
import sys
from collections import defaultdict

def reducer():
    data = defaultdict(int)  # hoặc list, dict tùy logic
    
    for line in sys.stdin:
        line = line.strip()
        try:
            key, value = line.split('\t')
            # Aggregate data
            # ...
        except:
            continue
    
    # Emit results
    for key, result in data.items():
        print(f"{key}\t{result}")

if __name__ == "__main__":
    reducer()
```

---

## 🐛 Troubleshooting

### Lỗi: "No such file or directory"
- Kiểm tra đường dẫn HDFS: `hdfs dfs -ls /user/bigdata/laptops/`

### Lỗi: "Output directory already exists"
- Xóa output cũ: `hdfs dfs -rm -r /user/bigdata/laptops/output/jobXX_*`

### Lỗi: "Permission denied"
- Cấp quyền: `hdfs dfs -chmod -R 777 /user/bigdata/`

---

## 📊 Kết Quả Mong Đợi

Sau khi chạy xong 10 jobs, bạn sẽ có:
- 10 thư mục output trên HDFS
- Mỗi thư mục chứa file part-00000 với kết quả đã tổng hợp
- Data Analyst (Anh Thịnh) sẽ dùng Hive để query các kết quả này
