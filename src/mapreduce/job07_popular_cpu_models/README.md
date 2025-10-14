# MapReduce Job 11: Thống kê các dòng CPU phổ biến nhất

## Mục tiêu
Phân tích xem những dòng CPU nào (ví dụ: i5-13420H, R5-7520U, i7-13620H, M4) đang được các nhà bán lẻ ưu tiên sử dụng nhiều nhất. Insight này cực kỳ giá trị để nhận định xu hướng cấu hình của thị trường laptop.

## Input
- **File CSV**: `tgdd.csv`, `cellphones.csv`
- **Columns sử dụng**: 
  - `raw_specs_string`: Chuỗi cấu hình (CellphoneS)
  - `cpu`: Cột CPU riêng (TGDD)

## Output
```
CPU_MODEL    COUNT
I5-13420H    45
R5-7520U     38
I7-13620H    32
M4           28
...
```

## Logic MapReduce

### Mapper (`mapper.py`)
1. Đọc từng dòng CSV
2. Trích xuất mã CPU từ `raw_specs_string` hoặc cột `cpu` sử dụng regex:
   - **Intel**: `i3, i5, i7, i9` (pattern: `i\d-\d{4,5}[A-Z]{1,3}`)
   - **AMD Ryzen**: `R3, R5, R7, R9` (pattern: `R\d\s\d{4,5}[A-Z]{1,3}`)
   - **Apple**: `M1, M2, M3, M4` (pattern: `M\d( PRO| MAX)?`)
   - **Intel Core**: `Core 5, Core 7` (pattern: `Core \d-\d{3,5}[A-Z]+`)
   - **Intel Ultra**: `U9` (pattern: `U\d{1,2}-\d{3}[A-Z]+`)
3. Chuẩn hóa mã CPU (viết hoa, loại bỏ khoảng trắng thừa)
4. Output: `(cpu_model, 1)`

**Ví dụ:**
```
Input:  "I7-13620H/16GB/512GB PCIE/VGA 6GB RTX4050"
Output: I7-13620H    1

Input:  "R5 7520U, 16GB, 512GB"
Output: R5-7520U    1

Input:  "M4 Pro 14CPU 20GPU"
Output: M4-PRO    1
```

### Reducer (`reducer.py`)
1. Nhận dữ liệu đã được sort theo `cpu_model`
2. Đếm tổng số lần xuất hiện của mỗi CPU
3. Output: `(cpu_model, total_count)`

## Cách chạy

### 1. Chạy local test (Python subprocess)
```bash
cd src/mapreduce/job11_popular_cpu_models
python run_local.py
```

### 2. Chạy trên Hadoop Streaming (Production)
```bash
# Trên Ubuntu/WSL2
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/tgdd_raw_data.csv \
  -input /raw_data/products_csv/cellphones_raw_data.csv \
  -output /output/job11_popular_cpu_models \
  -file mapper.py \
  -file reducer.py
```

### 3. Xem kết quả
```bash
# Local
cat ../../../data/output_raw/job11_popular_cpu_models.txt

# HDFS
hdfs dfs -cat /output/job11_popular_cpu_models/part-00000
```

## Business Value
1. **Xu hướng thị trường**: Xác định các dòng CPU đang "hot" nhất
2. **Chiến lược kinh doanh**: Nhà bán lẻ ưu tiên stock CPU nào?
3. **Phân khúc sản phẩm**: CPU nào phủ sóng nhiều phân khúc giá?
4. **So sánh cửa hàng**: TGDĐ vs CellphoneS có xu hướng CPU khác nhau không?

## Sample Output
Dựa trên sample data, kết quả mong đợi:
- Intel i5/i7 series 13xxx (thế hệ 13) sẽ chiếm ưu thế
- AMD Ryzen 5/7 7xxx series cũng phổ biến
- Apple M4 xuất hiện ở phân khúc cao cấp
- CPU cũ hơn (i3, Ryzen 3) ít hơn
