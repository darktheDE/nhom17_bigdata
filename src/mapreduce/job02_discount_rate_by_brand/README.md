# Job 02: Tính Tỷ Lệ Giảm Giá Trung Bình Theo Hãng

## Mô tả
Tính tỷ lệ giảm giá trung bình (discount percentage) cho mỗi hãng laptop để xác định hãng nào đang có chương trình giảm giá "mạnh tay" nhất.

## Công thức
```
discount_percentage = ((list_price - current_price) / list_price) * 100
```

## Input
- CSV files với cột `current_price` và `list_price`

## Output
Format: `brand \t average_discount_percentage%`

Ví dụ:
```
Acer	7.06%
Asus	9.18%
Dell	7.46%
HP	11.69%
Lenovo	8.91%
MacBook	3.75%
```

## Chạy Local Test
```bash
cd src/mapreduce/job02_discount_rate_by_brand
python run_local.py
```

## Chạy trên Hadoop Streaming
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/* \
  -output /output/job02_discount_rate_by_brand \
  -file src/mapreduce/job02_discount_rate_by_brand/mapper.py \
  -file src/mapreduce/job02_discount_rate_by_brand/reducer.py
```

## Logic
- **Mapper**: Tính discount % cho mỗi sản phẩm, output `brand \t discount_percentage`
- **Reducer**: Tính trung bình discount % cho mỗi brand
