-- ========================================================
-- File: 03_platform_comparison_analysis.hql
-- Mô tả: Phân tích so sánh giữa 2 sàn thương mại (TGDD vs CellphoneS)
-- Tác giả: Phạm Văn Thịnh - Data Analyst
-- Ngày: 2025-10-07
-- ========================================================

-- --------------------------------------------------------
-- QUERY 1: So sánh giá bán trung bình theo thương hiệu trên 2 sàn
-- Mục đích: Tìm hiểu sàn nào có giá rẻ hơn cho từng thương hiệu
-- --------------------------------------------------------

SELECT 
    brand,
    source_website,
    ROUND(AVG(current_price), 0) AS avg_price,
    COUNT(*) AS product_count,
    ROUND(MIN(current_price), 0) AS min_price,
    ROUND(MAX(current_price), 0) AS max_price
FROM raw_laptops
WHERE brand IS NOT NULL 
    AND source_website IS NOT NULL
    AND current_price > 0
GROUP BY brand, source_website
ORDER BY brand, source_website;

-- --------------------------------------------------------
-- QUERY 2: So sánh tỷ lệ giảm giá trung bình giữa 2 sàn
-- Mục đích: Sàn nào có chương trình khuyến mãi hấp dẫn hơn?
-- --------------------------------------------------------

SELECT 
    source_website,
    ROUND(AVG(((list_price - current_price) / list_price) * 100), 2) AS avg_discount_percent,
    COUNT(*) AS products_with_discount,
    ROUND(MIN(((list_price - current_price) / list_price) * 100), 2) AS min_discount,
    ROUND(MAX(((list_price - current_price) / list_price) * 100), 2) AS max_discount
FROM raw_laptops
WHERE list_price > current_price
    AND list_price > 0
    AND source_website IS NOT NULL
GROUP BY source_website
ORDER BY avg_discount_percent DESC;

-- --------------------------------------------------------
-- QUERY 3: Phân tích danh mục sản phẩm - Đa dạng thương hiệu
-- Mục đích: Sàn nào có nhiều thương hiệu hơn?
-- --------------------------------------------------------

SELECT 
    source_website,
    COUNT(DISTINCT brand) AS unique_brands,
    COUNT(*) AS total_products,
    ROUND(COUNT(*) / COUNT(DISTINCT brand), 1) AS avg_products_per_brand
FROM raw_laptops
WHERE source_website IS NOT NULL
    AND brand IS NOT NULL
GROUP BY source_website
ORDER BY unique_brands DESC;

-- --------------------------------------------------------
-- QUERY 4: Top 5 thương hiệu có giá chênh lệch lớn nhất giữa 2 sàn
-- Mục đích: Phát hiện cơ hội kinh doanh
-- --------------------------------------------------------

WITH brand_prices AS (
    SELECT 
        brand,
        source_website,
        AVG(current_price) AS avg_price
    FROM raw_laptops
    WHERE brand IS NOT NULL 
        AND source_website IS NOT NULL
        AND current_price > 0
    GROUP BY brand, source_website
),
price_comparison AS (
    SELECT 
        t1.brand,
        t1.avg_price AS tgdd_price,
        t2.avg_price AS cellphones_price,
        ABS(t1.avg_price - t2.avg_price) AS price_diff,
        ROUND(((t1.avg_price - t2.avg_price) / t1.avg_price) * 100, 2) AS price_diff_percent
    FROM 
        (SELECT brand, avg_price FROM brand_prices WHERE source_website = 'thegioididong') t1
    INNER JOIN 
        (SELECT brand, avg_price FROM brand_prices WHERE source_website = 'cellphones') t2
    ON t1.brand = t2.brand
)
SELECT *
FROM price_comparison
ORDER BY price_diff DESC
LIMIT 5;

-- --------------------------------------------------------
-- QUERY 5: Phân tích phân khúc giá theo sàn
-- Mục đích: Sàn nào tập trung vào phân khúc nào?
-- --------------------------------------------------------

SELECT 
    source_website,
    CASE 
        WHEN current_price < 15000000 THEN 'Budget (< 15M)'
        WHEN current_price >= 15000000 AND current_price < 25000000 THEN 'Mid-range (15-25M)'
        WHEN current_price >= 25000000 AND current_price < 35000000 THEN 'Premium (25-35M)'
        ELSE 'High-end (>= 35M)'
    END AS price_segment,
    COUNT(*) AS product_count,
    ROUND(AVG(current_price), 0) AS avg_price,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY source_website), 2) AS percent_of_platform
FROM raw_laptops
WHERE current_price > 0
    AND source_website IS NOT NULL
GROUP BY 
    source_website,
    CASE 
        WHEN current_price < 15000000 THEN 'Budget (< 15M)'
        WHEN current_price >= 15000000 AND current_price < 25000000 THEN 'Mid-range (15-25M)'
        WHEN current_price >= 25000000 AND current_price < 35000000 THEN 'Premium (25-35M)'
        ELSE 'High-end (>= 35M)'
    END
ORDER BY source_website, 
    CASE 
        WHEN current_price < 15000000 THEN 1
        WHEN current_price >= 15000000 AND current_price < 25000000 THEN 2
        WHEN current_price >= 25000000 AND current_price < 35000000 THEN 3
        ELSE 4
    END;

-- --------------------------------------------------------
-- QUERY 6: Thương hiệu độc quyền (chỉ có trên 1 sàn)
-- Mục đích: Tìm sản phẩm độc quyền
-- --------------------------------------------------------

WITH brand_platform_count AS (
    SELECT 
        brand,
        COUNT(DISTINCT source_website) AS platform_count,
        MAX(source_website) AS exclusive_platform
    FROM raw_laptops
    WHERE brand IS NOT NULL 
        AND source_website IS NOT NULL
    GROUP BY brand
)
SELECT 
    brand,
    exclusive_platform,
    COUNT(*) AS product_count
FROM raw_laptops
WHERE brand IN (
    SELECT brand 
    FROM brand_platform_count 
    WHERE platform_count = 1
)
GROUP BY brand, source_website
ORDER BY product_count DESC;

-- --------------------------------------------------------
-- QUERY 7: So sánh rating trung bình theo sàn
-- Mục đích: Sàn nào có sản phẩm được đánh giá cao hơn?
-- --------------------------------------------------------

SELECT 
    source_website,
    ROUND(AVG(average_rating), 2) AS avg_rating,
    COUNT(*) AS total_products,
    SUM(CASE WHEN average_rating >= 4.5 THEN 1 ELSE 0 END) AS products_high_rating,
    ROUND(SUM(CASE WHEN average_rating >= 4.5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS percent_high_rating
FROM raw_laptops
WHERE average_rating > 0
    AND source_website IS NOT NULL
GROUP BY source_website
ORDER BY avg_rating DESC;

-- --------------------------------------------------------
-- QUERY 8: Xuất dữ liệu để Power BI sử dụng
-- Tạo bảng tổng hợp cho BI Developer
-- --------------------------------------------------------

-- Tạo bảng kết quả so sánh giá
CREATE TABLE IF NOT EXISTS platform_price_comparison AS
SELECT 
    brand,
    source_website,
    ROUND(AVG(current_price), 0) AS avg_price,
    COUNT(*) AS product_count
FROM raw_laptops
WHERE brand IS NOT NULL 
    AND source_website IS NOT NULL
    AND current_price > 0
GROUP BY brand, source_website;

-- Tạo bảng kết quả so sánh khuyến mãi
CREATE TABLE IF NOT EXISTS platform_discount_comparison AS
SELECT 
    source_website,
    brand,
    ROUND(AVG(((list_price - current_price) / list_price) * 100), 2) AS avg_discount_percent,
    COUNT(*) AS product_count
FROM raw_laptops
WHERE list_price > current_price
    AND list_price > 0
    AND source_website IS NOT NULL
    AND brand IS NOT NULL
GROUP BY source_website, brand;

-- ========================================================
-- KẾT THÚC FILE QUERY SO SÁNH PLATFORM
-- ========================================================
