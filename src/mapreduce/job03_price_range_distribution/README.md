# Job 03: Phân Bổ Sản Phẩm Theo Khoảng Giá

## Mô tả
Đếm số lượng sản phẩm laptop trong từng phân khúc giá để phân tích sự phân bổ sản phẩm trên thị trường.

## Phân khúc giá
- **Duoi_15_trieu**: Giá < 15,000,000 VND
- **15_25_trieu**: 15,000,000 <= Giá < 25,000,000 VND  
- **Tren_25_trieu**: Giá >= 25,000,000 VND

## Input
- CSV files với cột `current_price` hoặc `current_price_raw`

## Output
Format: `price_range \t count`

Ví dụ:
```
15_25_trieu	4
Tren_25_trieu	13
```

## Chạy Local Test
```bash
cd src/mapreduce/job03_price_range_distribution
python run_local.py
```

## Chạy trên Hadoop Streaming
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/* \
  -output /output/job03_price_range_distribution \
  -file src/mapreduce/job03_price_range_distribution/mapper.py \
  -file src/mapreduce/job03_price_range_distribution/reducer.py
```

## Logic
- **Mapper**: Phân loại giá vào khoảng, output `price_range \t 1`
- **Reducer**: Đếm tổng số cho mỗi khoảng giá
