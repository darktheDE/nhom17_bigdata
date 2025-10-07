### **Tổng quan vai trò Big Data Developer**

*   **Nhiệm vụ cốt lõi:** Kiến Hưng là người xây dựng và vận hành "nhà máy chế biến" dữ liệu. Kiến Hưng nhận "nông sản thô" (dữ liệu CSV) và biến nó thành "thực phẩm tinh chế" (dữ liệu đã được tổng hợp, sẵn sàng cho phân tích) bằng công cụ hạng nặng là MapReduce.
*   **Mục tiêu cuối cùng:** Cung cấp 10 bộ dữ liệu đầu ra, mỗi bộ là kết quả của một job MapReduce, được lưu trữ gọn gàng trên HDFS để Data Analyst (anh Thịnh) có thể sử dụng.

---

### **Kế hoạch chi tiết theo từng giai đoạn**

#### **Giai đoạn 1: Nền tảng & Thử nghiệm (Tuần 1)**

Mục tiêu của tuần này là đảm bảo mọi thứ sẵn sàng, từ môi trường, dữ liệu cho đến một job MapReduce "chào sân" để kiểm tra toàn bộ hệ thống.

*   **Bước 1: Thiết lập Môi trường & Nhận dữ liệu**
    *   **Công việc:**
        1.  Phối hợp với team hạ tầng (Phú, Quí) để đảm bảo Kiến Hưng có quyền truy cập vào server CentOS, có thể sử dụng các lệnh `hadoop`, `hdfs`.
        2.  Nhận file dữ liệu **phiên bản đầu tiên** (có thể chỉ là một phần, khoảng 200-300 dòng) từ Quí. Không cần đợi file đầy đủ.
    *   **Mục tiêu:** Sẵn sàng môi trường làm việc và có dữ liệu mẫu để phát triển.
    *   **Sản phẩm/Kết quả:** Kiến Hưng có thể SSH vào server và có file `laptops_sample.csv` trong tay.

*   **Bước 2: Đưa dữ liệu lên HDFS**
    *   **Công việc:**
        1.  Tạo một thư mục làm việc cho nhóm trên HDFS: `hdfs dfs -mkdir -p /user/nhom2/input`
        2.  Tải file dữ liệu mẫu lên thư mục đó: `hdfs dfs -put laptops_sample.csv /user/nhom2/input`
    *   **Mục tiêu:** Dữ liệu đã nằm trên hệ thống file phân tán, sẵn sàng để MapReduce đọc.
    *   **Sản phẩm/Kết quả:** Chạy lệnh `hdfs dfs -ls /user/nhom2/input` thấy file `laptops_sample.csv`.

*   **Bước 3: Viết Job MapReduce "Hello, World!" (Job Thử nghiệm)**
    *   **Công việc:** Viết một job MapReduce đơn giản nhất có thể.
        *   **Ý tưởng:** Đếm số lượng sản phẩm của mỗi thương hiệu (`brand`).
        *   **Mapper.py:** Đọc từng dòng CSV, tách cột `brand`, và output ra `(brand, 1)`.
        *   **Reducer.py:** Nhận input từ mapper, cộng tất cả các số `1` lại cho cùng một `brand`.
    *   **Mục tiêu:** **Quan trọng nhất!** Xác nhận rằng Kiến Hưng có thể chạy một job MapReduce hoàn chỉnh từ đầu đến cuối. Bước này giúp phát hiện sớm mọi vấn đề về môi trường (phiên bản Python, Hadoop Streaming,...).
    *   **Sản phẩm/Kết quả:** Chạy thành công job và thấy kết quả trong thư mục output trên HDFS (ví dụ: `Apple 50`, `Samsung 45`,...).

#### **Giai đoạn 2: Xử lý Lô 1 - Các Job Phân tích Cơ bản (Tuần 2)**

Bây giờ hệ thống đã thông suốt, Kiến Hưng sẽ bắt tay vào các job chính.

*   **Bước 4: Viết và chạy Job 1, 2, 3**
    *   **Công việc:** Lần lượt viết code và thực thi 3 job MapReduce đầu tiên trong danh sách 10 jobs. Đây thường là các job về đếm và phân loại.
        *   **Job 1:** WordCount trên `product_name` (đếm các từ khóa hot).
        *   **Job 2:** Phân loại sản phẩm vào các khoảng giá (giá rẻ, tầm trung, cao cấp).
        *   **Job 3:** Tính tỷ lệ giảm giá trung bình cho mỗi thương hiệu.
    *   **Mục tiêu:** Hoàn thành 3/10 yêu cầu phân tích, tạo ra các kết quả đầu tiên có giá trị.
    *   **Sản phẩm/Kết quả:** 3 thư mục output mới trên HDFS, chứa kết quả của 3 job trên. Code được commit lên GitHub.

*   **Bước 5: Kiểm tra kết quả & Đồng bộ với Data Analyst**
    *   **Công việc:** Dùng lệnh `hdfs dfs -cat /path/to/output/part-00000` để xem kết quả của từng job, đảm bảo nó đúng như mong đợi.
    *   **Mục tiêu:** Đảm bảo chất lượng dữ liệu đầu ra.
    *   **Sản phẩm/Kết quả:** Kiến Hưng tự tin về kết quả và có thể thông báo cho anh Thịnh về cấu trúc của 3 bộ dữ liệu này.

#### **Giai đoạn 3: Xử lý Lô 2 - Các Job Phân tích Nâng cao (Tuần 3)**

Tăng tốc và hoàn thành các job còn lại, thường là các job có logic phức tạp hơn.

*   **Bước 6: Viết và chạy Job 4 đến 10**
    *   **Công việc:** Hoàn thành nốt 7 jobs MapReduce còn lại.
        *   Các job đếm cấu hình (RAM, ROM, CPU).
        *   Job tìm kích thước màn hình phổ biến nhất cho mỗi hãng (logic ở Reducer sẽ phức tạp hơn).
        *   Các job lọc sản phẩm "kỳ lạ" (RAM cao/rating thấp, ROM cao/rating thấp).
    *   **Mục tiêu:** Hoàn thành toàn bộ 10 yêu cầu xử lý dữ liệu.
    *   **Sản phẩm/Kết quả:** 7 thư mục output mới trên HDFS. Toàn bộ 10 jobs được commit đầy đủ lên GitHub.

#### **Giai đoạn 4: Hoàn thiện, Tối ưu và Bàn giao (Tuần 4)**

Giai đoạn cuối cùng, đảm bảo sản phẩm của Kiến Hưng được "đóng gói" và bàn giao một cách chuyên nghiệp.

*   **Bước 7: Tối ưu và Dọn dẹp Code**
    *   **Công việc:**
        1.  Xem lại code của tất cả 10 jobs.
        2.  Thêm comment giải thích các đoạn logic quan trọng.
        3.  Tổ chức lại cấu trúc thư mục code trên GitHub cho gọn gàng, dễ hiểu.
    *   **Mục tiêu:** Mã nguồn sạch sẽ, dễ đọc, dễ chấm điểm và thể hiện sự chuyên nghiệp.
    *   **Sản phẩm/Kết quả:** Repo GitHub được tổ chức tốt.

*   **Bước 8: Viết Tài liệu Bàn giao**
    *   **Công việc:** Tạo một file `README.md` hoặc một tài liệu ngắn gọn. Với mỗi job MapReduce, ghi rõ 3 thông tin:
        1.  **Mô tả:** Job này làm gì? (Vd: "Tính giá bán trung bình cho từng loại CPU").
        2.  **Đường dẫn Output HDFS:** Kết quả của job này nằm ở đâu? (Vd: `/user/nhom2/output/avg_price_by_cpu`).
        3.  **Cấu trúc Output:** Dữ liệu đầu ra có những cột nào, kiểu dữ liệu là gì? (Vd: `cpu (string), avg_price (float)`).
    *   **Mục tiêu:** Giúp anh Thịnh có thể bắt đầu công việc của mình ngay lập tức mà không cần hỏi lại Kiến Hưng.
    *   **Sản phẩm/Kết quả:** Một file tài liệu bàn giao rõ ràng.

*   **Bước 9: Hỗ trợ và Phối hợp**
    *   **Công việc:** Sẵn sàng hỗ trợ anh Thịnh nếu anh ấy gặp vấn đề khi tạo bảng Hive hoặc đọc dữ liệu của Kiến Hưng.
    *   **Mục tiêu:** Đảm bảo luồng công việc của cả nhóm trôi chảy.