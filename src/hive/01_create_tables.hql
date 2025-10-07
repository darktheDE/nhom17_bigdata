-- Tạo database cho dự án
CREATE DATABASE IF NOT EXISTS mobile_analytics;

USE mobile_analytics;

-- Tạo bảng dữ liệu thô laptop từ HDFS
CREATE EXTERNAL TABLE IF NOT EXISTS raw_laptops (
    id INT,
    product_name STRING,
    current_price DECIMAL(12,0),
    list_price DECIMAL(12,0),
    brand STRING,
    category STRING,
    cpu STRING,
    ram STRING,
    storage STRING,
    screen_size STRING,
    screen_resolution STRING,
    os STRING,
    software STRING,
    average_rating DECIMAL(2,1),
    product_url STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/bigdata/laptops/raw/'
TBLPROPERTIES ("skip.header.line.count"="1");

-- Tạo bảng kết quả từ MapReduce Job 01
CREATE EXTERNAL TABLE IF NOT EXISTS brand_counts (
    brand STRING,
    product_count INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/user/bigdata/laptops/output/job01_brand_count/';

-- Tạo bảng kết quả từ MapReduce Job 02
CREATE EXTERNAL TABLE IF NOT EXISTS keyword_counts (
    keyword STRING,
    frequency INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/user/bigdata/laptops/output/job02_word_count/';

-- Kiểm tra dữ liệu
SELECT 'Tổng số laptop:' as metric, COUNT(*) as value FROM raw_laptops
UNION ALL
SELECT 'Tổng số thương hiệu:' as metric, COUNT(DISTINCT brand) as value FROM raw_laptops
UNION ALL
SELECT 'Giá trung bình:' as metric, ROUND(AVG(current_price), 0) as value FROM raw_laptops;
