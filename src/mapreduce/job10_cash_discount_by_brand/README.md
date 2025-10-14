# Job 10: Cash Discount by Brand

## 📋 Mô tả
Tính tổng giá trị giảm giá tiền mặt (cash discount) theo từng thương hiệu từ dữ liệu khuyến mãi JSON, sử dụng JOIN giữa JSON promotions và CSV products.

## 🎯 Mục tiêu
- Phân tích chiến lược giảm giá trực tiếp của từng brand
- Xác định brand nào có cash discount lớn nhất
- So sánh giá trị cash discount giữa TGDĐ và CellphoneS

## 📊 Input/Output

### Input
- **JSON Files**: 
  - `data/raw/tgdd_promotions_nosql.json` (414 records)
  - `data/raw/cellphones_promotions_nosql.json` (750 records)
- **CSV Files** (để JOIN lấy brand):
  - `data/raw/tgdd_raw_data.csv`
  - `data/raw/cellphones_raw_data.csv`

### Output
```
ASUS    38500000        38.500.000đ
Acer    11900000        11.900.000đ
Apple   2800000         2.800.000đ
Asus    1400000         1.400.000đ
Dell    17500000        17.500.000đ
HP      17500000        17.500.000đ
Lenovo  37800000        37.800.000đ
MSI     14700000        14.700.000đ
MacBook 14300000        14.300.000đ
```

**Format**: `brand \t total_discount \t formatted_amount`

## 🔍 Kết quả phân tích (RAW DATA)

### Top 5 Brands - Tổng Cash Discount
```
1. ASUS     38.500.000đ (38.5M)
2. Lenovo   37.800.000đ (37.8M)
3. HP       17.500.000đ (17.5M)
4. Dell     17.500.000đ (17.5M)
5. MSI      14.700.000đ (14.7M)
```

### 💡 Key Insights

#### 1. **Cash Discount Strategy**
- **ASUS leads**: 38.5M tổng cash discount → Chiến lược aggressive pricing
- **Lenovo close 2nd**: 37.8M → Cạnh tranh trực tiếp với ASUS
- **HP & Dell tied**: 17.5M → Mid-tier cash discount strategy
- **MacBook**: 14.3M → Discount cao bất thường cho Apple ecosystem

#### 2. **Pattern Analysis**
- **Format variations detected**:
  - TGDĐ: "Giảm ngay 700,000đ" (dấu phẩy)
  - CellphoneS: "Giảm ngay 500K" (chữ K)
- **Regex patterns used**:
  ```python
  r'giảm\s+ngay\s+([\d,]+)đ'  # TGDĐ format
  r'giảm\s+ngay\s+(\d+)k\b'    # CellphoneS format
  ```

#### 3. **Data Quality Issues**
- **Case sensitivity**: "ASUS" vs "Asus" → Cần normalize
- **Duplicate brands**: "Gaming" vs "gaming"
- **244 promotions có cash discount** từ 1,164 total products (21%)

### Business Implications
1. **ASUS & Lenovo**: Dùng cash discount mạnh để cạnh tranh trong phân khúc mid-range
2. **HP & Dell**: Balanced strategy, ít cash discount hơn
3. **MacBook**: Cash discount 14.3M là bất thường → Có thể là clearance sale
4. **Low-end brands** (Avita, Huawei): 700K cash discount → Niche market

## 🛠️ Technical Implementation

### JOIN Strategy
```python
# Step 1: Load CSV to build brand mapping
brand_map = {}  # product_id → brand
for csv_file in ['tgdd_raw_data.csv', 'cellphones_raw_data.csv']:
    for row in csv.DictReader(open(csv_file, encoding='utf-8-sig')):
        product_id = row.get('id')
        brand = extract_brand(row.get('product_name'))
        brand_map[product_id] = brand

# Step 2: Process JSON and lookup brand
for json_file in promotions:
    data = json.loads(open(json_file).read())
    for item in data:
        product_id = item['product_id']
        brand = brand_map.get(product_id, "Unknown")
        
        for promo_text in item['promotions']:
            discount = extract_cash_discount(promo_text)
            if discount:
                print(f"{brand}\t{int(discount)}")
```

### Regex Extraction
```python
def extract_cash_discount(promo_text):
    promo_lower = promo_text.lower()
    
    # Pattern 1: "700,000đ" (TGDĐ)
    match = re.search(r'giảm\s+ngay\s+([\d,]+)đ', promo_lower)
    if match:
        return float(match.group(1).replace(',', ''))
    
    # Pattern 2: "500K" (CellphoneS)
    match = re.search(r'giảm\s+ngay\s+(\d+)k\b', promo_lower)
    if match:
        return float(match.group(1)) * 1000
    
    return None
```

## 🔧 Cách chạy

### Local Test
```bash
cd src/mapreduce/job10_cash_discount_by_brand
python run_local.py
```

### Hadoop Production
```bash
# Map-side JOIN with distributed cache
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files tgdd_raw_data.csv,cellphones_raw_data.csv \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/promotions_json/*.json \
  -output /output/job10_cash_discount_by_brand
```

## 📝 Mapper Logic
```python
# 1. Load CSV into memory (distributed cache)
brand_map = load_product_brands(['tgdd_raw_data.csv', 'cellphones_raw_data.csv'])

# 2. Process JSON from stdin
data = json.loads(sys.stdin.read())
for item in data:
    product_id = item['product_id']
    brand = brand_map.get(product_id, "Unknown")
    
    for promo in item['promotions']:
        discount = extract_cash_discount(promo)
        if discount:
            print(f"{brand}\t{int(discount)}")
```

## 📝 Reducer Logic
```python
# Group by brand và sum total discount
from itertools import groupby

for brand, group in groupby(sys.stdin, key=lambda x: x.split('\t')[0]):
    total = sum(int(line.split('\t')[1]) for line in group)
    formatted = f"{total:,}đ".replace(',', '.')
    print(f"{brand}\t{total}\t{formatted}")
```

## 🚨 Challenges & Solutions

### Challenge 1: BOM (Byte Order Mark) in CSV
**Problem**: CSV có `\ufeffid` thay vì `id`
```python
# Solution: Use utf-8-sig encoding
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
```

### Challenge 2: Multiple Price Formats
**Problem**: "700,000đ" vs "500K"
```python
# Solution: Multi-pattern regex với priority order
patterns = [
    r'giảm\s+ngay\s+([\d,]+)đ',  # Try comma format first
    r'giảm\s+ngay\s+(\d+)k\b'     # Then K format
]
```

### Challenge 3: JOIN Performance
**Problem**: 1,164 products × JSON lookups
```python
# Solution: In-memory hash join với dict
brand_map = {product_id: brand}  # O(1) lookup
```

## 🔄 Mở rộng

### Phiên bản cải tiến
1. **Multi-discount types**: Tặng voucher, giảm qua ngân hàng, trả góp 0%
2. **Time-based analysis**: Discount trends theo tháng
3. **Store comparison**: TGDĐ vs CellphoneS cash discount strategy

### Sample output mở rộng
```
BRAND    CASH_DISCOUNT   VOUCHER   BANK_DISCOUNT   TOTAL
ASUS     38,500,000      5,000,000 2,000,000       45,500,000
Lenovo   37,800,000      3,500,000 1,500,000       42,800,000
```

## 📚 Dependencies
- Python 3.x
- Standard library: `json`, `csv`, `re`, `sys`, `io`, `os`

## 👤 Developer
- **Đỗ Kiến Hưng** - MapReduce Developer
- Role: Design & implement JOIN pattern với distributed cache
