# Dữ Liệu Thô (Raw Data)

## 📄 Nguồn Gốc Dữ Liệu

Dữ liệu laptop được thu thập từ hai trang web thương mại điện tử lớn tại Việt Nam:
- **Thế Giới Di Động** (thegioididong.com/laptop)
- **CellphoneS** (cellphones.com.vn/laptop)

## 📊 Cấu Trúc Dữ Liệu

File: `laptops_sample.csv` (hoặc `laptops_full.csv` khi đã cào đầy đủ)

### Các Cột Dữ Liệu:

| Tên Cột | Kiểu Dữ Liệu | Mô Tả | Ví Dụ |
|---------|--------------|-------|-------|
| `id` | Integer | ID duy nhất của sản phẩm | 1, 2, 3, ... |
| `product_name` | String | Tên đầy đủ của sản phẩm | "Laptop HP 15 fc0085AU - A6VV8PA" |
| `current_price` | Float | Giá hiện tại (VNĐ) | 13190000 |
| `list_price` | Float | Giá niêm yết (VNĐ) | 14890000 |
| `brand` | String | Thương hiệu sản phẩm | "HP", "Dell", "Asus", "Lenovo" |
| `category` | String | Danh mục sản phẩm | "Laptop" |
| `cpu` | String | Loại CPU | "R5 7430U", "i5 1334U", "i3 1315U" |
| `ram` | String | Dung lượng RAM | "8GB", "16GB" |
| `storage` | String | Dung lượng ổ cứng | "256GB", "512GB" |
| `screen_size` | String | Kích thước màn hình | "13 inch", "15 inch" |
| `screen_resolution` | String | Độ phân giải màn hình | "Full HD", "WUXGA" |
| `os` | String | Hệ điều hành | "Windows 11", "macOS" |
| `software` | String | Phần mềm đi kèm | "OfficeH24+365", "OfficeHS" |
| `average_rating` | Float | Đánh giá trung bình (1-5 sao) | 4.9, 5.0 |
| `product_url` | String | Link sản phẩm | "https://..." |

## 📈 Thống Kê Dữ Liệu

- **Tổng số bản ghi:** ~1000+ sản phẩm laptop
- **Số thương hiệu:** ~10-15 thương hiệu (HP, Dell, Asus, Lenovo, Acer, MacBook, MSI, v.v.)
- **Khoảng giá:** 10,000,000 VNĐ - 60,000,000 VNĐ
- **Nguồn:** Thế Giới Di Động (60%), CellphoneS (40%)

## ⚠️ Lưu Ý

1. **Dữ liệu mẫu:** File `laptops_sample.csv` chỉ chứa ~200-300 bản ghi để test.
2. **Dữ liệu đầy đủ:** File `laptops_full.csv` chứa toàn bộ dữ liệu nhưng **KHÔNG** được commit lên GitHub.
3. **Dữ liệu thiếu:** Một số sản phẩm có thể thiếu thông tin ở một số trường.
4. **Làm sạch:** Dữ liệu đã được làm sạch cơ bản (loại bỏ ký tự đặc biệt, chuẩn hóa format).

## 🔄 Cập Nhật Dữ Liệu

Để cập nhật dữ liệu mới nhất:
```bash
cd src/scraping
python tgdd_scraper.py
python cellphones_scraper.py
```

Dữ liệu mới sẽ được ghi vào file `laptops_full.csv` với timestamp.
