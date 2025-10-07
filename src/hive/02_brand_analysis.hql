-- Phân tích thương hiệu laptop
USE mobile_analytics;

-- 1. Market Share theo thương hiệu
SELECT 
    brand,
    COUNT(*) as product_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM raw_laptops), 2) as market_share_percent,
    ROUND(AVG(current_price), 0) as avg_price,
    ROUND(AVG(average_rating), 1) as avg_rating
FROM raw_laptops
WHERE brand IS NOT NULL AND brand != 'N/A'
GROUP BY brand
ORDER BY product_count DESC;

-- 2. Top 5 thương hiệu có giá trung bình cao nhất
SELECT 
    brand,
    ROUND(AVG(current_price), 0) as avg_price,
    ROUND(MIN(current_price), 0) as min_price,
    ROUND(MAX(current_price), 0) as max_price,
    COUNT(*) as product_count
FROM raw_laptops
WHERE brand IS NOT NULL AND brand != 'N/A'
GROUP BY brand
HAVING COUNT(*) >= 5
ORDER BY avg_price DESC
LIMIT 5;

-- 3. Thương hiệu có đánh giá cao nhất
SELECT 
    brand,
    ROUND(AVG(average_rating), 2) as avg_rating,
    COUNT(*) as product_count,
    ROUND(AVG(current_price), 0) as avg_price
FROM raw_laptops
WHERE brand IS NOT NULL 
    AND brand != 'N/A'
    AND average_rating IS NOT NULL
    AND average_rating > 0
GROUP BY brand
HAVING COUNT(*) >= 3
ORDER BY avg_rating DESC, product_count DESC
LIMIT 10;

-- 4. Xuất kết quả ra file CSV cho Power BI
INSERT OVERWRITE LOCAL DIRECTORY '/tmp/brand_market_share'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT 
    brand,
    COUNT(*) as product_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM raw_laptops), 2) as market_share_percent,
    ROUND(AVG(current_price), 0) as avg_price,
    ROUND(MIN(current_price), 0) as min_price,
    ROUND(MAX(current_price), 0) as max_price,
    ROUND(AVG(average_rating), 1) as avg_rating
FROM raw_laptops
WHERE brand IS NOT NULL AND brand != 'N/A'
GROUP BY brand
ORDER BY product_count DESC;
