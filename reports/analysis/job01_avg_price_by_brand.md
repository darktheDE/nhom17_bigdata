# Job 01: Phân Tích Giá Trung Bình Theo Thương Hiệu

## 📋 Mô tả Job

**Mục tiêu**: Tính giá trung bình của laptop theo từng thương hiệu từ 2 nguồn dữ liệu TGDĐ và CellphoneS.

## 🔄 Luồng Xử Lý (PySpark)

### 1. **Xử lý dữ liệu TGDĐ** (`tgdd_raw_data.csv`)
```
Đọc CSV → Cast current_price sang float → GroupBy brand → Tính AVG(current_price) → Sắp xếp giảm dần
```

**Đặc điểm**: 
- Cột `brand` có sẵn
- Giá đã là số (float): `13190000.0`

### 2. **Xử lý dữ liệu CellphoneS** (`cellphones_raw_data.csv`)
```
Đọc CSV → Làm sạch giá (loại bỏ dấu chấm và "đ") → Tách brand từ product_name → GroupBy brand → Tính AVG(current_price) → Sắp xếp giảm dần
```

**Đặc điểm**:
- **Không có cột `brand`** → Tách từ `product_name`
- Giá dạng string: `"22.990.000đ"` → Regex replace `[.đ]` → `22990000`
- Logic tách brand: 
  - Nếu từ đầu = "Laptop" → lấy từ thứ 2
  - Ngược lại → lấy từ đầu tiên

## 📊 Kết Quả & Insight

### **Top 5 Thương Hiệu Đắt Nhất - CellphoneS**

| Thứ hạng | Thương hiệu | Giá trung bình (VNĐ) |
|----------|-------------|----------------------|
| 1️⃣ | MacBook | **50,932,833** (~51 triệu) |
| 2️⃣ | iMac | 44,635,714 (~45 triệu) |
| 3️⃣ | Apple | 40,875,714 (~41 triệu) |
| 4️⃣ | Gigabyte | 33,647,143 (~34 triệu) |
| 5️⃣ | MSI | 28,652,121 (~29 triệu) |

### **Top 5 Thương Hiệu Đắt Nhất - TGDĐ**

| Thứ hạng | Thương hiệu | Giá trung bình (VNĐ) |
|----------|-------------|----------------------|
| 1️⃣ | MacBook | **37,797,692** (~38 triệu) |
| 2️⃣ | MSI | 36,791,333 (~37 triệu) |
| 3️⃣ | Gigabyte | 33,473,333 (~33 triệu) |
| 4️⃣ | Lenovo | 30,950,938 (~31 triệu) |
| 5️⃣ | HP | 24,466,471 (~24 triệu) |

### **So Sánh Giữa 2 Cửa Hàng**

| Thương hiệu | CellphoneS (VNĐ) | TGDĐ (VNĐ) | Chênh lệch |
|-------------|------------------|-------------|------------|
| MacBook | 50,932,833 | 37,797,692 | **+13,135,141** (CellphoneS đắt hơn 34.7%) |
| MSI | 28,652,121 | 36,791,333 | **-8,139,212** (TGDĐ đắt hơn 28.4%) |
| Gigabyte | 33,647,143 | 33,473,333 | +173,810 (gần bằng nhau) |
| Lenovo | 27,695,217 | 30,950,938 | -3,255,721 (TGDĐ đắt hơn 11.8%) |

## 💡 Nhận Định Quan Trọng

### ✅ **Điểm Mạnh**
1. **MacBook thống trị phân khúc cao cấp** ở cả 2 cửa hàng (>37-51 triệu)
2. **Gigabyte có giá ổn định** giữa 2 kênh (~33-34 triệu)
3. **CellphoneS có nhiều thương hiệu hơn** (24 brands vs 10 brands)

### ⚠️ **Vấn Đề Dữ Liệu**
1. **Dữ liệu CellphoneS có nhiễu**:
   - Giá trị NULL/rỗng (Avita, Fujitsu, Huawei, Vaio, Samsung...)
   - Trùng lặp brand: `MacBook` vs `Macbook`, `ASUS` vs `Asus`, `Gaming` vs `gaming`
   - Parsing lỗi: `"Win11)\""`

2. **Cần cải thiện**:
   - Chuẩn hóa tên brand (lowercase, trim)
   - Filter NULL values trước khi tính toán
   - Xử lý edge case khi parse `product_name`

### 🎯 **Chiến Lược Kinh Doanh**
- **CellphoneS**: Định vị cao cấp hơn với MacBook (+35% giá)
- **TGDĐ**: Cạnh tranh tốt ở Gaming laptop (MSI, Gigabyte)
- **HP, Dell, Acer**: Phân khúc mainstream (19-24 triệu)

## 📁 Output Files
- `data/processed_for_bi/job01_avg_price_cellphones/part-*.csv`
- `data/processed_for_bi/job01_avg_price_tgdd/part-*.csv`
