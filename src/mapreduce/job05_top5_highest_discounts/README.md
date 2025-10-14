# Job 05: Top 5 Highest Discounts

## Mục tiêu
Tìm **5 laptop có tỷ lệ giảm giá cao nhất** từ dữ liệu TGDĐ và CellphoneS.

## Thuật toán Top-N Pattern (2 bước)

### Bước 1: Mapper
- **Đầu vào**: CSV files (tgdd.csv, cellphones.csv)
- **Xử lý**:
  1. Đọc từng record
  2. Tính `discount_percent = ((list_price - current_price) / list_price) * 100`
  3. Extract brand từ product_name
  4. Format giá dạng dễ đọc (VD: 22.990.000đ)
- **Đầu ra**: `discount_percent (padded) \t product_info`
  - Key: `006.50` (pad để sort string = sort number, VD: 012.34)
  - Value: `product_name|current_price|list_price|brand`

### Bước 2: Reducer
- **Đầu vào**: Mapper output đã được Hadoop **sort GIẢM DẦN** theo discount_percent
- **Xử lý**:
  1. Đọc tuần tự từ stdin (đã sort)
  2. Chỉ lấy 5 records đầu tiên
  3. Gán rank (1-5)
- **Đầu ra**: `rank \t product_name \t discount% \t current_price \t list_price \t brand`

## Hadoop Streaming Command

```bash
# Upload input to HDFS
hdfs dfs -put data/raw/tgdd_raw_data.csv /raw_data/products_csv/
hdfs dfs -put data/raw/cellphones_raw_data.csv /raw_data/products_csv/

# Run MapReduce với sort DESCENDING
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
  -D stream.num.map.output.key.fields=1 \
  -D mapreduce.partition.keycomparator.options=-k1,1nr \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/*.csv \
  -output /output/job05_top5_highest_discounts \
  -file mapper.py \
  -file reducer.py

# Download output
hdfs dfs -get /output/job05_top5_highest_discounts/part-00000 job05_output.txt
```

## Giải thích Hadoop Options

- **`-D mapreduce.job.output.key.comparator.class`**: Sử dụng comparator tùy chỉnh
- **`-D stream.num.map.output.key.fields=1`**: Key là field đầu tiên (discount_percent)
- **`-D mapreduce.partition.keycomparator.options=-k1,1nr`**:
  - `-k1,1`: Sort theo field 1
  - `n`: Numeric sort
  - `r`: **Reverse (giảm dần)** - QUAN TRỌNG cho Top-N!

## Output Format

```
Rank    Product Name                             Discount%    Current Price    List Price      Brand
1       Laptop HP Pavilion 15-eg2081TU          15.00%       18.490.000đ      21.990.000đ     HP
2       Laptop Asus Vivobook 15 X1502ZA         12.50%       17.490.000đ      19.990.000đ     Asus
3       Laptop Dell Inspiron 15 3520            11.36%       19.490.000đ      21.990.000đ     Dell
4       Laptop Lenovo IdeaPad Slim 3 15IAH8     10.23%       17.990.000đ      20.040.000đ     Lenovo
5       Laptop Acer Aspire 5 A515-57            9.09%        19.990.000đ      21.990.000đ     Acer
```

## Local Test

```bash
cd src/mapreduce/job05_top5_highest_discounts
python run_local.py
```

## Lưu ý

1. **Sort descending** là quan trọng - nếu không thêm `r` trong `-k1,1nr`, sẽ lấy top 5 discount **THẤP NHẤT**!
2. **Padding key**: Mapper output `012.34` thay vì `12.34` để sort string hoạt động đúng
3. **Reducer chỉ đọc 5 dòng đầu** - tối ưu với dataset lớn
4. **Format giá**: Dùng dấu chấm (22.990.000đ) theo chuẩn Việt Nam

## So sánh với Sorting toàn bộ

| Phương pháp | Memory | Speed | Scalability |
|-------------|--------|-------|-------------|
| Sort all → take 5 | High | Slow | Poor |
| **Top-N pattern** | Low | Fast | Excellent |

Top-N pattern phù hợp với Big Data vì chỉ cần **1 lần scan** qua sorted data!
