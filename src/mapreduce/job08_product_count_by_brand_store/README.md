# MapReduce Job 14: Đếm sản phẩm theo thương hiệu & cửa hàng

## Mục tiêu
Một trong những phân tích cạnh tranh cơ bản và quan trọng nhất là so sánh **danh mục sản phẩm (inventory)**. Job này đếm xem mỗi cửa hàng đang kinh doanh bao nhiêu mẫu laptop của từng thương hiệu.

## Input
- **File CSV**: `tgdd.csv`, `cellphones.csv`
- **Columns sử dụng**: 
  - `product_name`: Trích xuất brand
  - `brand`: Cột brand (nếu có)
  - `product_url`: Xác định source

## Output
```
BRAND       TGDD    CELLPHONES    TOTAL    DIFFERENCE
Asus        45      38            83       7
Lenovo      42      40            82       2
HP          35      28            63       7
Dell        30      25            55       5
MacBook     18      22            40       4
```

## Logic MapReduce

### Mapper (`mapper.py`)
1. Đọc từng dòng CSV
2. Trích xuất `brand`:
   - Ưu tiên cột `brand` nếu có (TGDD)
   - Fallback: extract từ `product_name` (CellphoneS)
3. Xác định `source` từ `product_url`:
   - `thegioididong.com` → `thegioididong`
   - `cellphones.com.vn` → `cellphones`
4. Tạo **composite key**: `(brand, source)`
5. Output: `(brand,source, 1)`

**Ví dụ:**
```
Input (TGDD):  "Laptop HP 15...", url="...thegioididong.com..."
Output: HP,thegioididong    1

Input (CellphoneS):  "Laptop Lenovo IdeaPad...", url="...cellphones.com.vn..."
Output: Lenovo,cellphones    1
```

### Reducer (`reducer.py`)
1. Nhận dữ liệu đã được sort theo composite key `(brand,source)`
2. Đếm tổng cho mỗi cặp
3. Output: `(brand, source, count)`

**Output format:**
```
Asus    thegioididong    45
Asus    cellphones       38
Dell    thegioididong    30
Dell    cellphones       25
...
```

## Cách chạy

### 1. Chạy local test (Python subprocess)
```bash
cd src/mapreduce/job14_product_count_by_brand_store
python run_local.py
```

### 2. Chạy trên Hadoop Streaming (Production)
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/tgdd_raw_data.csv \
  -input /raw_data/products_csv/cellphones_raw_data.csv \
  -output /output/job14_product_count_by_brand_store \
  -file mapper.py \
  -file reducer.py
```

### 3. Xem kết quả
```bash
# Local
cat ../../../data/output_raw/job14_product_count_by_brand_store.txt

# HDFS
hdfs dfs -cat /output/job14_product_count_by_brand_store/part-00000
```

## Business Value

### 1. Chiến lược Inventory
- **Thương hiệu nào được ưu tiên?**: Cửa hàng nào stock nhiều Asus/Dell hơn?
- **Đa dạng sản phẩm**: Số lượng SKU của mỗi brand

### 2. Partnership & Deals
- **Exclusive deals**: Brand nào chỉ có ở một cửa hàng?
- **Supplier relationship**: Cửa hàng nào có quan hệ tốt hơn với HP/Dell?

### 3. Market Positioning
- **TGDĐ focus**: Phân khúc phổ thông (HP, Asus)
- **CellphoneS focus**: Cao cấp hơn (MacBook, MSI Gaming)

### 4. Competitive Intelligence
- **Gap analysis**: Brand nào đối thủ có mà mình chưa có?
- **Assortment planning**: Nên thêm/bớt brand nào?

## Composite Key Pattern
Job này minh họa kỹ thuật **Composite Key** trong MapReduce:

```python
# Mapper output
key = f"{brand},{source}"  # "Asus,thegioididong"

# Hadoop tự động sort theo composite key:
# Asus,cellphones
# Asus,thegioididong
# Dell,cellphones
# Dell,thegioididong
```

**Ưu điểm**:
- Tự động group theo nhiều chiều
- Reducer nhận data đã organize tốt
- Dễ phân tích so sánh

## Sample Insights
Từ sample data, có thể phát hiện:
- **Lenovo IdeaPad**: Cả 2 cửa hàng đều stock mạnh (phân khúc sinh viên)
- **MacBook**: CellphoneS có nhiều variant hơn (chuyên Apple)
- **Asus Gaming (ROG/TUF)**: TGDĐ stock nhiều hơn
- **Dell Latitude**: Cả 2 đều ít (thị trường doanh nghiệp)

## Post-processing
Kết quả có thể dùng để:
1. **Pivot Table**: Tạo bảng so sánh trực quan
2. **Heatmap**: Visualize độ phủ sóng
3. **Dashboard**: Real-time inventory comparison
4. **Alert system**: Notify khi gap quá lớn
