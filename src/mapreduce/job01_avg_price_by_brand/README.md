# Job 01: Tính Giá Bán Trung Bình Theo Hãng

## Mô tả
Chương trình MapReduce tính giá bán trung bình (current_price) cho mỗi hãng laptop (HP, Dell, Asus, Lenovo, MacBook...).

## Input
- `tgdd.csv`: Dữ liệu từ Thế Giới Di Động
- `cellphones.csv`: Dữ liệu từ CellphoneS

## Output
Format: `brand \t average_price`

Ví dụ:
```
Acer	14490000.00
Asus	8749666.67
Dell	16740000.00
HP	14690000.00
Lenovo	8182000.00
MacBook	15419500.00
```

## Chạy Local Test
```bash
cd src/mapreduce/job01_avg_price_by_brand
python run_local.py
```

Output: `data/output_mapreduce/job01_avg_price_by_brand.txt`

## Chạy trên Hadoop Streaming

### Bước 1: Upload input lên HDFS (nếu chưa có)
```bash
hdfs dfs -mkdir -p /raw_data/products_csv
hdfs dfs -put data/raw/tgdd_raw_data.csv /raw_data/products_csv/
hdfs dfs -put data/raw/cellphones_raw_data.csv /raw_data/products_csv/
```

### Bước 2: Chạy MapReduce job
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/* \
  -output /output/job01_avg_price_by_brand \
  -file src/mapreduce/job01_avg_price_by_brand/mapper.py \
  -file src/mapreduce/job01_avg_price_by_brand/reducer.py
```

### Bước 3: Xem kết quả
```bash
hdfs dfs -cat /output/job01_avg_price_by_brand/part-00000
```

### Bước 4: Download về local (tùy chọn)
```bash
hdfs dfs -get /output/job01_avg_price_by_brand/part-00000 data/output_mapreduce/job01_avg_price_by_brand.txt
```

## Logic xử lý

### Mapper (mapper.py)
1. Đọc CSV từ stdin
2. Extract brand (từ cột `brand` nếu có, hoặc parse từ `product_name`)
3. Clean price (xử lý cả format TGDĐ số và CellphoneS string "22.990.000đ")
4. Output: `brand \t price`

### Reducer (reducer.py)
1. Nhận input đã sort theo brand
2. Tính tổng giá và đếm số lượng cho mỗi brand
3. Output: `brand \t average_price`

## Lưu ý quan trọng
- **Encoding**: Code tự động xử lý UTF-8 cho Hadoop Streaming
- **Price cleaning**: Hỗ trợ cả 2 format giá từ TGDĐ và CellphoneS
- **Brand extraction**: Ưu tiên dùng cột `brand`, fallback sang parse `product_name`
- **Error handling**: Skip các row có giá không hợp lệ ("Liên hệ để báo giá", N/A)
