### **Tổng quan vai trò BI Developer (Duy)**

*   **Nhiệm vụ cốt lõi:** Quang Duy là người kể chuyện bằng hình ảnh (Visual Storyteller). Quang Duy nhận các bộ dữ liệu đã được phân tích và tổng hợp, sau đó sử dụng các công cụ BI (Power BI, Grafana) để "vẽ" nên một bức tranh toàn cảnh về thị trường laptop, giúp người xem (giảng viên) nắm bắt được những insight quan trọng nhất chỉ qua vài cú click chuột.
*   **Mục tiêu cuối cùng:**
    1.  Xây dựng một dashboard Power BI tương tác, thẩm mỹ và đầy đủ chức năng, trả lời trực quan các câu hỏi kinh doanh.
    2.  Thiết lập một dashboard Grafana để giám sát hiệu năng hệ thống, thể hiện năng lực kỹ thuật của nhóm.

---

### **Kế hoạch chi tiết theo từng giai đoạn**

#### **Giai đoạn 1: Lên ý tưởng & Chuẩn bị (Tuần 1)**

Mục tiêu của tuần này là phác thảo ý tưởng cho dashboard và chuẩn bị sẵn sàng công cụ, không cần đợi dữ liệu cuối cùng.

*   **Bước 1: Cài đặt và làm quen Công cụ**
    *   **Công việc:**
        1.  **Power BI:** Cài đặt Power BI Desktop (miễn phí) trên máy tính cá nhân. Xem qua một vài video hướng dẫn cơ bản về cách import dữ liệu, tạo biểu đồ và thêm slicer.
        2.  **Grafana:** Phối hợp với team hạ tầng (Phú, Quí) để cài đặt Grafana trên server. Tìm hiểu cách tạo một dashboard đơn giản và kết nối với nguồn dữ liệu (ví dụ: Prometheus, nếu nhóm cài đặt).
    *   **Mục tiêu:** Nắm vững các công cụ sẽ sử dụng.

*   **Bước 2: Phác thảo Dashboard trên giấy (Wireframing)**
    *   **Công việc:** Dựa trên danh sách các câu hỏi kinh doanh, lấy một tờ giấy và bút, phác thảo bố cục của dashboard.
        *   **Dashboard sẽ có mấy trang?** (Gợi ý: 3 trang là hợp lý: 1-Tổng quan, 2-Phân tích giá & Thương hiệu, 3-Phân tích cấu hình).
        *   **Mỗi trang sẽ có những biểu đồ gì?** (Ví dụ: Trang tổng quan có biểu đồ tròn thị phần, bảng top 10 rating,...).
        *   **Bộ lọc (Slicer) sẽ đặt ở đâu?** (Thường là bên trái hoặc phía trên).
    *   **Mục tiêu:** Có một "bản thiết kế" rõ ràng trước khi bắt tay vào code. Điều này giúp tiết kiệm rất nhiều thời gian sau này.

#### **Giai đoạn 2: Xây dựng Dashboard Lô 1 (Tuần 2)**

Tuần này Quang Duy sẽ nhận những dữ liệu đầu tiên từ anh Thịnh và bắt đầu hiện thực hóa bản thiết kế.

*   **Bước 3: Tiếp nhận và Import Dữ liệu Lô 1**
    *   **Công việc:** Nhận các file CSV đầu tiên từ anh Thịnh (ví dụ: thị phần, top rating, phân khúc giá). Import chúng vào Power BI.
    *   **Mục tiêu:** Dữ liệu đã sẵn sàng trong Power BI.

*   **Bước 4: Xây dựng Trang Tổng quan & Trang Phân tích Thương hiệu**
    *   **Công việc:** Dựa trên bản phác thảo, tạo các biểu đồ đầu tiên.
        *   Biểu đồ tròn (Pie Chart) cho thị phần thương hiệu.
        *   Biểu đồ cột (Bar Chart) cho phân khúc giá của từng hãng.
        *   Bảng (Table) cho top 10 sản phẩm rating cao.
        *   Thêm các Slicer quan trọng: Lọc theo `Brand`, lọc theo `Sàn` (TGDD/CellphoneS).
    *   **Mục tiêu:** Hoàn thành 50-60% dashboard. Có một sản phẩm demo ban đầu để cả nhóm xem và góp ý.

*   **Bước 5: Thiết lập Dashboard Grafana cơ bản**
    *   **Công việc:** Tạo một dashboard trên Grafana hiển thị các chỉ số cơ bản của cluster Hadoop.
        *   CPU Usage (Tổng và từng Node).
        *   Memory Usage (Tổng và từng Node).
        *   Disk I/O.
    *   **Mục tiêu:** Hoàn thành yêu cầu kỹ thuật phụ, sẵn sàng để "trình diễn" trong video demo.

#### **Giai đoạn 3: Hoàn thiện Dashboard & Tinh chỉnh (Tuần 3)**

Tuần này Quang Duy sẽ nhận nốt phần dữ liệu còn lại và tập trung vào việc làm cho dashboard trở nên hoàn hảo.

*   **Bước 6: Tiếp nhận và Import Dữ liệu Lô 2**
    *   **Công việc:** Nhận các file CSV còn lại từ anh Thịnh (kết quả phân tích cấu hình, các sản phẩm "kỳ lạ",...). Import và liên kết (tạo relationship) chúng với các bảng dữ liệu đã có trong Power BI nếu cần.
    *   **Mục tiêu:** Toàn bộ dữ liệu đã nằm trong Power BI.

*   **Bước 7: Xây dựng Trang Phân tích Cấu hình**
    *   **Công việc:** Hoàn thiện nốt các biểu đồ còn lại.
        *   Biểu đồ nhiệt (Heatmap) cho phân bổ RAM/ROM.
        *   Biểu đồ phân tán (Scatter Plot) cho mối quan hệ Giá vs Rating.
        *   Đám mây từ (Word Cloud) cho các từ khóa hot trong tên sản phẩm.
    *   **Mục tiêu:** Dashboard đã hoàn thiện 100% về mặt chức năng.

*   **Bước 8: Tinh chỉnh Thẩm mỹ và Trải nghiệm Người dùng (UX)**
    *   **Công việc:** Đây là bước biến một dashboard "tốt" thành "xuất sắc".
        *   **Màu sắc:** Chọn một bộ màu chủ đạo, đồng nhất cho tất cả các biểu đồ.
        *   **Tiêu đề & Nhãn:** Đặt lại tên cho các biểu đồ và các trục để người xem dễ hiểu (ví dụ: "Thị phần các thương hiệu" thay vì "count of id by brand").
        *   **Căn chỉnh:** Sắp xếp các biểu đồ ngay ngắn, thẳng hàng.
    *   **Mục tiêu:** Dashboard trông chuyên nghiệp, sạch sẽ và dễ nhìn.

#### **Giai đoạn 4: Đóng gói & Trình bày (Tuần 4)**

Giai đoạn cuối cùng để chuẩn bị cho việc báo cáo.

*   **Bước 9: Ghi lại Tương tác Dashboard**
    *   **Công việc:** Sử dụng một phần mềm quay màn hình (OBS, Camtasia,...), tự mình thao tác trên dashboard Power BI.
        *   Lần lượt click vào các Slicer (chọn Apple, rồi chọn Samsung) để cho thấy các biểu đồ thay đổi theo.
        *   Di chuột (hover) vào một cột dữ liệu để cho thấy thông tin chi tiết hiện ra.
    *   **Mục tiêu:** Tạo ra một video ngắn (1-2 phút) để gửi cho người làm video tổng của nhóm, hoặc để trình chiếu trực tiếp khi báo cáo.

*   **Bước 10: Chụp ảnh màn hình chất lượng cao**
    *   **Công việc:** Chụp lại ảnh của từng trang dashboard Power BI và dashboard Grafana.
    *   **Mục tiêu:** Cung cấp hình ảnh trực quan để đưa vào file báo cáo Word và slide PowerPoint.

*   **Bước 11: Chuẩn bị cho phần Trình bày**
    *   **Công việc:** Chuẩn bị sẵn lời thuyết trình cho phần của mình. Quang Duy không chỉ nói "Đây là biểu đồ X", mà hãy kể câu chuyện đằng sau nó: "Nhìn vào biểu đồ này, chúng ta có thể thấy rằng..."
    *   **Mục tiêu:** Sẵn sàng trình bày một cách tự tin và thuyết phục trong buổi báo cáo cuối kỳ.
