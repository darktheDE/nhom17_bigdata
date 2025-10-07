# 📖 Data Dictionary - Từ Điển Dữ Liệu Laptop

## Mô Tả Chi Tiết Các Thuộc Tính Dữ Liệu

### 1. Thông Tin Định Danh

#### `id` (Integer)
- **Mô tả:** Số định danh duy nhất cho mỗi sản phẩm laptop
- **Kiểu:** Integer, Primary Key
- **Ràng buộc:** NOT NULL, UNIQUE
- **Ví dụ:** 1, 2, 3, 1001

#### `product_name` (String)
- **Mô tả:** Tên đầy đủ của sản phẩm laptop (bao gồm model, cấu hình)
- **Kiểu:** VARCHAR(500)
- **Ràng buộc:** NOT NULL
- **Ví dụ:** 
  - "Laptop HP 15 fc0085AU - A6VV8PA (R5 7430U, 16GB, 512GB, Full HD, Win11)"
  - "Laptop Dell Inspiron 15 3530 - N5I5530W1 (i5 1334U, 16GB, 512GB, Full HD 120Hz, OfficeH24+365, Win11)"
  - "Laptop MacBook Air 13 inch M4 16GB/256GB"

#### `brand` (String)
- **Mô tả:** Thương hiệu/hãng sản xuất laptop
- **Kiểu:** VARCHAR(50)
- **Giá trị phổ biến:** HP, Dell, Asus, Lenovo, Acer, MacBook, MSI, Gigabyte, LG
- **Ví dụ:** "HP", "Dell", "Asus", "MacBook"

#### `category` (String)
- **Mô tả:** Danh mục sản phẩm
- **Kiểu:** VARCHAR(50)
- **Giá trị:** "Laptop"
- **Ví dụ:** "Laptop"

---

### 2. Thông Tin Giá Cả

#### `current_price` (Float)
- **Mô tả:** Giá bán hiện tại của sản phẩm (VNĐ)
- **Kiểu:** DECIMAL(12,0)
- **Ràng buộc:** >= 0
- **Đơn vị:** VNĐ (Việt Nam Đồng)
- **Khoảng giá trị:** 10,000,000 - 60,000,000
- **Ví dụ:** 13190000 (13.19 triệu VNĐ)

#### `list_price` (Float)
- **Mô tả:** Giá niêm yết gốc trước khi giảm giá (VNĐ)
- **Kiểu:** DECIMAL(12,0)
- **Ràng buộc:** >= current_price
- **Đơn vị:** VNĐ
- **Ví dụ:** 14890000 (14.89 triệu VNĐ)

#### `discount_percent` (Calculated)
- **Mô tả:** Phần trăm giảm giá (có thể tính toán)
- **Kiểu:** DECIMAL(5,2)
- **Công thức:** `((list_price - current_price) / list_price) * 100`
- **Khoảng giá trị:** 0% - 30%
- **Ví dụ:** 11.42% (giảm 11.42%)

---

### 3. Đánh Giá

#### `average_rating` (Float)
- **Mô tả:** Điểm đánh giá trung bình từ người dùng
- **Kiểu:** DECIMAL(2,1)
- **Khoảng giá trị:** 1.0 - 5.0 (sao)
- **Ví dụ:** 4.9, 5.0, 4.7
- **Lưu ý:** NULL hoặc N/A nếu chưa có đánh giá

---

### 4. Thông Số Kỹ Thuật

#### `cpu` (String)
- **Mô tả:** Loại CPU (bộ vi xử lý)
- **Kiểu:** VARCHAR(100)
- **Giá trị phổ biến:**
  - **Intel:** i3, i5, i7, i9 (các thế hệ 11, 12, 13, 14)
  - **AMD:** R5 (Ryzen 5), R7 (Ryzen 7)
  - **Apple:** M1, M2, M3, M4
- **Ví dụ:** 
  - "R5 7430U" (AMD Ryzen 5)
  - "i5 1334U" (Intel Core i5 thế hệ 13)
  - "i3 1315U" (Intel Core i3)
  - "M4" (Apple Silicon)

#### `ram` (String)
- **Mô tả:** Dung lượng RAM (bộ nhớ truy cập ngẫu nhiên)
- **Kiểu:** VARCHAR(20)
- **Giá trị phổ biến:** "4GB", "8GB", "16GB", "32GB", "64GB"
- **Ví dụ:** "8GB", "16GB"

#### `storage` (String)
- **Mô tả:** Dung lượng ổ cứng (SSD/HDD)
- **Kiểu:** VARCHAR(20)
- **Giá trị phổ biến:** "256GB", "512GB", "1TB", "2TB"
- **Công nghệ:** Thường là SSD (Solid State Drive)
- **Ví dụ:** "512GB", "256GB"

#### `screen_size` (String)
- **Mô tả:** Kích thước màn hình
- **Kiểu:** VARCHAR(20)
- **Đơn vị:** inch
- **Khoảng giá trị:** 13" - 17"
- **Phổ biến:** 13.3", 14", 15.6", 16"
- **Ví dụ:** "13 inch", "15 inch", "N/A"

#### `screen_resolution` (String)
- **Mô tả:** Độ phân giải màn hình
- **Kiểu:** VARCHAR(50)
- **Giá trị phổ biến:**
  - "Full HD" (1920x1080)
  - "WUXGA" (1920x1200)
  - "2K" (2560x1440)
  - "4K" (3840x2160)
  - "Retina" (MacBook)
- **Ví dụ:** "Full HD", "WUXGA", "Full HD 120Hz"

#### `os` (String)
- **Mô tả:** Hệ điều hành
- **Kiểu:** VARCHAR(50)
- **Giá trị phổ biến:** 
  - "Windows 11"
  - "Windows 10"
  - "macOS" (cho MacBook)
  - "Linux" (ít phổ biến)
- **Ví dụ:** "Windows 11", "macOS"

#### `software` (String)
- **Mô tả:** Phần mềm đi kèm (thường là Microsoft Office)
- **Kiểu:** VARCHAR(100)
- **Giá trị phổ biến:**
  - "OfficeH24+365" (Office Home 2024 + Microsoft 365)
  - "OfficeHS" (Office Home & Student)
  - "N/A" (không có)
- **Ví dụ:** "OfficeH24+365", "OfficeHS", "N/A"

---

### 5. Thông Tin Meta

#### `product_url` (String)
- **Mô tả:** Link URL nguồn của sản phẩm
- **Kiểu:** TEXT
- **Ví dụ:** 
  - "https://www.thegioididong.com/laptop/hp-15-fc0085au-r5-a6vv8pa"
  - "https://cellphones.com.vn/laptop-dell-inspiron-15.html"

---

## 📊 Phân Loại Dữ Liệu

### Dữ Liệu Số (Numeric)
- `id`, `current_price`, `list_price`, `average_rating`

### Dữ Liệu Văn Bản (Text)
- `product_name`, `brand`, `category`, `cpu`, `ram`, `storage`
- `screen_size`, `screen_resolution`, `os`, `software`, `product_url`

---

## 📐 Phân Khúc Sản Phẩm (Market Segments)

### Theo Giá:
- **Budget:** < 15 triệu VNĐ (sinh viên, văn phòng cơ bản)
- **Mid-range:** 15-25 triệu VNĐ (văn phòng cao cấp, đa nhiệm)
- **Premium:** 25-35 triệu VNĐ (thiết kế, lập trình)
- **High-end:** > 35 triệu VNĐ (gaming, workstation, MacBook Pro)

### Theo CPU:
- **Entry:** i3, R3, Celeron, Pentium
- **Mainstream:** i5, R5
- **Performance:** i7, R7
- **Enthusiast:** i9, R9, Apple M-series

### Theo RAM:
- **Basic:** 4GB - 8GB (văn phòng nhẹ)
- **Standard:** 16GB (đa nhiệm, phát triển phần mềm)
- **Pro:** 32GB+ (đồ họa, render, gaming cao cấp)

---

## ⚠️ Xử Lý Dữ Liệu Thiếu (Missing Values)

| Thuộc Tính | Xử Lý Khi NULL hoặc "N/A" |
|------------|----------------|
| `average_rating` | Gán = 0 hoặc loại bỏ khỏi phân tích đánh giá |
| `screen_size` | Trích xuất từ `product_name` hoặc gán = "Unknown" |
| `screen_resolution` | Trích xuất từ `product_name` hoặc gán = "Unknown" |
| `software` | Gán = "None" (không có phần mềm đi kèm) |
| `cpu`, `ram`, `storage` | Trích xuất từ `product_name` nếu thiếu |

---

## 🔍 Lưu Ý Quan Trọng

1. **Tên sản phẩm chứa nhiều thông tin:** Nhiều thuộc tính kỹ thuật có thể được trích xuất từ `product_name`
2. **Độ nhất quán brand:** Cần chuẩn hóa tên brand (ví dụ: "MacBook" vs "Apple")
3. **Format CPU:** Cần xử lý các format khác nhau (i5 1334U, i5-1334U, Intel Core i5 1334U)
4. **Tính discount_percent:** Cần tính toán từ `current_price` và `list_price`
