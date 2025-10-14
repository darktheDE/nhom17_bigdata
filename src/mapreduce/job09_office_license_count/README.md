# Job 09: Office License Count

## 📋 Mô tả
Đếm số lượng laptop được tặng kèm bản quyền Microsoft Office Home & Student từ dữ liệu TGDĐ.

## 🎯 Mục tiêu
- Phân tích chiến lược khuyến mãi bằng phần mềm bản quyền
- Xác định tỷ lệ sản phẩm có Office miễn phí
- So sánh giá trị gia tăng từ Office license

## 📊 Input/Output

### Input
- **File**: `data/raw/tgdd_raw_data.csv`
- **Columns sử dụng**: `software`
- **Lưu ý**: Chỉ TGDĐ có cột `software`, CellphoneS không có

### Output
```
No Office       414
```

**Format**: `category \t count`
- **No Office**: Số sản phẩm không có Office H&S
- **Office H&S**: Số sản phẩm có Office Home & Student

## 🔍 Kết quả phân tích (RAW DATA)

### Kết quả thực tế
```
No Office: 414 sản phẩm (100%)
Office H&S: 0 sản phẩm (0%)
```

### 💡 Insight
1. **Không có sản phẩm nào** được tặng Office H&S trong dataset TGDĐ hiện tại
2. Cột `software` đều có giá trị `N/A` hoặc không chứa "Office Home & Student"
3. **Giả thuyết**: 
   - TGDĐ có thể đã thay đổi chính sách khuyến mãi
   - Office H&S có thể được tặng riêng qua chương trình khuyến mãi khác
   - Data scraping có thể cần cập nhật để capture đúng thông tin Office

### Business implication
- Cần verify lại data source để đảm bảo đầy đủ thông tin khuyến mãi
- Có thể expand sang phân tích Windows license thay vì Office
- Xem xét các phần mềm bản quyền khác: Kaspersky, Adobe, AutoCAD

## 🛠️ Cách chạy

### Local Test
```bash
cd src/mapreduce/job09_office_license_count
python run_local.py
```

### Hadoop Production
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /raw_data/products_csv/tgdd_raw_data.csv \
  -output /output/job09_office_license_count
```

## 📝 Mapper Logic
```python
# Đọc CSV từ stdin
for row in csv.DictReader(sys.stdin):
    software = row.get('software', 'N/A').strip()
    
    # Kiểm tra keyword "Office Home & Student"
    if 'office home' in software.lower() and 'student' in software.lower():
        print(f"Office H&S\t1")
    else:
        print(f"No Office\t1")
```

## 📝 Reducer Logic
```python
# Aggregation đơn giản
from itertools import groupby

for key, group in groupby(sys.stdin, key=lambda x: x.split('\t')[0]):
    count = sum(int(line.split('\t')[1]) for line in group)
    print(f"{key}\t{count}")
```

## 🔄 Mở rộng

### Phiên bản cải tiến
1. **Multi-software detection**: Detect cả Office 365, Office 2021, etc.
2. **Cross-store comparison**: So sánh với CellphoneS (nếu có data)
3. **Value calculation**: Tính giá trị tiền tệ của Office license (~2.8 triệu)

### Sample output mở rộng
```
No Office       300     72.5%
Office H&S      80      19.3%
Office 365      34      8.2%
```

## 📚 Dependencies
- Python 3.x
- Standard library: `csv`, `sys`, `io`

## 👤 Developer
- **Đỗ Kiến Hưng** - MapReduce Developer
- Role: Design & implement 10 MapReduce jobs
