# Job 03: Phân Phối Khoảng Giá Laptop

## 📊 Mục tiêu
Phân tích phân bố sản phẩm theo các khoảng giá để hiểu cấu trúc thị trường laptop của 2 đại lý.

## 🔄 Luồng xử lý

### 1. Đọc dữ liệu
- **TGDĐ**: `tgdd_raw_data.csv` - Giá đã ở định dạng số (float)
- **CellphoneS**: `cellphones_raw_data.csv` - Giá dạng chuỗi `"22.990.000đ"`

### 2. Làm sạch giá
```python
# TGDĐ: Chuyển đổi trực tiếp
laptops_df.withColumn("current_price", col("current_price").cast("float"))

# CellphoneS: Loại bỏ dấu chấm và ký tự 'đ'
cellphones_df.withColumn("current_price", 
    regexp_replace(col("current_price_raw"), "[.đ]", "").cast("float"))
```

### 3. Phân loại khoảng giá
Sử dụng `when()` để gán nhãn:
- `<5M`: Dưới 5 triệu
- `5-10M`: Từ 5-10 triệu
- `10-15M`: Từ 10-15 triệu
- `15-20M`: Từ 15-20 triệu
- `>20M`: Trên 20 triệu

### 4. Tổng hợp
```python
groupBy("price_range").agg(count("*").alias("count"))
```

## 💡 Insights

### TheGioiDiDong (TGDĐ)
| Khoảng giá | Số lượng | % |
|------------|----------|---|
| 5-10M      | 3        | 0.7% |
| 10-15M     | 41       | 9.9% |
| 15-20M     | 98       | 23.7% |
| >20M       | 272      | 65.7% |
| **Tổng**   | **414**  | **100%** |

**Nhận xét TGDĐ**:
- ✅ **Tập trung cao cấp**: 65.7% sản phẩm trên 20 triệu
- ✅ **Phân khúc chính**: 15-20M (23.7%) - laptop doanh nhân, sinh viên cao cấp
- ⚠️ **Thiếu phổ thông**: Chỉ 3 sản phẩm dưới 10 triệu (0.7%)
- 🎯 **Chiến lược**: Nhắm đến khách hàng có thu nhập trung-cao

### CellphoneS
| Khoảng giá | Số lượng | % |
|------------|----------|---|
| <5M        | 1        | 0.1% |
| 5-10M      | 16       | 2.1% |
| 10-15M     | 74       | 9.9% |
| 15-20M     | 118      | 15.7% |
| >20M       | 541      | 72.1% |
| **Tổng**   | **750**  | **100%** |

**Nhận xét CellphoneS**:
- ✅ **Cao cấp chiếm đa số**: 72.1% trên 20 triệu (cao hơn TGDĐ)
- ✅ **Kho hàng lớn hơn**: 750 sản phẩm vs 414 của TGDĐ (+81%)
- ✅ **Đa dạng hơn**: Có cả phân khúc <5M
- 🎯 **Chiến lược**: Phủ rộng nhưng ưu tiên cao cấp

## 📈 So sánh hai đại lý

| Tiêu chí | TGDĐ | CellphoneS | Ghi chú |
|----------|------|------------|---------|
| Tổng sản phẩm | 414 | 750 | CellphoneS nhiều hơn 81% |
| % Cao cấp (>20M) | 65.7% | 72.1% | CellphoneS tập trung cao cấp hơn |
| % Trung cấp (10-20M) | 33.6% | 25.6% | TGDĐ cân đối hơn |
| % Phổ thông (<10M) | 0.7% | 2.3% | Cả hai đều yếu phân khúc này |

## 🎯 Kết luận

1. **Thị trường laptop Việt Nam đang chuyển dịch cao cấp**:
   - Gần 70% sản phẩm > 20 triệu ở cả 2 đại lý
   - Phân khúc dưới 10 triệu gần như bị bỏ quên

2. **CellphoneS có lợi thế về số lượng**:
   - Nhiều hơn 336 sản phẩm (+81%)
   - Đặc biệt mạnh ở >20M (541 vs 272)

3. **TGDĐ cân đối hơn ở trung cấp**:
   - 33.6% trong khoảng 10-20M
   - Phù hợp với khách hàng cần laptop làm việc/học tập

4. **Cơ hội kinh doanh**:
   - ⚠️ Thiếu laptop phổ thông (<10M) - thị trường sinh viên/văn phòng
   - ✅ Laptop cao cấp có nhu cầu lớn - gaming, đồ họa, lập trình
