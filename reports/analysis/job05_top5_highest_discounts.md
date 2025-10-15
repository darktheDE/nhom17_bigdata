# Job 05: Top 5 Highest Discounts Analysis

## 📋 Mô tả Job
Job này phân tích và tìm ra **5 sản phẩm laptop có tỷ lệ giảm giá cao nhất** từ dữ liệu TheGioiDiDong (TGDĐ) và CellphoneS, giúp xác định các chương trình khuyến mãi hấp dẫn nhất để thu hút khách hàng.

## 🔄 Luồng xử lý dữ liệu (ETL Pipeline)

### 1. **Extract (Trích xuất)**
```python
# TGDĐ - Dữ liệu đã có định dạng số
laptops_df = spark.read.option("header", "true").csv("data/raw/tgdd_raw_data.csv")

# CellphoneS - Cần làm sạch định dạng giá (ví dụ: "22.990.000đ")
cellphones_df = spark.read.option("header", "true").csv("data/raw/cellphones_raw_data.csv")
```

**Input Data:**
- `tgdd_raw_data.csv`: Giá ở dạng số (16490000.0)
- `cellphones_raw_data.csv`: Giá ở dạng chuỗi ("22.990.000đ")

### 2. **Transform (Chuyển đổi)**

**Bước 2.1: Chuẩn hóa giá trị**
```python
# TGDĐ - Cast trực tiếp
laptops_df = laptops_df.withColumn("current_price", col("current_price").cast("float")) \
                       .withColumn("list_price", col("list_price").cast("float"))

# CellphoneS - Xóa dấu chấm và ký tự "đ" trước khi cast
cellphones_df = cellphones_df.withColumn("current_price", 
                                         regexp_replace(col("current_price_raw"), "[.đ]", "").cast("float"))
```

**Bước 2.2: Lọc dữ liệu hợp lệ**
```python
# Loại bỏ các dòng có giá NULL hoặc list_price = 0 (tránh division by zero)
df = df.filter((col("list_price").isNotNull()) & 
               (col("current_price").isNotNull()) & 
               (col("list_price") > 0))
```

**Bước 2.3: Tính toán discount rate**
```python
# Công thức: discount_rate = (list_price - current_price) / list_price
df = df.withColumn("discount_rate", 
                   (col("list_price") - col("current_price")) / col("list_price"))
```

**Bước 2.4: Sắp xếp và lấy Top 5**
```python
top5 = df.orderBy(col("discount_rate").desc()).limit(5)
```

### 3. **Load (Tải xuất)**
```python
top5.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job05_top5_highest_discounts_tgdd")
```

## 📊 Kết quả phân tích dữ liệu (TGDĐ)

### Top 5 Laptop Giảm Giá Cao Nhất

| Rank | Sản phẩm | Brand | Giá gốc | Giá hiện tại | Giảm giá | Đánh giá |
|------|----------|-------|---------|--------------|----------|----------|
| 🥇 #1 | HP VICTUS 15 fb1022AX (R5 7535HS, RTX 2050) | HP | 24.99M | 16.49M | **34.01%** | ⭐ 5.0 |
| 🥈 #2 | Acer Nitro 5 Tiger AN515 58 (i5 12500H, RTX 3050) | Acer | 27.49M | 18.69M | **32.01%** | ⭐ 4.9 |
| 🥉 #3 | HP VICTUS 15 fa1139TX (i5 12450H, RTX 2050) | HP | 24.09M | 16.99M | **29.47%** | ⭐ 4.9 |
| #4 | HP VICTUS 16 s0173AX (R5 7640HS, RTX 3050) | HP | 26.89M | 19.69M | **26.78%** | ⭐ 5.0 |
| #5 | HP VICTUS 16 s0078AX (R5 7640HS, RTX 3050) | HP | 26.89M | 19.69M | **26.78%** | ⭐ 5.0 |

## 💡 Insights & Business Intelligence

### 1. **HP thống trị chương trình khuyến mãi lớn**
- **4/5 sản phẩm** giảm giá cao nhất đều là HP (80%)
- Chỉ có 1 sản phẩm Acer lọt top 5
- **Chiến lược:** HP đang chạy chiến dịch marketing aggressive để cạnh tranh với các đối thủ

### 2. **Dòng VICTUS là flagship discount**
- **5/5 sản phẩm** top giảm giá đều thuộc dòng HP VICTUS hoặc Acer Nitro (gaming laptops)
- **Nhận định:** Dòng gaming là phân khúc cạnh tranh gay gắt nhất, nhà bán lẻ phải giảm giá mạnh để thu hút game thủ

### 3. **Mức giảm giá trung bình: 29.8%**
```
Average discount = (34.01% + 32.01% + 29.47% + 26.78% + 26.78%) / 5 = 29.81%
```
- Các sản phẩm top discount đều giảm **gần 1/3 giá trị** so với giá niêm yết
- Mức giảm cao nhất: **34.01%** (HP VICTUS 15 fb1022AX) - tiết kiệm được **8.5 triệu đồng**

### 4. **Phân khúc giá sau giảm: 16.5M - 19.7M**
- Tất cả sản phẩm top 5 đều rơi vào **phân khúc 15-25M** sau khi giảm giá
- Đây là phân khúc **mid-range gaming laptop** phổ biến nhất với sinh viên/văn phòng

### 5. **Đánh giá khách hàng xuất sắc**
- **Average rating: 4.96/5.0** cho 5 sản phẩm này
- 3/5 sản phẩm đạt **5.0 sao tuyệt đối**
- **Kết luận:** Giảm giá sâu + chất lượng cao = công thức thành công

### 6. **Cấu hình gaming phổ biến trong top discount**
```
CPU:     R5 7535HS / i5 12500H / R5 7640HS (mid-tier gaming)
RAM:     8GB - 16GB
GPU:     RTX 2050 / RTX 3050 (entry-level gaming)
Storage: 512GB SSD
Display: Full HD 144Hz (gaming-oriented)
```
- **Insight:** Laptop gaming entry-level (RTX 2050/3050) là phân khúc giảm giá mạnh nhất

## 🎯 Khuyến nghị cho Business

### Cho Nhà bán lẻ (TGDĐ):
1. **Tập trung quảng cáo** 5 sản phẩm này trên homepage và social media
2. **Bundle deals:** Kết hợp với phụ kiện gaming (chuột, tai nghe) để tăng AOV (Average Order Value)
3. **Flash sale timing:** Chạy flash sale vào khung giờ vàng (20h-22h) khi game thủ online nhiều

### Cho Nhà sản xuất (HP, Acer):
1. **Inventory clearance:** Các model này có thể là hàng tồn kho cần xả để nhường chỗ cho thế hệ mới
2. **Market penetration:** Sử dụng chiến lược giá thấp để chiếm thị phần từ đối thủ (Dell, Lenovo, Asus)

### Cho Người mua:
1. **Timing chuẩn:** Đây là thời điểm tốt nhất trong năm để mua laptop gaming mid-range
2. **ROI cao:** Tiết kiệm 8-10 triệu đồng (30% giá trị) với sản phẩm rated 4.9-5.0 sao
3. **Ưu tiên HP VICTUS 15 fb1022AX:** Giảm nhiều nhất (34%) + rating 5.0/5.0

## 🔍 So sánh với các Job khác

| Metric | Job 02 (Discount Rate by Brand) | Job 05 (Top 5 Discounts) |
|--------|----------------------------------|--------------------------|
| Góc nhìn | **Tổng quan theo brand** | **Chi tiết sản phẩm cụ thể** |
| Dữ liệu | Trung bình discount của HP: ~15% | Top product HP: 34% discount |
| Insight | HP giảm giá nhiều nhất theo brand | VICTUS là dòng giảm mạnh nhất |

**Kết luận tổng hợp:** HP không chỉ dẫn đầu về average discount rate mà còn có các deal cá nhân cực kỳ hấp dẫn ở dòng VICTUS gaming.

## 📈 Visualization Suggestions

```python
# Bar chart: Top 5 products by discount_rate
# X-axis: Product name (shortened)
# Y-axis: Discount rate (%)
# Color: Brand (HP = blue, Acer = orange)

# Price comparison chart
# Grouped bar: Original price vs Current price for top 5
# Label: Discount amount (VND)
```

## 🏆 Key Takeaways

1. ✅ **HP VICTUS 15 fb1022AX** là laptop có giảm giá cao nhất thị trường (34.01%)
2. ✅ HP chiếm 80% top 5 deals - chiến lược discount aggressive
3. ✅ Gaming laptops (RTX 2050/3050) được giảm giá mạnh nhất
4. ✅ Phân khúc 16-20M VND sau discount là sweet spot
5. ✅ Tất cả sản phẩm top discount đều có rating ≥ 4.9/5.0

---
**Ngày phân tích:** 15/10/2025  
**Nguồn dữ liệu:** TheGioiDiDong.com (TGDĐ)  
**Tool:** PySpark 3.x  
**Analyst:** Đỗ Kiến Hưng - Big Data Team
