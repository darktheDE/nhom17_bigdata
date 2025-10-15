# Job 02: Phân Tích Tỷ Lệ Giảm Giá Theo Thương Hiệu

## Luồng Xử Lý Dữ Liệu

### 1. Đọc Dữ Liệu
- **TGDD**: `tgdd_raw_data.csv` - giá đã ở dạng số
- **CellphoneS**: `cellphones_raw_data.csv` - giá dạng chuỗi "22.990.000đ"

### 2. Làm Sạch Dữ Liệu
- **TGDD**: Chuyển `current_price` và `list_price` sang kiểu float
- **CellphoneS**: 
  - Xóa dấu chấm và ký tự "đ" khỏi giá
  - Tách brand từ `product_name` (từ đầu tiên, hoặc từ thứ 2 nếu có "Laptop")
- **Cả 2 nguồn**: Lọc bỏ giá NULL và `list_price = 0` (tránh chia cho 0)

### 3. Tính Toán
- **Công thức**: `discount_rate = (list_price - current_price) / list_price`
- Tính tỷ lệ giảm giá trung bình theo từng thương hiệu
- Sắp xếp giảm dần theo tỷ lệ giảm giá

### 4. Kết Quả
- **TGDD**: 9 thương hiệu
- **CellphoneS**: 16 thương hiệu

## Phân Tích Insight

### So Sánh Giữa 2 Sàn

#### TheGioiDiDong (TGDĐ)
| Thương hiệu | Tỷ lệ giảm giá trung bình |
|-------------|--------------------------|
| Samsung | 22.83% |
| Acer | 11.71% |
| HP | 11.56% |
| Asus | 10.39% |
| MacBook | 5.31% |

#### CellphoneS
| Thương hiệu | Tỷ lệ giảm giá trung bình |
|-------------|--------------------------|
| Masstel | 44.68% |
| LG | 34.89% |
| Asus | 31.48% |
| HP | 20.66% |
| MacBook | 11.14% |

### Các Phát Hiện Chính

1. **CellphoneS giảm giá mạnh hơn**:
   - Masstel giảm tới 44.68% (cao nhất toàn bộ)
   - LG giảm 34.89%
   - Asus giảm 31.48% (gấp 3 lần so với TGDĐ)

2. **Samsung chỉ có ở TGDĐ**:
   - Đứng đầu với 22.83% giảm giá
   - CellphoneS không bán laptop Samsung

3. **Apple/MacBook - Giảm giá ít nhất**:
   - TGDĐ: MacBook giảm 5.31%
   - CellphoneS: MacBook 11.14%, Apple 8.36%, iMac 5.22%
   - Sản phẩm cao cấp ít khuyến mãi hơn

4. **Thương hiệu gaming**:
   - MSI, Gigabyte giảm 6-13% ở cả 2 sàn
   - Tương đối đồng đều

5. **Vấn đề dữ liệu CellphoneS**:
   - Có brand trùng lặp: "Asus" (31.48%), "ASUS" (13.71%), "gaming" (21.06%), "Gaming" (17.17%)
   - Cần chuẩn hóa chữ hoa/thường và loại bỏ từ khóa chung

## Kết Luận

- **Chiến lược giá**: CellphoneS tập trung giảm giá mạnh để cạnh tranh, đặc biệt các thương hiệu phổ thông (Masstel, LG, Asus)
- **Sản phẩm cao cấp**: Apple/MacBook giữ giá tốt, ít khuyến mãi
- **Khuyến nghị**: Cần làm sạch brand name để kết quả chính xác hơn (chuẩn hóa chữ hoa/thường, gộp các biến thể)
