# 📊 ỨNG DỤNG HADOOP THỰC HIỆN XÂY DỰNG HỆ THỐNG PHÂN TÍCH CẠNH TRANH THỊ TRƯỜNG DỰA TRÊN DỮ LIỆU GIÁ VÀ KHUYẾN MÃI SẢN PHẨM LAPTOP

## 🎯 Giới Thiệu Dự Án

**Đề tài:** Ứng dụng Hadoop thực hiện xây dựng hệ thống phân tích cạnh tranh thị trường dựa trên dữ liệu giá và khuyến mãi sản phẩm Laptop từ hai trang web: [www.thegioididong.com](http://www.thegioididong.com) và [www.cellphones.com.vn](http://www.cellphones.com.vn).

### 🎯 Mục tiêu chính

Xây dựng một hệ thống Big Data hoàn chỉnh có khả năng:
- **Thu thập, lưu trữ, và xử lý** dữ liệu về giá và các chương trình khuyến mãi của sản phẩm laptop từ hai nhà bán lẻ lớn
- **Phân tích dữ liệu** để cung cấp cái nhìn sâu sắc về chiến lược cạnh tranh trên thị trường
- **Cung cấp giao diện trực quan** để người dùng có thể thực hiện truy vấn và xem kết quả phân tích

### 👥 Đối tượng hướng đến
- **Người tiêu dùng:** Dễ dàng tìm kiếm và so sánh để chọn được sản phẩm có giá và ưu đãi tốt nhất
- **Doanh nghiệp:** Theo dõi, phân tích chiến lược của đối thủ để đưa ra các quyết định kinh doanh hiệu quả

## 👥 Thành Viên Nhóm

| Họ Tên | Vai Trò | Nhiệm Vụ Chính |
|--------|---------|----------------|
| Phan Trọng Phú | Team Hạ tầng & Dữ liệu | Thiết lập môi trường Hadoop, cấu hình hệ thống |
| Phan Trọng Quí | Team Hạ tầng & Dữ liệu | Web Scraping, Làm sạch dữ liệu, ETL Pipeline |
| Đỗ Kiến Hưng | Big Data Developer | Lập trình 10 chương trình MapReduce (Python) |
| Phạm Văn Thịnh | Data Analyst | Phân tích dữ liệu với Hive/HiveQL và Apache Drill |
| Nguyễn Văn Quang Duy | BI Developer | Trực quan hóa với Apache Zeppelin và PySpark |

## 🛠️ Công Nghệ Sử Dụng

### Hệ sinh thái Hadoop & Big Data
- **Lưu trữ phân tán:** Hadoop HDFS, YARN
- **Xử lý dữ liệu:** Apache Hadoop MapReduce
- **ETL & Transformation:** Apache Pig, Apache Sqoop
- **Truy vấn dữ liệu:** Apache Hive (HiveQL), Apache Drill, Apache Phoenix
- **Cơ sở dữ liệu:** HBase (NoSQL), MySQL (RDBMS)
- **Phân tích & Tương tác:** Apache Spark (PySpark), Apache Zeppelin
- **Điều phối:** Apache Zookeeper

### Môi trường phát triển
- **Hệ điều hành:** Ubuntu trên WSL 2
- **Ngôn ngữ lập trình:** Python (Web Scraping, PySpark), Java (MapReduce)
- **Quản lý mã nguồn:** GitHub


## 📁 Cấu Trúc Dự Án

```
nhom17_bigdata/
├── data/
│   ├── raw/                           # Dữ liệu thô từ web scraping
│   │   ├── cellphones_raw_data.csv    # Dữ liệu sản phẩm CellphoneS
│   │   ├── cellphones_promotions_nosql.json  # Khuyến mãi CellphoneS
│   │   ├── tgdd_raw_data.csv          # Dữ liệu sản phẩm TGDĐ
│   │   └── tgdd_promotions_nosql.json # Khuyến mãi TGDĐ
│   ├── sample/                        # Dữ liệu mẫu
│   └── processed_for_bi/              # Dữ liệu đã xử lý cho BI
├── docs/                              # Tài liệu dự án
│   ├── ABOUT_PROJECT.md               # Tổng quan dự án
│   ├── ABOUT_DATA.md                  # Mô tả chi tiết dữ liệu
│   └── ABOUT_PERSONAL_ROLE.md         # Phân công nhiệm vụ
├── reports/                           # Báo cáo, slide, video demo
│   └── video/
├── src/
│   ├── scraping/                      # Script thu thập dữ liệu
│   │   ├── tgdd_scraper.py
│   │   ├── cellphones_scraper.py
│   │   └── sql_config.sql
│   ├── mapreduce/                     # 10 MapReduce jobs (Python)
│   └── hive/                          # HiveQL scripts
└── README.md
```

## 📊 Dữ Liệu Dự Án

### Nguồn dữ liệu
- **Thế Giới Di Động:** [www.thegioididong.com](https://www.thegioididong.com)
- **CellphoneS:** [www.cellphones.com.vn](https://cellphones.com.vn)
- **Phương pháp:** Web Crawling (tự động)
- **Quy mô:** Khoảng **1,200 sản phẩm laptop**

### Cấu trúc dữ liệu

#### 1. Dữ liệu có cấu trúc (CSV) - Thông tin sản phẩm
- `id`: Mã định danh duy nhất
- `product_name`: Tên sản phẩm
- `current_price_raw`: Giá bán hiện tại
- `list_price_raw`: Giá niêm yết
- `raw_specs_string`: Chuỗi mô tả cấu hình
- `product_url`: URL sản phẩm

**Đặc điểm:**
- **CellphoneS:** Giá dạng chuỗi ("22.990.000đ") - cần làm sạch
- **TGDĐ:** Giá dạng số (13190000.0) - sẵn sàng xử lý

#### 2. Dữ liệu phi cấu trúc (JSON) - Thông tin khuyến mãi
```json
{
  "product_id": "xxx",
  "product_url": "...",
  "promotions": [
    "Trả góp 0% lãi suất",
    "Tặng Balo",
    "Giảm ngay 700,000đ"
  ]
}
```

**Đặc điểm:** Văn bản tự do, cần xử lý NLP để phân loại

## 🔄 Kiến Trúc Hệ Thống và Luồng Xử Lý ETL

### Pipeline xử lý dữ liệu

```
┌─────────────────┐
│  Web Scraping   │ ──> Python Scripts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Raw Data      │ ──> CSV + JSON Files
│   (Local)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   HDFS          │ ──> Hadoop Distributed File System
│ /raw_data/      │     - /products_csv/
└────────┬────────┘     - /promotions_json/
         │
         ▼
┌─────────────────┐
│  Apache Pig     │ ──> ETL & Data Transformation
│  (ETL Layer)    │     - Làm sạch dữ liệu CellphoneS
└────────┬────────┘     - Chuẩn hóa schema
         │              - Hợp nhất (UNION) dữ liệu
         ▼
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐  ┌───────┐
│ MySQL │  │ HBase │ ──> Data Warehouses
│(RDBMS)│  │(NoSQL)│     - MySQL: Dữ liệu có cấu trúc
└───┬───┘  └───┬───┘     - HBase: Dữ liệu phi cấu trúc
    │          │
    └────┬─────┘
         ▼
┌─────────────────┐
│  Analysis       │ ──> MapReduce, Hive, Drill, Spark
│  Layer          │     - 10 MapReduce Jobs
└────────┬────────┘     - HiveQL Queries
         │              - PySpark Analytics
         ▼
┌─────────────────┐
│ Visualization   │ ──> Apache Zeppelin
│ & Reporting     │     - Interactive Notebooks
└─────────────────┘     - Charts & Dashboards
```

### Chi tiết từng bước

**Bước 1: Ingestion (Thu thập và Lưu trữ)**
- Đưa 4 file dữ liệu thô lên **HDFS**
- Phân loại vào thư mục `/raw_data/products_csv` và `/raw_data/promotions_json`

**Bước 2: Transformation (Xử lý và Làm sạch)**
- **Apache Pig** thực hiện:
  - Làm sạch giá CellphoneS: "22.990.000đ" → 22990000
  - Thêm cột `source_brand` (cellphones/tgdd)
  - UNION dữ liệu từ 2 nguồn
  - Chuẩn hóa dữ liệu JSON khuyến mãi

**Bước 3: Loading (Lưu vào Kho dữ liệu)**
- **Apache Sqoop:** Import dữ liệu có cấu trúc từ HDFS → MySQL
- **HBase:** Lưu trữ dữ liệu khuyến mãi (NoSQL) cho truy xuất nhanh

**Bước 4: Analysis (Phân tích)**
- **MapReduce (Java/Python):** Các phân tích phức tạp
- **Apache Hive:** Truy vấn SQL-like trên HDFS
- **Apache Drill:** Truy vấn đa nguồn (MySQL + HBase)
- **Apache Spark (PySpark):** Phân tích tương tác

**Bước 5: Presentation (Trực quan hóa)**
- **Apache Zeppelin:** Notebook tương tác
- **GUI Web:** Giao diện người dùng cuối




## 🚀 Hướng Dẫn Chạy Dự Án

### Bước 1: Thu thập dữ liệu (Web Scraping)
```bash
cd src/scraping
python tgdd_scraper.py
python cellphones_scraper.py
```

### Bước 2: Đưa dữ liệu lên HDFS (Ingestion)
```bash
# Tạo cấu trúc thư mục trên HDFS
hdfs dfs -mkdir -p /raw_data/products_csv
hdfs dfs -mkdir -p /raw_data/promotions_json

# Upload dữ liệu sản phẩm (CSV)
hdfs dfs -put data/raw/cellphones_raw_data.csv /raw_data/products_csv/
hdfs dfs -put data/raw/tgdd_raw_data.csv /raw_data/products_csv/

# Upload dữ liệu khuyến mãi (JSON)
hdfs dfs -put data/raw/cellphones_promotions_nosql.json /raw_data/promotions_json/
hdfs dfs -put data/raw/tgdd_promotions_nosql.json /raw_data/promotions_json/
```

### Bước 3: Xử lý dữ liệu với Apache Pig (ETL)
```bash
# Chạy Pig script để làm sạch và hợp nhất dữ liệu
pig -x mapreduce src/pig/mysql_brand_etl.pig

# Pig sẽ thực hiện:
# - Làm sạch giá CellphoneS
# - Thêm cột source_brand
# - UNION dữ liệu từ 2 nguồn
# - Lưu vào thư mục tạm trên HDFS
```

### Bước 4: Import vào MySQL với Sqoop
```bash
# Import dữ liệu đã xử lý từ HDFS vào MySQL
sqoop import \
  --connect jdbc:mysql://localhost:3306/bigdata_db \
  --username root \
  --password your_password \
  --table products \
  --target-dir /processed_data/products \
  --m 1
```

### Bước 5: Lưu dữ liệu JSON vào HBase
```bash
# Khởi động HBase shell
hbase shell

# Tạo bảng
create 'promotions', 'promo_details'

# Import dữ liệu (sử dụng script Python hoặc Pig)
pig -x mapreduce src/pig/hbase_promotions_import.pig
```

### Bước 6: Chạy MapReduce Jobs (Python Streaming)
```bash
# Job 01: Tính giá bán trung bình theo hãng
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/* \
  -output /output/job01_avg_price_by_brand \
  -file src/mapreduce/job01_avg_price/mapper.py \
  -file src/mapreduce/job01_avg_price/reducer.py

# Job 02: Tính tỷ lệ giảm giá trung bình
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/* \
  -output /output/job02_avg_discount \
  -file src/mapreduce/job02_avg_discount/mapper.py \
  -file src/mapreduce/job02_avg_discount/reducer.py

# Tương tự cho 8 jobs còn lại...
```

### Bước 7: Phân tích với Hive
```bash
# Khởi động Hive
hive

# Tạo bảng từ dữ liệu trên HDFS
CREATE EXTERNAL TABLE products (
  id STRING,
  product_name STRING,
  current_price DOUBLE,
  list_price DOUBLE,
  specs STRING,
  url STRING,
  source_brand STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/processed_data/products';

# Chạy các truy vấn phân tích
SELECT source_brand, AVG(current_price) as avg_price
FROM products
GROUP BY source_brand;
```

### Bước 8: Phân tích với Apache Drill
```bash
# Khởi động Drill
drill-embedded

# Truy vấn kết hợp MySQL và HBase
SELECT p.product_name, p.current_price, h.promotions
FROM mysql.bigdata_db.products p
JOIN hbase.promotions h
ON p.id = h.product_id
WHERE p.current_price < 20000000;
```

### Bước 9: Phân tích tương tác với Zeppelin
1. Mở trình duyệt và truy cập: `http://localhost:8080`
2. Tạo notebook mới
3. Sử dụng PySpark để phân tích:

```python
# Đọc dữ liệu từ HDFS
df = spark.read.csv("/processed_data/products", header=True, inferSchema=True)

# Phân tích
df.groupBy("source_brand").agg({"current_price": "avg"}).show()

# Trực quan hóa
%sql
SELECT source_brand, AVG(current_price) as avg_price
FROM products
GROUP BY source_brand
```
---

## 🎯 Các Phân Tích Chính với Hive/Drill

### Phân tích thị trường
- Thị phần theo thương hiệu (HP, Dell, Asus, Lenovo, Acer, MacBook)
- Chiến lược giá và khuyến mãi theo từng nhà bán lẻ
- Xu hướng cấu hình phổ biến (RAM, Storage, CPU)

### Phân tích sản phẩm
- Phân khúc sản phẩm theo màn hình và độ phân giải
- Phân bố hệ điều hành (Windows 11, macOS)
- Mối tương quan giá - cấu hình

### So sánh cạnh tranh
- So sánh giá cùng sản phẩm giữa 2 nguồn
- Chiến lược khuyến mãi TGDĐ vs CellphoneS
- Phân tích gap về giá và dịch vụ

## 📈 Kết Quả Mong Đợi

### Cho người tiêu dùng
- ✅ Tìm kiếm sản phẩm có giá tốt nhất
- ✅ So sánh khuyến mãi giữa các cửa hàng
- ✅ Xác định thời điểm mua hàng tối ưu

### Cho doanh nghiệp
- ✅ Giám sát chiến lược giá của đối thủ
- ✅ Phân tích xu hướng thị trường
- ✅ Đưa ra quyết định kinh doanh dựa trên dữ liệu

## 🤝 Đóng Góp

Dự án này được phát triển bởi Nhóm 17 - Môn Big Data (BDES333877)
- **Trường:** Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE)
- **Học kỳ:** HK5 (2024-2025)

## 📧 Liên Hệ

Nếu có bất kỳ câu hỏi nào, vui lòng liên hệ qua:
- **Repository:** [darktheDE/nhom17_bigdata](https://github.com/darktheDE/nhom17_bigdata)
---

**© 2025 Nhóm 17 - Big Data Analytics Project**


## 📹 Video Demo

Link video demo: [Xem tại đây](reports/video/link_demo.txt)

## 📄 License

Dự án này được phát triển cho môn học Nhập môn Dữ Liệu Lớn - HCMUTE.

---
**Lưu ý:** File dữ liệu lớn không được commit lên GitHub. Chỉ file mẫu `laptops_sample.csv` được đưa vào repository.
