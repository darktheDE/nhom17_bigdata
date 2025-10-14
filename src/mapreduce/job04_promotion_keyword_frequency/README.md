# Job 04: Thống Kê Tần Suất Từ Khóa Khuyến Mãi

## Mô tả
Phân tích các từ khóa phổ biến trong chương trình khuyến mãi để hiểu xu hướng marketing của các nhà bán lẻ.

## Đầu vào
- `tgdd_promo.json`: Khuyến mãi từ Thế Giới Di Động (JSON array)
- `cellphones_promo.json`: Khuyến mãi từ CellphoneS (JSON array)

## Đầu ra
Format: `keyword \t frequency`

Kết quả mẫu:
```
Tặng	78
Phiếu Mua Hàng	61
Giảm	42
0%	26
Balo	18
Màn Hình	18
```

## Từ khóa theo dõi
- Hình thức thanh toán: "trả góp", "0%", "giảm ngay"
- Quà tặng: "tặng", "balo", "túi", "chuột", "tai nghe", "loa"
- Voucher: "phiếu mua hàng", "voucher"
- Dịch vụ: "bảo hành", "thu cũ", "lên đời"
- Phần mềm: "office", "microsoft", "win11"

## Chạy Local Test
```bash
cd src/mapreduce/job04_promotion_keyword_frequency
python run_local.py
```

## Chạy trên Hadoop Streaming
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/promotions_json/* \
  -output /output/job04_promotion_keyword_frequency \
  -file src/mapreduce/job04_promotion_keyword_frequency/mapper.py \
  -file src/mapreduce/job04_promotion_keyword_frequency/reducer.py
```

## Logic xử lý

### Mapper
1. Đọc toàn bộ file JSON (array lớn)
2. Parse JSON thành Python list
3. Duyệt qua từng sản phẩm → mảng `promotions`
4. Với mỗi chuỗi khuyến mãi, tìm các từ khóa quan trọng
5. Output: `keyword \t 1`

### Reducer
1. Đếm tổng số lần xuất hiện của mỗi từ khóa
2. Output: `keyword \t total_count`

## Lưu ý kỹ thuật
- **JSON parsing**: Đọc toàn bộ file vào memory (OK cho dataset vừa/nhỏ)
- **UTF-8 handling**: Đặc biệt quan trọng vì từ khóa tiếng Việt
- **Keyword matching**: So sánh lowercase để không phân biệt hoa thường
- **Chuẩn hóa output**: `.title()` để viết hoa đầu mỗi từ
