# Job 11: Top 5 Thông Số Màn Hình Phổ Biến Nhất

## 📊 Mục Đích
Phân tích các kích thước và độ phân giải màn hình laptop phổ biến nhất tại TGDD và CellphoneS để hiểu xu hướng thị trường và nhu cầu người dùng.

## 🔄 Luồng Xử Lý Dữ Liệu

### 1. Nguồn Dữ Liệu
- **TGDD**: `tgdd_raw_data.csv` - có cột `screen_size` và `screen_resolution` riêng biệt
- **CellphoneS**: `cellphones_raw_data.csv` - cần trích xuất từ cột `raw_specs_string`

### 2. Các Bước Xử Lý

#### TGDD (Dữ liệu có sẵn)
```python
1. Đọc CSV với header
2. GroupBy (screen_size, screen_resolution)
3. Đếm số lượng sản phẩm: COUNT(*)
4. Sắp xếp giảm dần theo product_count
5. Lấy Top 5
```

#### CellphoneS (Trích xuất bằng Regex)
```python
1. Đọc CSV với header
2. Trích xuất screen_size từ raw_specs_string:
   - Pattern: r"(\d+\.\d+)" → Lấy số thập phân (VD: 15.6, 14.0)
3. Trích xuất screen_resolution:
   - Pattern: r"(FHD|WUXGA|QHD|UHD|OLED|Full HD|4K|\d+\s*[xX]\s*\d+)"
   - Tìm các từ khóa độ phân giải phổ biến
4. GroupBy (screen_size, screen_resolution)
5. Đếm số lượng: COUNT(*)
6. Sắp xếp giảm dần → Top 5
```

## 💡 Insights Từ Dữ Liệu

### Top 5 Thông Số Màn Hình

#### Thế Giới Di Động
| Hạng | Kích Thước | Độ Phân Giải | Số Sản Phẩm | % |
|------|------------|--------------|-------------|---|
| 1 | N/A | Full HD | 209 | 53.9% |
| 2 | N/A | WUXGA | 87 | 22.4% |
| 3 | N/A | N/A | 41 | 10.6% |
| 4 | N/A | 2.8K | 40 | 10.3% |
| 5 | N/A | QHD | 12 | 3.1% |

**Tổng**: 389 sản phẩm trong Top 5

#### CellphoneS
| Hạng | Kích Thước | Độ Phân Giải | Số Sản Phẩm | % |
|------|------------|--------------|-------------|---|
| 1 | 15.6" | FHD | 200 | 38.0% |
| 2 | (rỗng) | (rỗng) | 161 | 30.6% |
| 3 | 14.0" | FHD | 65 | 12.4% |
| 4 | 14.0" | WUXGA | 51 | 9.7% |
| 5 | 14.0" | OLED | 45 | 8.6% |

**Tổng**: 522 sản phẩm (161 dòng thiếu data)

## 🔍 Phân Tích Chi Tiết

### 1. Độ Phân Giải Thống Trị
- **Full HD (FHD) là vua**: 
  - TGDD: 209 sản phẩm (53.9%)
  - CellphoneS: 200+65 = 265 sản phẩm FHD (50.8%)
  - ✅ Tỷ lệ giá/chất lượng tốt nhất, phù hợp đại đa số người dùng

- **WUXGA - phân giải làm việc**:
  - TGDD: 87 sp (22.4%)
  - CellphoneS: 51 sp (9.7%)
  - ✅ Phổ biến ở laptop văn phòng (1920x1200, tỷ lệ 16:10)

- **2.8K/QHD - cao cấp**:
  - TGDD: 40+12 = 52 sp (13.4%)
  - ✅ Phân khúc premium, đồ họa/sáng tạo nội dung

- **OLED - công nghệ mới**:
  - CellphoneS: 45 sp (8.6%)
  - ✅ Màu sắc đẹp, tiết kiệm pin, đang tăng trưởng

### 2. Kích Thước Màn Hình Phổ Biến

#### CellphoneS (có data kích thước)
- **15.6 inch - chuẩn phổ thông**:
  - 200 sản phẩm (38%)
  - ✅ Kích thước vừa vặn, phù hợp văn phòng/đa năng
  - ✅ Cân bằng giữa di động và diện tích làm việc

- **14.0 inch - laptop mỏng nhẹ**:
  - 65 (FHD) + 51 (WUXGA) + 45 (OLED) = 161 sp (30.8%)
  - ✅ Xu hướng tăng trưởng mạnh
  - ✅ Phù hợp di chuyển nhiều (sinh viên, doanh nhân)

#### TGDD (vấn đề data)
- ⚠️ **100% sản phẩm có screen_size = "N/A"**
- Nguyên nhân:
  - Cột `screen_size` không được populate từ scraping
  - Hoặc data bị lỗi khi import

### 3. So Sánh 2 Cửa Hàng

| Tiêu Chí | TGDD | CellphoneS |
|----------|------|------------|
| **Data Quality** | ⚠️ Thiếu screen_size | ✅ Đầy đủ (70% có data) |
| **Độ phân giải chủ đạo** | Full HD (54%) | FHD 15.6" (38%) |
| **Đa dạng** | 4 loại chính | 2 size × 3 độ phân giải |
| **Dòng lỗi** | 41 sp (10.6%) | 161 sp (30.6%) |

### 4. Xu Hướng Thị Trường

#### ✅ Phân Khúc Chủ Lực
1. **Laptop phổ thông**: 15.6" Full HD (~200 sp)
   - Giá tầm trung
   - Đa năng (văn phòng, học tập, giải trí)

2. **Laptop di động**: 14.0" FHD/WUXGA (~116 sp)
   - Mỏng nhẹ
   - Pin tốt
   - Phù hợp di chuyển

#### 📈 Xu Hướng Tăng Trưởng
- **OLED**: 45 sp (8.6%) - công nghệ mới, màu sắc đẹp
- **2.8K**: 40 sp (10.3%) - độ phân giải cao, content creator
- **14 inch**: Thay thế dần 15.6" ở phân khúc cao cấp

#### 📉 Xu Hướng Giảm
- **13.3 inch**: Không xuất hiện trong Top 5 (quá nhỏ)
- **17 inch**: Không xuất hiện (quá nặng, ít di động)

## ⚠️ Vấn Đề Data Quality

### TGDD
- **Lỗi nghiêm trọng**: 100% screen_size = "N/A"
- **Nguyên nhân**:
  ```python
  # Scraper có thể không lấy được field này
  # Hoặc cột bị mapping sai
  ```
- **Ảnh hưởng**: Không phân tích được xu hướng kích thước

### CellphoneS
- **30.6% dữ liệu rỗng** (161/522 sản phẩm)
- **Regex không match**:
  - raw_specs_string format khác thường
  - Hoặc thiếu thông tin màn hình
- **Ví dụ lỗi**:
  ```
  "Intel Core i5/8GB/256GB SSD/Windows 11"
  → Thiếu thông tin màn hình
  ```

## 🔧 Đề Xuất Cải Tiến

### 1. Fix TGDD Data
```python
# Option 1: Re-scrape với selector đúng cho screen_size
# Option 2: Extract từ product_name nếu có (VD: "Laptop HP 15.6 inch...")
cellphones_df = cellphones_df.withColumn("screen_size", 
    regexp_extract(col("product_name"), r"(\d+\.\d+)", 1)
)
```

### 2. Cải Thiện Regex CellphoneS
```python
# Thêm pattern phổ biến hơn
screen_patterns = r"(\d+\.?\d*)\s*inch|(\d+\.?\d*)\s*\"|(\d+\.?\d*)'"
resolution_patterns = r"(FHD|WUXGA|QHD|UHD|OLED|IPS|TN|VA|Retina|2K|4K)"
```

### 3. Thêm Metrics
```python
# Thống kê kèm tỷ lệ màn hình
SELECT screen_size, aspect_ratio, resolution, 
       COUNT(*) as count,
       AVG(price) as avg_price
GROUP BY screen_size, aspect_ratio, resolution
```

### 4. Phân Loại Rõ Ràng
- **Portable**: 13-14 inch
- **Standard**: 15-16 inch  
- **Desktop Replacement**: 17+ inch

## 📈 Ứng Dụng Thực Tế

### Cho Khách Hàng
- **Văn phòng/Đa năng**: Chọn 15.6" FHD (nhiều lựa chọn, giá tốt)
- **Di động**: Chọn 14.0" FHD/WUXGA (nhẹ, pin tốt)
- **Đồ họa/Video**: Chọn 14-16" OLED/2.8K (màu đẹp, độ phân giải cao)

### Cho Cửa Hàng
- **Tập trung kho**: 15.6" FHD (38% thị trường)
- **Tăng cường**: 14.0" các loại (30% và đang tăng)
- **Giảm tồn**: Các size lẻ không phổ biến

### Cho Nhà Sản Xuất
- **Đầu tư R&D**: OLED, 2.8K, tỷ lệ 16:10
- **Tăng sản xuất**: 14" segment (xu hướng mỏng nhẹ)
- **Giảm dần**: 15.6" TN panel thấp cấp

## 🎯 Kết Luận

1. **Full HD 1920×1080 vẫn là vua** (50%+ thị trường)
2. **15.6 inch và 14.0 inch chiếm 70%** laptop
3. **OLED và 2.8K đang lên** (công nghệ mới, giá cao)
4. **Cần fix data TGDD** để phân tích chính xác hơn
