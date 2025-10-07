# 📊 Dự Án Phân Tích Big Data - Thị Trường Laptop

## 🎯 Giới Thiệu Dự Án
**Đề tài:** Ứng dụng hệ sinh thái Hadoop để phân tích dữ liệu bán laptop từ các sàn thương mại điện tử lớn tại Việt Nam (thegioididong.com và cellphones.com.vn).

Dự án này phân tích hơn 1000 sản phẩm laptop để rút ra các insights về:
- Thị phần thương hiệu (HP, Dell, Asus, Lenovo, Acer, MacBook)
- Chiến lược giá và khuyến mãi
- Xu hướng cấu hình (RAM, Storage, CPU)
- Phân khúc sản phẩm theo màn hình và độ phân giải
- Mối tương quan giá - đánh giá - cấu hình

## 👥 Thành Viên Nhóm

| Họ Tên | Vai Trò | Nhiệm Vụ Chính |
|--------|---------|----------------|
| Phan Trọng Phú | Team Hạ tầng & Dữ liệu | Thiết lập môi trường dùng CentOS |
| Phan Trọng Quí | Team Hạ tầng & Dữ liệu | Web Scraping, Làm sạch dữ liệu, Đẩy dữ liệu lên HDFS |
| Đỗ Kiến Hưng | Big Data Developer | Xử lý dữ liệu với MapReduce (10 jobs) |
| Phạm Văn Thịnh | Data Analyst | Phân tích dữ liệu với Hive/HiveQL |
| Nguyễn Văn Quang Duy | BI Developer | Trực quan hóa với Power BI & Grafana |

## 🛠️ Công Nghệ Sử Dụng

- **Lưu trữ phân tán:** Hadoop HDFS
- **Xử lý dữ liệu:** Apache Hadoop MapReduce (Python)
- **Truy vấn dữ liệu:** Apache Hive (HiveQL)
- **Trực quan hóa:** Microsoft Power BI
- **Giám sát:** Grafana
- **Hệ điều hành:** CentOS
- **Quản lý mã nguồn:** GitHub

## 📁 Cấu Trúc Dự Án

```
nhom17-bigdata-analytics/
├── data/
│   ├── raw/                    # Dữ liệu thô từ web scraping
│   └── processed_for_bi/       # Dữ liệu đã xử lý cho Power BI
├── docs/                       # Tài liệu dự án
├── reports/                    # Báo cáo, slide, video demo
├── src/
│   ├── scraping/              # Script cào dữ liệu
│   ├── mapreduce/             # 10 MapReduce jobs
│   └── hive/                  # HiveQL scripts
└── README.md
```

## 🚀 Hướng Dẫn Chạy Dự Án

### 1. Thu Thập Dữ Liệu (Web Scraping)
```bash
cd src/scraping
python tgdd_scraper.py
python cellphones_scraper.py
```

### 2. Upload Dữ Liệu Lên HDFS
```bash
# Tạo thư mục trên HDFS
hdfs dfs -mkdir -p /user/bigdata/laptops/raw

# Upload file dữ liệu
hdfs dfs -put data/raw/laptops.csv /user/bigdata/laptops/raw/
```

### 3. Chạy MapReduce Jobs
```bash
# Ví dụ: Job 01 - Đếm số lượng sản phẩm theo thương hiệu
hadoop jar /path/to/hadoop-streaming.jar \
  -mapper "python mapper.py" \
  -reducer "python reducer.py" \
  -input /user/bigdata/laptops/raw/laptops.csv \
  -output /user/bigdata/laptops/output/job01_brand_count \
  -file src/mapreduce/job01_brand_count/mapper.py \
  -file src/mapreduce/job01_brand_count/reducer.py
```

### 4. Phân Tích Với Hive
```bash
# Khởi động Hive
hive

# Chạy các script HiveQL
source src/hive/01_create_tables.hql;
source src/hive/02_brand_analysis.hql;
```

### 5. Trực Quan Hóa Với Power BI
- Mở Power BI Desktop
- Import các file CSV từ `data/processed_for_bi/`
- Tạo dashboard theo thiết kế

## 📊 Danh Sách 10 MapReduce Jobs

1. **job01_brand_count** - Đếm số lượng sản phẩm theo thương hiệu
2. **job02_word_count** - Phân tích từ khóa trong tên sản phẩm
3. **job03_price_range_analysis** - Phân tích phân khúc giá
4. **job04_ram_rom_distribution** - Phân bố RAM và ROM
5. **job05_rating_by_brand** - Đánh giá trung bình theo thương hiệu
6. **job06_discount_analysis** - Phân tích chương trình khuyến mãi
7. **job07_cpu_analysis** - Phân tích loại CPU phổ biến
8. **job08_screen_size_analysis** - Phân tích kích thước màn hình
9. **job09_os_distribution** - Phân bố hệ điều hành
10. **job10_price_rating_correlation** - Tương quan giá và đánh giá

## 📝 Tài Liệu Tham Khảo

- [Data Dictionary](docs/data_dictionary.md) - Giải thích chi tiết các thuộc tính dữ liệu
- [Setup Guide](docs/setup_guide.md) - Hướng dẫn cài đặt môi trường chi tiết

## 📹 Video Demo

Link video demo: [Xem tại đây](reports/video/link_demo.txt)

## 📄 License

Dự án này được phát triển cho môn học Big Data Analytics - HCMUTE.

---
**Lưu ý:** File dữ liệu lớn không được commit lên GitHub. Chỉ file mẫu `laptops_sample.csv` được đưa vào repository.
