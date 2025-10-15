# Job 10: Phân Tích Phân Bố RAM và Storage

## 1. Mục Đích
Phân tích cấu hình RAM và dung lượng lưu trữ phổ biến của laptop trên thị trường từ 2 nguồn dữ liệu: TheGioiDiDong và CellphoneS.

## 2. Luồng Xử Lý

### 2.1. Xử Lý Dữ Liệu TGDĐ
```
Input: tgdd_raw_data.csv (cột ram, storage)
→ Chuẩn hóa: Loại bỏ ký tự "GB", chuyển sang số nguyên
→ Group by (ram_clean, storage_clean)
→ Đếm số lượng sản phẩm
→ Sắp xếp giảm dần theo product_count
→ Output: job10_ram_storage_tgdd/
```

### 2.2. Xử Lý Dữ Liệu CellphoneS
```
Input: cellphones_raw_data.csv (cột raw_specs_string)
→ Dùng regex trích xuất RAM và Storage từ chuỗi specs
→ Chuyển đổi TB sang GB (nhân 1024)
→ Group by (ram_clean, storage_clean)
→ Đếm số lượng sản phẩm
→ Sắp xếp giảm dần theo product_count
→ Output: job10_ram_storage_cellphones/
```

## 3. Phân Tích Kết Quả

### 3.1. TheGioiDiDong (412 sản phẩm)
**Top 5 cấu hình phổ biến:**
1. **16GB RAM + 512GB SSD**: 244 sản phẩm (59.2%) - **Cấu hình thống trị**
2. **32GB RAM + 1TB SSD**: 46 sản phẩm (11.2%)
3. **16GB RAM + 1TB SSD**: 41 sản phẩm (10.0%)
4. **8GB RAM + 512GB SSD**: 26 sản phẩm (6.3%)
5. **32GB RAM + 512GB SSD**: 16 sản phẩm (3.9%)

**Xu hướng:**
- **16GB RAM** là chuẩn phổ biến nhất (chiếm gần 60%)
- **512GB SSD** là dung lượng lưu trữ được ưa chuộng
- Laptop cao cấp (32GB+) chiếm khoảng 15% thị trường
- 4 sản phẩm thiếu thông tin cấu hình

### 3.2. CellphoneS (746 sản phẩm)
**Top 5 cấu hình phổ biến:**
1. **16GB RAM + 512GB SSD**: 296 sản phẩm (39.7%)
2. **Thiếu thông tin**: 163 sản phẩm (21.8%) - **Vấn đề dữ liệu**
3. **32GB RAM + 1TB SSD**: 78 sản phẩm (10.5%)
4. **8GB RAM + 512GB SSD**: 63 sản phẩm (8.4%)
5. **16GB RAM + 1TB SSD**: 54 sản phẩm (7.2%)

**Xu hướng:**
- **163 sản phẩm thiếu specs** (21.8%) - chất lượng dữ liệu kém hơn TGDĐ
- Cấu hình 16GB+512GB vẫn phổ biến nhất nhưng tỷ lệ thấp hơn (39.7% vs 59.2%)
- Phân bố cấu hình đa dạng hơn (28 tổ hợp khác nhau vs 20 tổ hợp của TGDĐ)
- Xuất hiện cấu hình RAM cao: 64GB, 128GB (cho workstation)

## 4. Insight Kinh Doanh

### 4.1. Cấu Hình Phổ Thông
- **16GB RAM + 512GB SSD** là tiêu chuẩn thị trường 2024-2025
- Phù hợp văn phòng, đa nhiệm nhẹ, sinh viên
- Chiếm 40-60% tổng sản phẩm

### 4.2. Phân Khúc Cao Cấp
- **32GB RAM + 1TB SSD** đang lên ngôi (10-11% thị trường)
- Nhu cầu cho content creator, lập trình viên
- TGDĐ và CellphoneS đều tập trung vào phân khúc này

### 4.3. Phân Khúc Giá Rẻ
- **8GB RAM + 512GB/256GB** vẫn tồn tại (6-8%)
- Phục vụ học sinh, người dùng cơ bản
- Xu hướng giảm dần theo thời gian

### 4.4. Chất Lượng Dữ Liệu
- **TGDĐ**: Chỉ 1% sản phẩm thiếu specs → Dữ liệu đầy đủ
- **CellphoneS**: 21.8% thiếu specs → Cần cải thiện crawling logic
- Regex extraction từ `raw_specs_string` không hiệu quả 100%

## 5. Khuyến Nghị

### 5.1. Cho Nhà Bán Lẻ
- Tập trung tồn kho vào cấu hình **16GB+512GB** (60% inventory)
- Đầu tư vào phân khúc 32GB cho khách chuyên nghiệp
- Loại bỏ dần sản phẩm 8GB RAM (xu hướng giảm)

### 5.2. Cho Nhà Sản Xuất
- Sản xuất nhiều biến thể **16GB+512GB** với giá cạnh tranh
- Phát triển dòng 32GB+1TB cho creator/developer
- Nâng cấp miễn phí RAM/SSD để tăng giá trị sản phẩm

### 5.3. Cải Thiện Hệ Thống
- **Fix scraper CellphoneS**: 21.8% missing data là quá cao
- Thêm validation cho specs extraction
- Chuẩn hóa format specs trước khi lưu database
