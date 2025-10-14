# MapReduce Jobs - Laptop Price Analysis System

## 📋 Tổng quan

Bộ **10 chương trình MapReduce** phân tích dữ liệu giá laptop và khuyến mãi từ **TheGioiDiDong** (TGDĐ) và **CellphoneS** để phục vụ phân tích thị trường cạnh tranh.

**Tổng số sản phẩm phân tích**: 1,164 laptops (919 có giá hợp lệ)
- **TGDĐ**: 414 sản phẩm
- **CellphoneS**: 750 sản phẩm

**Cách chạy toàn bộ**: Từ thư mục gốc project, chạy:
```bash
python run_all_10_jobs.py
```

**Thời gian chạy**: ~2.4 giây (10 jobs hoàn thành)

---

## 🎯 Danh sách 10 Jobs

| # | Job Name | Input | Output | Insight chính |
|---|----------|-------|--------|---------------|
| 01 | Avg Price by Brand | CSV | 15 brands analyzed | Gigabyte đắt nhất (172.6M), Masstel rẻ nhất (3.6M) |
| 02 | Discount Rate by Brand | CSV | 15 brands analyzed | Masstel giảm 44.68%, Apple chỉ 11.74% |
| 03 | Price Range Distribution | CSV | 3 ranges | 65.5% thị trường >25M (cao cấp) |
| 04 | Promotion Keyword Freq | JSON | 24 keywords | "Tặng" phổ biến nhất (3,646 lần) |
| 05 | Top 5 Highest Discounts | CSV | 5 products | LG Gram giảm tới 44% |
| 06 | Avg Promotions/Store | JSON | 2 stores | TGDĐ: 9.54 KM/sp, CellphoneS: 3.99 KM/sp |
| 07 | Popular CPU Models | CSV | 92 CPU models | Intel i5-13420H phổ biến nhất (62 sp) |
| 08 | Brand Count by Store | CSV | 20 brands × 2 stores | Lenovo nhiều nhất (221 sp), ASUS có case sensitivity issue |
| 09 | Office License Count | CSV | TGDĐ only | 0 sản phẩm có Office H&S (data quality issue) |
| 10 | Cash Discount by Brand | JSON+CSV | 17 brands | ASUS cash discount cao nhất (38.5M) |

---

## 🎯 Kết quả phân tích (Tập dữ liệu đầy đủ)

### **Job 01: Giá trung bình theo thương hiệu**
📊 **Insight**: Gigabyte và MSI là 2 thương hiệu đắt nhất, Masstel rẻ nhất

| Thương hiệu | Giá trung bình (VNĐ) | Phân khúc |
|-------------|---------------------|-----------|
| Gigabyte | 172.610.000 | Premium |
| MSI | 166.190.450 | Premium |
| Dell | 154.937.400 | Premium |
| HP | 162.387.009 | Premium |
| Lenovo | 128.455.587 | Trung cấp |
| Asus | 99.233.889 | Trung cấp |
| MacBook | 109.173.562 | Cao cấp (Apple) |
| Acer | 118.340.000 | Trung cấp |
| Samsung | 83.400.000 | Tầm trung |
| LG | 24.623.333 | Phổ thông |
| Masstel | 3.590.000 | Giá rẻ |

---

### **Job 02: Tỷ lệ giảm giá theo thương hiệu**
📊 **Insight**: Masstel và LG có chiết khấu cao nhất, Apple/MacBook ít giảm giá nhất

| Thương hiệu | Discount Rate | Chiến lược |
|-------------|---------------|------------|
| **Masstel** | **44.68%** | Aggressive pricing |
| **LG** | **34.89%** | Clearance sale |
| **Samsung** | **22.84%** | Promotion-heavy |
| **Gaming** | **17.17%** | Niche market |
| **HP** | **14.85%** | Competitive |
| **ASUS** | **13.71%** | Standard |
| Apple | 11.74% | Premium stable |
| Asus | 10.98% | Conservative |
| MacBook | 10.61% | Minimal discount |
| Acer | 10.62% | Value-focused |
| iMac | 5.21% | Luxury segment |

**Phân tích**:
- Brands "Gaming" và "gaming" là case sensitivity issue → cần normalize
- LG có discount 34.89% → có thể đang thanh lý model cũ
- Apple ecosystem (MacBook, iMac) giữ giá tốt (~5-11%)

---

### **Job 03: Phân bố theo khoảng giá**
📊 **Insight**: 65% thị trường ở phân khúc >25 triệu (cao cấp)

```
Tổng: 919 sản phẩm có giá hợp lệ

Dưới 15 triệu:    91 sản phẩm ( 9.9%) ████
15-25 triệu:     226 sản phẩm (24.6%) ███████████
Trên 25 triệu:   602 sản phẩm (65.5%) ███████████████████████████
```

**Business implication**:
- Thị trường thiên về cao cấp (gaming, workstation)
- Phân khúc phổ thông (<15M) ít cạnh tranh
- Sweet spot: 15-25M (24.6% thị phần)

---

### **Job 04: Tần suất từ khóa khuyến mãi**
📊 **Insight**: "Tặng" là chiến thuật phổ biến nhất (3,646 lần)

**Top 15 keywords** (từ 16,464 promotion records):

| Keyword | Tần suất | % |
|---------|----------|---|
| **Tặng** | 3,646 | 22.1% |
| **Phiếu Mua Hàng** | 2,399 | 14.6% |
| **Giảm** | 2,085 | 12.7% |
| **Trả góp 0%** | 1,442 | 8.8% |
| Balo | 950 | 5.8% |
| Tai Nghe | 832 | 5.1% |
| Màn Hình | 772 | 4.7% |
| Pin Dự Phòng | 736 | 4.5% |
| Voucher | 525 | 3.2% |
| Bảo Hành | 523 | 3.2% |
| Win11 | 523 | 3.2% |
| Ưu Đãi | 523 | 3.2% |
| Trả Góp | 522 | 3.2% |
| Máy In | 405 | 2.5% |
| Túi | 353 | 2.1% |

**Chiến lược khuyến mãi**:
1. **Quà tặng vật lý** (Balo, Tai nghe, Pin, Chuột): 2,850 lần
2. **Giảm giá trực tiếp**: 2,085 lần
3. **Tài chính** (Trả góp 0%): 1,964 lần
4. **Voucher/Phiếu**: 2,924 lần

---

### **Job 05: Top 5 Laptop giảm giá cao nhất**
📊 **Insight**: Clearance sale LG Gram chiếm 3/5 vị trí

| Rank | Sản phẩm | Discount | Giá hiện tại | Giá gốc | Brand |
|------|----------|----------|--------------|---------|-------|
| 🥇 1 | Laptop Masstel E140 Celeron | **44.68%** | 3.590.000đ | 6.490.000đ | Masstel |
| 🥈 2 | Laptop LG Gram 2023 16Z90R-E.AH75A5 | **44.01%** | 27.990.000đ | 49.990.000đ | LG |
| 🥉 3 | Laptop LG Gram 2024 14Z90S-G.AH75A5 | **43.25%** | 23.490.000đ | 41.390.000đ | LG |
| 4 | Laptop MSI Modern 15 B13M-297VN (Cũ Đẹp) | **42.29%** | 12.690.000đ | 21.990.000đ | MSI |
| 5 | Laptop LG Gram 2024 14Z90S-G.AH55A5 | **42.16%** | 20.990.000đ | 36.290.000đ | LG |

**Phân tích**:
- LG đang có chương trình thanh lý mạnh (3/5 top deals)
- MSI "Cũ Đẹp" → refurbished market
- Masstel discount 44.68% nhưng giá tuyệt đối thấp (3.59M)

---

### **Job 06: So sánh số khuyến mãi giữa 2 cửa hàng**
📊 **Insight**: TGDĐ "chơi lớn" hơn CellphoneS gấp 2.4 lần

```
┌─────────────┬───────────────────┬──────────────┐
│ Cửa hàng   │ Avg KM/sản phẩm   │ Tổng SP      │
├─────────────┼───────────────────┼──────────────┤
│ TGDĐ        │ 9.54              │ 414          │
│ CellphoneS  │ 3.99              │ 750          │
└─────────────┴───────────────────┴──────────────┘
```

**Business implication**:
- TGDĐ: Chiến lược "nhiều khuyến mãi" để tăng perceived value
- CellphoneS: Chiến lược "giá tốt từ đầu", ít combo deal
- Avg 9.54 KM/sp của TGDĐ → có thể gây overwhelm cho khách

---

### **Job 07: CPU phổ biến nhất**
📊 **Top 5 CPU models** (từ 92 models):

| CPU Model | Số lượng | % | Phân khúc |
|-----------|----------|---|-----------|
| **i5-13420H** | 62 | 8.0% | Mid-range laptop |
| **i7-13620H** | 58 | 7.5% | High-end gaming |
| **i5-1334U** | 34 | 4.4% | Ultrabook |
| **i5-1235U** | 33 | 4.3% | Business laptop |
| **i7-1355U** | 33 | 4.3% | Premium ultrabook |

**Insight**:
- **Intel dominates**: Top 20 đều là Intel (Core i5/i7 gen 12-14)
- **13th Gen leads**: i5-13420H (62 sp), i7-13620H (58 sp) phổ biến nhất
- **U-series vs H-series**: 
  - U-series (ultrabook): ~35% (i5-1334U, i5-1235U, i7-1355U)
  - H-series (performance): ~65% (i5-13420H, i7-13620H)
- **AMD Ryzen**: Thiếu vắng trong top 20 → Intel monopoly

**Business implication**:
- Thị trường thiên về **performance laptops** (H-series)
- Cơ hội cho AMD nếu muốn tăng thị phần
- i5-13420H là sweet spot (giá/hiệu năng)

---

### **Job 08: Số lượng sản phẩm theo Brand & Store**
📊 **Top 5 Brands** (tổng sản phẩm):

| Brand | TGDĐ | CellphoneS | Tổng | Chênh lệch |
|-------|------|------------|------|------------|
| **Lenovo** | 67 | 154 | 221 | +87 (CPS) |
| **HP** | 81 | 83 | 164 | +2 (CPS) |
| **Dell** | 64 | 83 | 147 | +19 (CPS) |
| **MSI** | 47 | 92 | 139 | +45 (CPS) |
| **Asus** | 78 | 1 | 79 | +77 (TGDĐ) |

**Critical Data Quality Issue**:
- **ASUS case sensitivity**: "ASUS" (CellphoneS) vs "Asus" (TGDĐ)
  - CellphoneS có **77 sản phẩm "ASUS"** (uppercase)
  - TGDĐ có **78 sản phẩm "Asus"** (mixed case)
  - **Nếu merge**: ASUS sẽ là #3 với 155 sản phẩm!

**Inventory Strategy**:
- **CellphoneS**: Mạnh về Lenovo (154), MSI (92), Dell (83)
- **TGDĐ**: Mạnh về Asus (78), HP (81)
- **Apple ecosystem**: Chỉ có ở CellphoneS (MacBook 62, iMac 8, Mac 13)

---

### **Job 09: Đếm laptop có Office license**
📊 **Kết quả**: 0/414 sản phẩm có Office Home & Student

```
No Office: 414 sản phẩm (100%)
```

**Phân tích**:
- Chỉ TGDĐ có cột `software`, CellphoneS không có
- TGDĐ dataset này không có product nào preinstall Office
- Có thể Office là option mua thêm, không list trong specs
- **Data quality concern**: Cột `software` đều là "N/A"

**Business recommendation**:
- Rescrape với pattern mới để capture Office info
- Hoặc analyze từ promotions ("Tặng Microsoft 365")
- Expand sang Windows license analysis

---

### **Job 10: Tổng giá trị giảm giá bằng tiền mặt**
📊 **Top 5 Brands - Cash Discount**:

| Brand | Tổng Cash Discount | Số sản phẩm ước tính | Avg/sp |
|-------|-------------------|----------------------|--------|
| **ASUS** | 38.500.000đ | ~10 | 3.85M |
| **Lenovo** | 37.800.000đ | ~8 | 4.73M |
| **HP** | 17.500.000đ | ~5 | 3.50M |
| **Dell** | 17.500.000đ | ~5 | 3.50M |
| **MSI** | 14.700.000đ | ~4 | 3.68M |

**Insight**:
- **244 promotions có cash discount** từ 1,164 products (21%)
- **ASUS aggressive**: 38.5M total, ~3.85M per product
- **Lenovo competitive**: 37.8M total, average 4.73M/sp (cao nhất!)
- **Premium brands** (HP, Dell, MSI): 14-17.5M range

**Format detected**:
- TGDĐ: "Giảm ngay 700,000đ" (dấu phẩy)
- CellphoneS: "Giảm ngay 500K" (chữ K)

**Pattern cần thêm**:
```python
r'phiếu\s+mua\s+hàng\s+([\d\.]+)đ'  # "Phiếu mua hàng 500.000đ"
r'voucher\s+([\d\.]+)đ'              # "Voucher 1.000.000đ"
r'tặng.*?([\d\.]+)đ'                 # "Tặng 300.000đ"
```

---

## 📊 Tổng kết Business Insights

### **1. Phân khúc thị trường**
- **Cao cấp (>25M)**: 65.5% → Chiếm ưu thế
- **Trung cấp (15-25M)**: 24.6% → Sweet spot
- **Phổ thông (<15M)**: 9.9% → Ít cạnh tranh

### **2. Chiến lược giá**
- **Brands giữ giá tốt**: Apple (5-11% discount)
- **Brands aggressive**: Masstel (44.68%), LG (34.89%)
- **Brands ổn định**: Asus, Lenovo, Dell (7-11%)

### **3. Chiến lược khuyến mãi**
- **TGDĐ**: Nhiều KM (9.54/sp), bundle deals
- **CellphoneS**: Ít KM (3.99/sp), giá tốt từ đầu
- **Top tactics**: Quà tặng (22.1%) > Voucher (14.6%) > Giảm giá (12.7%)

### **4. Thương hiệu nổi bật**
- **Gaming segment**: Gigabyte, MSI, Gaming (>150M avg)
- **Value leaders**: Lenovo, Asus (90-130M avg)
- **Budget option**: LG, Masstel (<25M avg)

---

## 🗂️ Cấu trúc dữ liệu

### **Input Data**
```
data/raw/
├── tgdd_raw_data.csv           (414 products)
├── cellphones_raw_data.csv     (750 products)
├── tgdd_promotions_nosql.json  (414 promotion records)
└── cellphones_promotions_nosql.json (750 promotion records)
```

### **Output Results**
```
data/output_raw/
├── job01_avg_price_by_brand.txt
├── job02_discount_rate_by_brand.txt
├── job03_price_range_distribution.txt
├── job04_promotion_keyword_frequency.txt
├── job05_top5_highest_discounts.txt
├── job06_avg_promotions_per_store.txt
├── job07_popular_cpu_models.txt
├── job08_product_count_by_brand_store.txt
├── job09_office_license_count.txt
└── job10_cash_discount_by_brand.txt
```

---

## 🚀 Cách chạy từng job

### **Local Testing (Python)**
```bash
cd src/mapreduce/job01_avg_price_by_brand
python run_local.py
```

### **Hadoop Production**
```bash
# Upload data to HDFS
hdfs dfs -put data/raw/*.csv /raw_data/products_csv/
hdfs dfs -put data/raw/*_promotions_nosql.json /raw_data/promotions_json/

# Run MapReduce job
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/*.csv \
  -output /output/job01_avg_price_by_brand \
  -file mapper.py \
  -file reducer.py

# Download results
hdfs dfs -get /output/job01_avg_price_by_brand/part-00000 job01_output.txt
```

---

## 📋 Chi tiết từng Job

| Job | Input | Output Format | Hadoop Command |
|-----|-------|---------------|----------------|
| 01 | CSV | `brand \t avg_price` | Standard |
| 02 | CSV | `brand \t discount_percent` | Standard |
| 03 | CSV | `price_range \t count` | Standard |
| 04 | JSON | `keyword \t count` | Standard |
| 05 | CSV | `rank \t product \t discount \t price \t brand` | **Sort descending** |
| 06 | JSON | `store \t avg_promotions \t total_products` | Standard |
| 07 | CSV | `cpu_model \t count` | Thống kê CPU |
| 08 | CSV | `brand \t store \t count` | Brand & Store count |
| 09 | CSV | `category \t count` | TGDĐ only |
| 10 | JSON | `brand \t total_discount \t formatted` | Regex + JOIN |

**Lưu ý đặc biệt**:
- **Job 05**: Cần sort descending (`-k1,1nr`)
- **Job 07**: Extract CPU model từ cột `cpu` (Intel Core i5 → i5)
- **Job 08**: Đếm sản phẩm theo brand và store
- **Job 09**: Chỉ xử lý TGDĐ (có cột `software`)
- **Job 10**: JOIN JSON promotions với CSV products qua `product_id`

---

## 🔧 Technical Stack

- **Language**: Python 3
- **Framework**: Hadoop Streaming API
- **Data Format**: CSV (structured), JSON (semi-structured)
- **Encoding**: UTF-8 (Vietnamese support)
- **Pattern**: MapReduce with combiner optimization

### **Key Functions Used**
```python
# Price cleaning (handle both formats)
clean_price("22.990.000đ") → 22990000.0
clean_price("13190000.0")  → 13190000.0

# Brand extraction with aliases
extract_brand("Laptop Vivobook S15") → "Asus"
extract_brand("HP Pavilion 15")      → "HP"

# Encoding compatibility
io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
```

---

## 📈 Đề xuất cải tiến

### **Data Quality**
1. ✅ Normalize brand names (`Gaming` vs `gaming`, `Asus` vs `ASUS`)
2. ✅ Standardize CPU naming (`Intel Core i5` → `i5`)
3. ⚠️ Add `store` field to JSON for better tracking
4. ⚠️ Expand warranty info to separate field

### **Analysis Enhancement**
1. **Combiner optimization** cho Jobs 01, 02, 04, 06
2. **Fuzzy matching** cho specs comparison
3. **Time-series analysis** cho price trends

### **Performance**
1. Use combiner for aggregation jobs
2. Partitioner cho brand-based analysis
3. Compression (gzip) cho JSON files

---

## � Tổng kết Business Insights

### **1. Market Overview**
- **Total products**: 1,164 laptops (TGDĐ: 414, CellphoneS: 750)
- **Price range**: 3.59M (Masstel) → 172.6M (Gigabyte)
- **Avg discount**: 12.4% across all brands
- **Promotion intensity**: TGDĐ 9.54 vs CPS 3.99 promotions/product

### **2. Key Findings**

#### Pricing Strategy
- **Premium dominance**: 65.5% products >25M → Gaming/Workstation focus
- **Mid-range opportunity**: Only 24.6% in 15-25M sweet spot
- **Budget neglected**: 9.9% <15M → Untapped market

#### Brand Performance
1. **Volume leaders**: Lenovo (221), HP (164), Dell (147), MSI (139)
2. **ASUS hidden giant**: 155 products if case-normalized (#3 position)
3. **Apple exclusive**: CellphoneS only (83 total Apple products)
4. **Intel monopoly**: 100% top-20 CPUs are Intel

#### Discount Strategies
- **Aggressive**: Masstel (44.68%), LG (34.89%) → Exit/clearance
- **Conservative**: Dell (8.93%), Lenovo (7.18%) → Brand strength
- **Cash discount**: ASUS (38.5M), Lenovo (37.8M) lead investments

#### Promotion Tactics
- **TGDĐ bundle-heavy**: 9.54 KM/sp (quà tặng vật lý + voucher)
- **CellphoneS lean**: 3.99 KM/sp (giá tốt từ đầu)
- **Top keyword**: "Tặng" (22.1% of 16,464 promotions)

### **3. Data Quality Issues**
- ⚠️ **Case sensitivity**: ASUS/Asus, Gaming/gaming duplicates
- ⚠️ **Missing data**: 0 Office licenses, 0 extended warranties
- ⚠️ **Format inconsistency**: Price/CPU/discount formats vary
- ⚠️ **BOM issues**: `\ufeffid` in CSV headers

### **4. Recommendations**
**For Retailers**:
- Expand 15-25M mid-range segment (24.6% → target 35%)
- Normalize promotions (TGDĐ's 9.54 may overwhelm customers)
- Consider AMD laptops to break Intel monopoly

**For Data Team**:
- Implement case-insensitive brand normalization
- Rescrape for Office/warranty information
- Add store field to JSON for better tracking
- Standardize all format variations

---

## �👥 Team & Roles

- **Đỗ Kiến Hưng**: MapReduce Developer (10 Python jobs) ✅
- **Phan Trọng Phú/Quí**: Infrastructure, Scraping, ETL
- **Phạm Văn Thịnh**: Hive/Drill queries
- **Nguyễn Văn Quang Duy**: PySpark + Zeppelin visualization

---

## 📝 License & Usage

Dự án học tập - HCMUTE Big Data Course (BDES333877)  
Data source: TheGioiDiDong.com, CellphoneS.com.vn  
For educational purposes only.

---

**Last Updated**: October 15, 2025  
**Total Runtime**: ~2.4 seconds (10 jobs)  
**Status**: ✅ All 10 jobs completed successfully
