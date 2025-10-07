### **Bối cảnh dự án: Phân tích Dữ liệu Big Data trong Ngành Bán lẻ Laptop**

**1. Tên đề tài:** Ứng dụng hệ sinh thái Hadoop để phân tích dữ liệu bán laptop từ các sàn thương mại điện tử lớn tại Việt Nam.

**2. Mục tiêu kinh doanh (Business Objective):**
Dự án nhằm mục đích khai thác dữ liệu công khai từ các trang web bán lẻ để rút ra các thông tin kinh doanh (business insights) có giá trị. Các mục tiêu chính bao gồm:
*   Phân tích thị phần của các thương hiệu (Apple, Samsung, Xiaomi,...).
*   Hiểu rõ chiến lược giá và các chương trình khuyến mãi.
*   Xác định các xu hướng về cấu hình sản phẩm (RAM, ROM, CPU) đang phổ biến trên thị trường.
*   Tìm ra mối tương quan giữa giá bán, cấu hình và đánh giá của người dùng.
*   Tất cả các phân tích trên nhằm cung cấp một cái nhìn toàn cảnh, dựa trên dữ liệu, để hỗ trợ việc ra quyết định kinh doanh.

**3. Nguồn dữ liệu (Data Source):**
*   **Loại dữ liệu:** Dữ liệu sản phẩm laptop.
*   **Nguồn:** Dữ liệu được thu thập bằng phương pháp cào (web scraping) từ hai trang web lớn: `thegioididong.com` và `cellphones.com.vn`.
*   **Định dạng:** Dữ liệu thô được lưu dưới dạng file `.csv`.
*   **Số lượng:** Hơn 1000 bản ghi (records).
*   **Các thuộc tính chính:** `id`, `product_name`, `current_price`, `list_price`, `brand`, `category`, `cpu`, `ram`, `storage`, `screen_size`, `screen_resolution`, `os`, `software`, `average_rating`, `product_url`.

**4. Đội ngũ & Phân công vai trò (Team & Roles):**
Dự án được thực hiện bởi một nhóm gồm các vai trò chuyên biệt:
*   **Team Hạ tầng & Dữ liệu (Phan Trọng Phú, Phan Trọng Quí):** Chịu trách nhiệm thiết lập môi trường máy chủ (CentOS), cào dữ liệu và thực hiện làm sạch dữ liệu ban đầu.
*   **Big Data Developer (Bạn):** Chịu trách nhiệm chính trong việc xử lý dữ liệu lớn. Viết và thực thi 10 jobs MapReduce bằng Python để xử lý, biến đổi và tổng hợp dữ liệu thô từ HDFS.
*   **Data Analyst (Phạm Văn Thịnh):** Sử dụng Apache Hive và ngôn ngữ HiveQL để truy vấn dữ liệu (cả dữ liệu thô và dữ liệu đã qua MapReduce). Nhiệm vụ là khám phá dữ liệu, tìm kiếm insight và chuẩn bị các bộ dữ liệu tổng hợp cuối cùng.
*   **BI Developer (Nguyễn Văn Quang Duy):** Sử dụng Power BI để kết nối với dữ liệu tổng hợp từ Data Analyst và xây dựng một dashboard trực quan, tương tác. Đồng thời, thiết lập Grafana để giám sát hiệu năng hệ thống.

**5. Công nghệ sử dụng (Technology Stack):**
*   **Lưu trữ phân tán:** HDFS (Hadoop Distributed File System).
*   **Xử lý dữ liệu (Batch Processing):** Apache Hadoop MapReduce (sử dụng Python).
*   **Truy vấn & Kho dữ liệu (Data Warehousing):** Apache Hive (sử dụng HiveQL).
*   **Trực quan hóa dữ liệu (Visualization):** Microsoft Power BI.
*   **Giám sát hệ thống (Monitoring):** Grafana.
*   **Hệ điều hành:** CentOS.
*   **Quản lý mã nguồn:** GitHub.

**6. Luồng xử lý dữ liệu tổng thể (End-to-End Workflow):**
1.  **Thu thập:** Team Hạ tầng cào dữ liệu và tạo ra file `laptops.csv`.
2.  **Lưu trữ thô:** Big Data Developer tải file `laptops.csv` lên HDFS.
3.  **Xử lý & Biến đổi:** Big Data Developer chạy 10 jobs MapReduce để xử lý dữ liệu trên HDFS. Kết quả của mỗi job được lưu vào các thư mục riêng biệt trên HDFS.
4.  **Phân tích & Tổng hợp:** Data Analyst tạo các bảng Hive trỏ đến dữ liệu thô và dữ liệu đã xử lý. Anh ấy viết các câu lệnh HiveQL để phân tích và xuất ra các file CSV tổng hợp, cô đọng.
5.  **Trực quan hóa:** BI Developer import các file CSV tổng hợp vào Power BI và xây dựng dashboard.
6.  **Báo cáo:** Toàn bộ mã nguồn, báo cáo, slide và các sản phẩm khác được lưu trữ trên repository GitHub của nhóm.