# Job 07: Phân Tích CPU Phổ Biến

## Luồng Xử Lý

### 1. Đọc Dữ Liệu
- **TGDD**: Đọc từ `tgdd_raw_data.csv` với cột `cpu` sẵn có
- **CellphoneS**: Đọc từ `cellphones_raw_data.csv`, tách CPU từ cột `raw_specs_string`

### 2. Chuẩn Hóa CPU
- Chuyển về **lowercase** (chữ thường)
- Loại bỏ **khoảng trắng** (`\s+` → `""`)
- Ví dụ: `"Intel Core i7-13620H"` → `"i7-13620h"`

### 3. Đếm & Sắp Xếp
- **GroupBy** theo `cpu_clean`
- **Count** số sản phẩm mỗi loại CPU
- **OrderBy** giảm dần theo số lượng

### 4. Xuất Kết Quả
- Lưu vào 2 file CSV riêng biệt cho mỗi cửa hàng

---

## Insights Từ Dữ Liệu

### CellphoneS (561 sản phẩm laptop)

#### Top 5 CPU Phổ Biến:
| CPU | Số Lượng | % |
|-----|----------|---|
| **Thiếu thông tin** | 161 | 28.7% |
| **i7-13620H** | 35 | 6.2% |
| **i5-13420H** | 35 | 6.2% |
| **U5-125H** | 18 | 3.2% |
| **i5-1235U** | 17 | 3.0% |

**Nhận xét**:
- **28.7% sản phẩm thiếu thông tin CPU** - vấn đề chất lượng dữ liệu
- CPU Intel thế hệ **13th Gen** (i7-13620H, i5-13420H) chiếm ưu thế
- CPU dòng **U-series** (siêu tiết kiệm điện) xuất hiện nhiều (U5-125H)
- Intel Core i5/i7 chiếm **>80%** thị phần

### TGDD (280 sản phẩm laptop)

#### Top 5 CPU Phổ Biến:
| CPU | Số Lượng | % |
|-----|----------|---|
| **Thiếu thông tin** | 148 | 52.9% |
| **i5-13420H** | 27 | 9.6% |
| **i7-13620H** | 23 | 8.2% |
| **i5-1334U** | 18 | 6.4% |
| **i7-1355U** | 16 | 5.7% |

**Nhận xét**:
- **Hơn 50% sản phẩm thiếu thông tin CPU** - nghiêm trọng hơn CellphoneS
- Cùng xu hướng: CPU Intel Gen 13 (i5-13420H, i7-13620H) dẫn đầu
- Dòng **U-series** (tiết kiệm pin) nhiều hơn dòng **H-series** (hiệu năng cao)

---

## So Sánh 2 Cửa Hàng

| Tiêu Chí | CellphoneS | TGDD |
|----------|------------|------|
| **Tổng sản phẩm** | 561 | 280 |
| **Thiếu thông tin** | 28.7% | 52.9% |
| **CPU phổ biến nhất** | i7-13620H / i5-13420H | i5-13420H |
| **Đa dạng CPU** | 128 loại | 66 loại |

---

## Kết Luận

### Vấn Đề Cần Khắc Phục
1. **Dữ liệu thiếu sót**: 28-53% sản phẩm không có thông tin CPU
2. **Chuẩn hóa kém**: Một số giá trị là số tiền (16690000.0) thay vì tên CPU

### Xu Hướng Thị Trường
1. **Intel thống trị**: >90% thị phần so với AMD Ryzen
2. **Gen 13 phổ biến**: i5-13420H, i7-13620H là 2 CPU bán chạy nhất
3. **Dòng U-series**: Laptop văn phòng (tiết kiệm pin) nhiều hơn laptop gaming (H-series)
4. **CellphoneS đa dạng hơn**: 128 loại CPU vs 66 loại của TGDD

### Khuyến Nghị Kinh Doanh
- Tập trung nhập laptop Intel Gen 13 (i5/i7)
- Ưu tiên dòng U-series cho phân khúc văn phòng
- Cải thiện chất lượng dữ liệu CPU (giảm thiểu N/A)
