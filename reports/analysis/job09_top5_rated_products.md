# Job 09: Top 5 Sản Phẩm Được Đánh Giá Cao Nhất

## 📊 Mục đích phân tích
Tìm ra 5 laptop có điểm đánh giá trung bình cao nhất từ khách hàng trên TheGioiDiDong để hiểu sản phẩm nào được ưa chuộng nhất.

## 🔄 Luồng xử lý dữ liệu

### 1. Đọc dữ liệu
- **Input**: `data/raw/tgdd_raw_data.csv`
- **Cột quan trọng**: `average_rating`, `product_name`, `current_price`, `brand`

### 2. Xử lý dữ liệu
```python
# Chuyển đổi rating sang kiểu float
laptops_df = laptops_df.withColumn("average_rating", col("average_rating").cast("float"))

# Sắp xếp giảm dần theo rating và lấy 5 sản phẩm đầu
top5_laptops = laptops_df.orderBy(col("average_rating").desc()).limit(5)
```

### 3. Xuất kết quả
- **Output**: `data/processed_for_bi/job09_top5_rated_tgdd/`

## 📈 Kết quả phân tích

### Top 5 Laptop Rating Cao Nhất

| Thứ hạng | Sản phẩm | Rating | Giá hiện tại | Thương hiệu |
|----------|----------|---------|--------------|-------------|
| 1 | Acer Aspire Lite 15 AL15 71P 517D (i5 12450H, 16GB, 512GB) | 5.0⭐ | 14.49M | Acer |
| 2 | HP 15 fd0303TU (i3 1315U, 8GB, 512GB) | 5.0⭐ | 11.49M | HP |
| 3 | Asus Vivobook 15 X1504VA (i3 1315U, 8GB, 512GB) | 5.0⭐ | 11.29M | Asus |
| 4 | Acer Gaming Nitro V 15 (R5 6600H, 16GB, RTX 3050) | 5.0⭐ | 19.49M | Acer |
| 5 | Dell Inspiron 15 3530 (i5 1334U, 16GB, 512GB) | 5.0⭐ | 17.49M | Dell |

## 💡 Insight chính

### 1. **Tất cả đều đạt điểm tuyệt đối**
- Cả 5 laptop đều có rating **5.0/5.0** - mức đánh giá hoàn hảo
- Cho thấy chất lượng sản phẩm và dịch vụ xuất sắc

### 2. **Đa dạng phân khúc giá**
- **Phân khúc phổ thông** (11-15M): Acer Aspire, HP 15, Asus Vivobook - phù hợp học sinh, sinh viên
- **Phân khúc trung cao** (17-19M): Dell Inspiron, Acer Nitro - phục vụ gaming và công việc nặng

### 3. **Thương hiệu được tin dùng**
- **Acer** xuất hiện 2 lần (văn phòng + gaming)
- HP, Asus, Dell mỗi hãng có 1 đại diện
- Không có MacBook trong top 5 → Khách hàng đánh giá cao các thương hiệu Windows

### 4. **Cấu hình phổ biến**
- **CPU**: i3/i5 Intel Gen 13-14 hoặc Ryzen 5
- **RAM**: 8-16GB (đủ dùng cho đa số nhu cầu)
- **Ổ cứng**: 512GB SSD (chuẩn hiện nay)

### 5. **Gaming có giá trị tốt**
- Acer Nitro V 15 (19.49M) với RTX 3050 vẫn được đánh giá cao
- Tốc độ màn hình 165Hz là điểm cộng lớn

## 🎯 Kết luận

**Chiến lược kinh doanh:**
- Tập trung phát triển dòng sản phẩm phân khúc 11-15M (nhu cầu lớn nhất)
- Duy trì chất lượng laptop gaming Acer Nitro để cạnh tranh
- Học hỏi từ các model đạt 5.0 sao để cải thiện sản phẩm khác

**Cho người mua:**
- 5 laptop này là lựa chọn an toàn với đánh giá khách hàng tuyệt đối
- Nếu ngân sách dưới 12M → chọn HP/Asus
- Nếu cần gaming/làm việc nặng → Acer Nitro hoặc Dell Inspiron

---

*Dữ liệu từ: TheGioiDiDong.com | Xử lý: Apache Spark | Ngày: 2025*
