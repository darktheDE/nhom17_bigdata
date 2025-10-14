# Job 06: Average Promotions per Store

## Mục tiêu
So sánh **số khuyến mãi trung bình** mỗi sản phẩm giữa **TGDĐ** và **CellphoneS** để đánh giá chiến lược khuyến mãi.

## Input Data
- **tgdd_promo.json**: Promotions từ TheGioiDiDong
- **cellphones_promo.json**: Promotions từ CellphoneS

Format JSON:
```json
[
  {
    "product_name": "Laptop HP...",
    "promotions": [
      "Tặng balo...",
      "Giảm 500.000đ...",
      "Trả góp 0%..."
    ]
  }
]
```

## Thuật toán

### Mapper
- **Đầu vào**: JSON files
- **Xử lý**:
  1. Detect store name (từ file name hoặc environment variable)
  2. Với mỗi sản phẩm: đếm `len(promotions)`
  3. Output: `store_name \t num_promotions` (1 dòng per product)
  
### Reducer
- **Đầu vào**: Mapper output đã sort theo store_name
- **Xử lý**:
  1. Group by store_name
  2. Tính: `avg = sum(promotions) / count(products)`
  3. Output: `store_name \t avg_promotions \t total_products`

## Hadoop Streaming Command

```bash
# Upload JSON to HDFS
hdfs dfs -put data/raw/tgdd_promotions_nosql.json /raw_data/promotions_json/
hdfs dfs -put data/raw/cellphones_promotions_nosql.json /raw_data/promotions_json/

# Run MapReduce
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/promotions_json/*.json \
  -output /output/job06_avg_promotions_per_store \
  -file mapper.py \
  -file reducer.py

# Download output
hdfs dfs -get /output/job06_avg_promotions_per_store/part-00000 job06_output.txt
```

## Store Detection Strategy

Có 3 cách detect store name:

1. **Từ file name** (trong mapper.py):
   ```python
   if 'tgdd' in filename.lower():
       store = "TGDĐ"
   elif 'cellphone' in filename.lower():
       store = "CellphoneS"
   ```

2. **Từ data field** (nếu JSON có field `source` hoặc `store`):
   ```python
   store_name = item.get('source', 'Unknown')
   ```

3. **Từ environment variable** (local test):
   ```python
   store_name = os.environ.get('STORE_NAME', 'Unknown')
   ```

## Output Format

```
Store Name      Avg Promotions  Total Products
TGDĐ            3.60            10
CellphoneS      2.90            10
```

**Phân tích**:
- TGDĐ: 3.60 khuyến mãi/sản phẩm → Chiến lược generous hơn
- CellphoneS: 2.90 khuyến mãi/sản phẩm

## Local Test

```bash
cd src/mapreduce/job06_avg_promotions_per_store
python run_local.py
```

## Business Insights

Metric này giúp trả lời:
1. Cửa hàng nào "chơi lớn" hơn về khuyến mãi?
2. Chiến lược nào hiệu quả: nhiều KM nhỏ vs ít KM lớn?
3. Điều chỉnh chiến lược cạnh tranh như thế nào?

## Lưu ý Implementation

- **Environment variable**: Local test dùng `STORE_NAME`, Hadoop phải detect từ filename
- **JSON format**: File là 1 array lớn, không phải line-delimited JSON
- **Empty promotions**: Sản phẩm có `promotions: []` → count = 0 (vẫn tính vào average)
