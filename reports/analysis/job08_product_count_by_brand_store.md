# Job 08: Thống Kê Số Lượng Sản Phẩm Theo Thương Hiệu & Cửa Hàng

## 📊 Mục Đích
Đếm và so sánh số lượng laptop của từng thương hiệu được bán tại TGDĐ và CellphoneS để đánh giá độ phủ thương hiệu.

## 🔄 Luồng Xử Lý

### Bước 1: Đọc Dữ Liệu
- **TGDĐ**: Đọc từ `tgdd_raw_data.csv` (có sẵn cột `brand`)
- **CellphoneS**: Đọc từ `cellphones_raw_data.csv` (cần tách brand từ `product_name`)

### Bước 2: Chuẩn Hóa Brand
**Với CellphoneS**:
```python
# Tách từ đầu tiên từ tên sản phẩm
first_word = split(product_name, " ")[0]

# Nếu từ đầu = "Laptop" → lấy từ thứ 2
# Ngược lại → lấy từ đầu (MacBook, ASUS, HP...)
brand = if (first_word == "laptop") then word[1] else word[0]
```

### Bước 3: Gán Store Name
- Mỗi brand được coi như 1 "store_name" (vì không có thông tin cửa hàng cụ thể)
- Thực tế: brand = store_name

### Bước 4: Aggregation
```python
groupBy(brand, store_name)
  .count()
  .orderBy(product_count DESC)
```

### Bước 5: Xuất Kết Quả
- TGDĐ → `job08_product_count_tgdd/`
- CellphoneS → `job08_product_count_cellphones/`

## 📈 Phân Tích Kết Quả

### **CellphoneS (750 sản phẩm)**
| Thương Hiệu | Số Lượng | Thị Phần |
|-------------|----------|----------|
| **ASUS**    | 162      | 21.6%    |
| **Lenovo**  | 154      | 20.5%    |
| Dell        | 83       | 11.1%    |
| HP          | 83       | 11.1%    |
| MSI         | 75       | 10.0%    |
| MacBook     | 61       | 8.1%     |
| Acer        | 48       | 6.4%     |

### **TGDĐ (414 sản phẩm)**
| Thương Hiệu | Số Lượng | Thị Phần |
|-------------|----------|----------|
| **HP**      | 81       | 19.6%    |
| **Asus**    | 78       | 18.8%    |
| **Lenovo**  | 67       | 16.2%    |
| Dell        | 60       | 14.5%    |
| Acer        | 49       | 11.8%    |
| MSI         | 47       | 11.4%    |
| MacBook     | 14       | 3.4%     |

## 💡 Insights Quan Trọng

### 1. **Sự Khác Biệt Về Kho Hàng**
- CellphoneS có **nhiều gấp đôi** sản phẩm so với TGDĐ (750 vs 414)
- Nguyên nhân: CellphoneS có chiến lược nhập nhiều model, TGDĐ chọn lọc kỹ

### 2. **Thương Hiệu Phổ Biến**
**Top 3 tại CellphoneS**: ASUS (162) > Lenovo (154) > Dell/HP (83)  
**Top 3 tại TGDĐ**: HP (81) > Asus (78) > Lenovo (67)

→ **ASUS/Lenovo** thống trị CellphoneS, **HP** dẫn đầu TGDĐ

### 3. **MacBook - Khác Biệt Lớn**
- CellphoneS: 61 + 13 (Mac) + 8 (iMac) + 8 (Apple) = **90 sản phẩm Apple**
- TGDĐ: Chỉ **14 MacBook**

→ CellphoneS là điểm đến tốt hơn cho khách hàng tìm sản phẩm Apple

### 4. **Vấn Đề Chuẩn Hóa Dữ Liệu**
**CellphoneS**:
- "ASUS" (162) vs "Asus" (3) → Cần uppercase chuẩn hóa
- "MacBook" (61) vs "Macbook" (1) vs "Mac" (13) → Nhiều cách viết
- "Gaming" (16) + "gaming" (1) → Không phải brand, là danh mục
- Có 1 dòng thiếu brand (`,,1`)

**TGDĐ**:
- `"Win11)\""` (4) → Lỗi parse dữ liệu từ cột description
- Ít vấn đề hơn vì có sẵn cột brand

### 5. **Long Tail Brands**
- CellphoneS có nhiều brand nhỏ: Vaio, Alienware, Huawei, Masstel, Fujitsu, Avita (≤3 sản phẩm/brand)
- TGDĐ tập trung vào 7 brand chính, ít phân mảnh hơn

## 🎯 Khuyến Nghị

### Cho Data Engineer:
1. **Chuẩn hóa brand**:
   ```python
   # Thêm bước upper() và map synonym
   brand = upper(first_word)
   brand_map = {"MAC": "MacBook", "IMAC": "MacBook", "APPLE": "MacBook"}
   ```

2. **Lọc bỏ noise**:
   - Loại bỏ "Gaming"/"gaming" (là category, không phải brand)
   - Xử lý dòng missing brand (`,,1`)
   - Clean `"Win11)\""` từ TGDĐ

### Cho Business:
1. **CellphoneS** phù hợp nếu cần:
   - Đa dạng lựa chọn (750 models)
   - Nhiều sản phẩm ASUS/Lenovo
   - Hệ sinh thái Apple phong phú

2. **TGDĐ** phù hợp nếu cần:
   - Catalog chọn lọc, dễ quyết định (414 models)
   - Sản phẩm HP chất lượng cao
   - Ít bị overwhelm bởi quá nhiều lựa chọn

## 📊 Biểu Đồ Minh Họa

```
So Sánh Top 5 Brands (số lượng sản phẩm):

ASUS      ████████████████████ 162 (CPS) | ███████████████ 78 (TGDĐ)
Lenovo    ███████████████████ 154 (CPS)  | ████████████ 67 (TGDĐ)
HP        ████████ 83 (CPS)              | ███████████████ 81 (TGDĐ)
Dell      ████████ 83 (CPS)              | ███████████ 60 (TGDĐ)
MSI       ███████ 75 (CPS)               | ██████████ 47 (TGDĐ)
```

**Kết luận**: CellphoneS có chiến lược "SKU nhiều, tạo sự lựa chọn", TGDĐ theo "chọn lọc, bán chạy".
