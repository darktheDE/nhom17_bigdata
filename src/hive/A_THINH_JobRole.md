### **Tổng quan vai trò Data Analyst (Anh Thịnh)**

*   **Nhiệm vụ cốt lõi:** Anh Thịnh là "thám tử" của dữ liệu. Anh Thịnh nhận các bộ dữ liệu lớn đã được xử lý sơ bộ, sử dụng công cụ truy vấn chuyên dụng (Hive) để "thẩm vấn" dữ liệu, tìm ra các mẫu (patterns), xu hướng (trends), và các sự thật ngầm hiểu (insights).
*   **Mục tiêu cuối cùng:** Chuyển hóa các kết quả truy vấn thành những câu chuyện kinh doanh có ý nghĩa và cung cấp các bộ dữ liệu tổng hợp, sạch sẽ cho BI Developer (Duy) để xây dựng dashboard.

---

### **Kế hoạch chi tiết theo từng giai đoạn**

#### **Giai đoạn 1: Chuẩn bị & Khám phá ban đầu (Tuần 1)**

Mục tiêu của tuần này là kết nối thành công với "hiện trường vụ án" (dữ liệu trên HDFS) và thực hiện những cuộc "thẩm vấn" đầu tiên để nắm bắt tình hình chung.

*   **Bước 1: Đồng bộ Môi trường & Tiếp nhận thông tin**
    *   **Công việc:**
        1.  Phối hợp với Big Data Developer (Anh Thịnh) để nhận file tài liệu bàn giao, trong đó có:
            *   Đường dẫn HDFS của file CSV gốc.
            *   Đường dẫn và cấu trúc (schema) của các bộ dữ liệu đầu ra từ MapReduce.
        2.  Đảm bảo Anh Thịnh có thể truy cập vào server CentOS và sử dụng được Hive client (Beeline).
    *   **Mục tiêu:** Nắm rõ trong tay có những "chứng cứ" gì và công cụ "điều tra" đã sẵn sàng.

*   **Bước 2: Tạo Bảng Hive cho Dữ liệu Gốc**
    *   **Công việc:** Viết một câu lệnh DDL (Data Definition Language) để tạo một **bảng ngoài (External Table)** trong Hive. Bảng này sẽ trỏ trực tiếp đến file `laptops.csv` gốc trên HDFS.
        ```sql
        CREATE EXTERNAL TABLE IF NOT EXISTS raw_laptops (
            id STRING,
            product_name STRING,
            current_price DOUBLE,
            list_price DOUBLE,
            brand STRING,
            -- ... (các cột còn lại)
        )
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        STORED AS TEXTFILE
        LOCATION '/user/nhom2/input/'
        TBLPROPERTIES ("skip.header.line.count"="1");
        ```
    *   **Mục tiêu:** Có thể dùng SQL để truy vấn toàn bộ dữ liệu thô mà không cần di chuyển file.

*   **Bước 3: Chạy Truy vấn "Kiểm tra"**
    *   **Công việc:** Thực hiện một vài câu lệnh HiveQL cực kỳ đơn giản để xác nhận mọi thứ hoạt động trơn tru.
        *   `SELECT * FROM raw_laptops LIMIT 10;` — Xem 10 dòng đầu tiên.
        *   `SELECT DISTINCT brand FROM raw_laptops;` — Xem có những thương hiệu nào.
        *   `DESCRIBE raw_laptops;` — Kiểm tra lại cấu trúc bảng.
    *   **Mục tiêu:** Xác nhận 100% rằng Anh Thịnh có thể truy vấn được dữ liệu.

#### **Giai đoạn 2: Phân tích Tổng quan (Tuần 2)**

Bây giờ Anh Thịnh sẽ đi vào phân tích các chỉ số kinh doanh chính, trả lời những câu hỏi lớn.

*   **Bước 4: Tạo Bảng Hive cho Dữ liệu đã xử lý**
    *   **Công việc:** Dựa trên tài liệu bàn giao của Big Data Developer, tạo các bảng Hive tương ứng cho các kết quả từ jobs MapReduce (ví dụ: `word_counts`, `price_segments`,...).
    *   **Mục tiêu:** Hợp nhất tất cả các nguồn dữ liệu (cả thô và đã xử lý) vào một nơi duy nhất để dễ dàng truy vấn.

*   **Bước 5: Trả lời các Câu hỏi Kinh doanh bằng HiveQL**
    *   **Công việc:** Viết các câu lệnh HiveQL để trả lời các câu hỏi mang tính tổng hợp.
        *   **Thị phần:** `SELECT brand, COUNT(*) AS so_luong FROM raw_laptops GROUP BY brand;`
        *   **Top 10 rating cao:** `SELECT product_name, average_rating FROM raw_laptops ORDER BY average_rating DESC LIMIT 10;`
        *   **Phân khúc giá:** Dùng `CASE WHEN ... THEN ... END` để tạo các phân khúc giá rồi `GROUP BY`.
    *   **Mục tiêu:** Tạo ra các bảng kết quả đầu tiên.

*   **Bước 6: Xuất kết quả Lô 1**
    *   **Công việc:** Lưu kết quả của các truy vấn trên thành các file CSV nhỏ. Anh Thịnh có thể dùng lệnh `INSERT OVERWRITE LOCAL DIRECTORY ...` của Hive hoặc đơn giản là copy/paste kết quả từ terminal ra file.
    *   **Mục tiêu:** Bàn giao những kết quả đầu tiên cho Duy để anh ấy có thể bắt đầu dựng khung cho dashboard.

#### **Giai đoạn 3: Phân tích Chuyên sâu (Tuần 3)**

Tuần này Anh Thịnh sẽ đi sâu hơn, tìm kiếm các mối liên hệ ẩn và xác thực lại kết quả.

*   **Bước 7: Truy vấn Kết hợp (JOIN)**
    *   **Công việc:** Viết các câu lệnh HiveQL phức tạp hơn, kết hợp dữ liệu từ nhiều nguồn.
        *   **Ví dụ:** `JOIN` bảng `raw_laptops` với bảng `word_counts` (từ MapReduce) để tìm xem giá trung bình của các điện thoại có chữ "Pro" là bao nhiêu.
    *   **Mục tiêu:** Tìm ra những insight mà việc phân tích trên một bảng đơn lẻ không thể thấy được.

*   **Bước 8: Xác thực chéo kết quả MapReduce**
    *   **Công việc:** Chọn 1-2 job MapReduce (ví dụ: job đếm sản phẩm theo thương hiệu) và viết lại logic tương tự bằng HiveQL. So sánh kết quả của Anh Thịnh với kết quả của Big Data Developer.
    *   **Mục tiêu:** Đảm bảo tính nhất quán và chính xác của dữ liệu. Đây là một bước làm việc rất chuyên nghiệp.

#### **Giai đoạn 4: Tổng hợp & Bàn giao (Tuần 4)**

Giai đoạn cuối cùng để "đóng gói" tất cả những phát hiện của Anh Thịnh.

*   **Bước 9: Tổng hợp Insight**
    *   **Công việc:** Dựa trên tất cả kết quả, viết ra **3-5 gạch đầu dòng quan trọng nhất** mà Anh Thịnh đã phát hiện. Đây là phần giá trị nhất của một Data Analyst.
        *   *Ví dụ:* "Insight 1: Mặc dù Apple có ít mẫu mã nhất, nhưng lại chiếm trọn phân khúc cao cấp và có điểm rating trung bình cao vượt trội."
        *   *Ví dụ:* "Insight 2: Các thương hiệu Trung Quốc (Xiaomi, Oppo) có mức giảm giá trung bình cao nhất, cho thấy sự cạnh tranh khốc liệt về giá ở phân khúc tầm trung."
    *   **Mục tiêu:** Chuyển hóa từ "kết quả" thành "thông điệp kinh doanh".

*   **Bước 10: Hoàn thiện và Đóng gói Dữ liệu Bàn giao**
    *   **Công việc:** Tập hợp tất cả các file CSV kết quả vào một thư mục. Viết một file `README.txt` đơn giản, giải thích mỗi file chứa thông tin gì (ví dụ: `brand_market_share.csv` - chứa thị phần các hãng).
    *   **Mục tiêu:** Bàn giao một sản phẩm dữ liệu sạch sẽ, rõ ràng, có tài liệu hướng dẫn cho Duy.

*   **Bước 11: Họp Bàn giao với BI Developer**
    *   **Công việc:** Có một buổi trao đổi ngắn (15-20 phút) với Duy. Trình bày 3-5 insight quan trọng nhất và giải thích các file dữ liệu Anh Thịnh đã chuẩn bị. Gợi ý cho Duy nên dùng biểu đồ nào để làm nổi bật insight nào.
    *   **Mục tiêu:** Đảm bảo Duy hiểu đúng ý đồ phân tích và có thể xây dựng một dashboard "biết nói".