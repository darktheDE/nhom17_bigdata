-- Cấu hình: Thiết lập số lượng job song song
SET default_parallel 5;

-- Thiết lập encoding là UTF-8 để xử lý ký tự Tiếng Việt
SET default_charset utf-8;

-- BẮT BUỘC: Đăng ký và định nghĩa Piggybank UDFs
REGISTER /opt/pig/lib/piggybank.jar;
-- Hàm này sẽ được dùng để tách chuỗi số hợp lệ từ chuỗi giá Cellphones
DEFINE REGEX_EXTRACT org.apache.pig.piggybank.evaluation.string.RegexExtract; 

-----------------------------------------------------------------
-- 1. Xử lý Dữ liệu CellphoneS (LÀM SẠCH GIÁ VÀ CHUYỂN ĐỔI KIỂU DỮ LIỆU)
-----------------------------------------------------------------

-- LOAD từ Local File System (Đường dẫn cần tồn tại trên máy local)
CELLPHONES_DATA = LOAD 'file:///home/phu/raw_data/products_csv/cellphones_raw_data.csv' 
    USING org.apache.pig.piggybank.storage.CSVExcelStorage()
    AS (id:chararray, product_name:chararray, current_price_raw:chararray, list_price_raw:chararray, raw_specs:chararray, url:chararray);

-- Lọc dòng Header
CELLPHONES_FILTERED = FILTER CELLPHONES_DATA BY NOT (id == 'id' AND product_name == 'product_name');

-- LÀM SẠCH VÀ CHUYỂN ĐỔI KIỂU DỮ LIỆU
CELLPHONES_CLEANED = FOREACH CELLPHONES_FILTERED {
    -- 1. Tách chuỗi số (bao gồm dấu chấm) khỏi đơn vị tiền tệ và chữ cái (ví dụ: '22.990.000đ' -> '22.990.000')
    -- Biểu thức chính quy: '([0-9\.]+)' lấy ra chuỗi số và dấu chấm.
    price_cur_str = REGEX_EXTRACT(current_price_raw, '([0-9\\.]+)', 1);
    price_list_str = REGEX_EXTRACT(list_price_raw, '([0-9\\.]+)', 1);

    -- 2. Loại bỏ dấu chấm phân cách hàng nghìn (ví dụ: '22.990.000' -> '22990000')
    price_cur_clean = REPLACE(price_cur_str, '\\.', '');
    price_list_clean = REPLACE(price_list_str, '\\.', '');

    GENERATE
        (long)id AS id,
        product_name,
        -- Chuyển đổi sang double. Nếu chuỗi không hợp lệ, Pig sẽ đặt là NULL.
        (double)price_cur_clean AS current_price,
        (double)price_list_clean AS list_price,
        'cellphones' AS source_brand;
};

-----------------------------------------------------------------
-- 2. Xử lý Dữ liệu TGDD (LOAD từ LOCAL)
-----------------------------------------------------------------

-- LOAD từ Local File System (Giá đã là số hợp lệ)
TGDD_DATA = LOAD 'file:///home/phu/raw_data/products_csv/laptops_enriched_data.csv' 
    USING org.apache.pig.piggybank.storage.CSVExcelStorage() 
    AS (id:chararray, product_name:chararray, current_price:double, list_price:double, brand:chararray, category:chararray, cpu:chararray, ram:chararray, storage:chararray, screen_size:chararray, screen_resolution:chararray, os:chararray, software:chararray, average_rating:float, product_url:chararray); 

-- Lọc dòng Header
TGDD_FILTERED = FILTER TGDD_DATA BY NOT (id == 'id' AND product_name == 'product_name');

-- Chuẩn hóa: giữ nguyên các cột cần thiết (Giá đã là double)
TGDD_CLEANED = FOREACH TGDD_FILTERED GENERATE
    (long)id AS id,
    product_name,
    current_price,
    list_price,    
    'thegioididong' AS source_brand;


-----------------------------------------------------------------
-- 3. Hợp nhất Dữ liệu và Lưu Tạm
-----------------------------------------------------------------

-- Hợp nhất hai bộ dữ liệu (UNION) với Schema thống nhất: (long, chararray, double, double, chararray)
ALL_DATA_FOR_MYSQL = UNION CELLPHONES_CLEANED, TGDD_CLEANED;

-- Lưu dữ liệu. NullStorage('\N') sẽ xử lý các giá trị NULL thành '\N', phù hợp cho MySQL.
STORE ALL_DATA_FOR_MYSQL 
    INTO 'output/mysql_export_temp_fixed' 
    USING PigStorage(',', 'NullStorage(\'\\\N\')');
