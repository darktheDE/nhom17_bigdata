from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("Top 5 Highest Discounts") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_df = spark.read.option("header", "true").csv("data/raw/tgdd_raw_data.csv")
laptops_df = laptops_df.withColumn("current_price", col("current_price").cast("float")) \
                       .withColumn("list_price", col("list_price").cast("float"))

# Lọc bỏ các dòng có giá NULL hoặc list_price = 0 để tránh division by zero
laptops_df = laptops_df.filter((col("list_price").isNotNull()) & 
                               (col("current_price").isNotNull()) & 
                               (col("list_price") > 0))

# Tính tỷ lệ giảm giá
laptops_df = laptops_df.withColumn("discount_rate", 
                                   (col("list_price") - col("current_price")) / col("list_price"))

# Lấy top 5 sản phẩm giảm giá cao nhất
top5_laptops = laptops_df.orderBy(col("discount_rate").desc()).limit(5)

print("=== Top 5 Laptops Highest Discounts ===")
top5_laptops.show(truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job05_top5_highest_discounts_laptops"
top5_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job05_top5_highest_discounts_tgdd")

# -------------------------------
# 3. Xử lý Cellphones
# -------------------------------
# HDFS path: "/raw_data/products_csv/cellphones_raw_data.csv"
cellphones_df = spark.read.option("header", "true").csv("data/raw/cellphones_raw_data.csv")
cellphones_df = cellphones_df.withColumn("current_price", 
                                         regexp_replace(col("current_price_raw"), "[.đ]", "").cast("float")) \
                             .withColumn("list_price", 
                                         regexp_replace(col("list_price_raw"), "[.đ]", "").cast("float"))

# Lọc bỏ các dòng có giá NULL hoặc list_price = 0 để tránh division by zero
cellphones_df = cellphones_df.filter((col("list_price").isNotNull()) & 
                                     (col("current_price").isNotNull()) & 
                                     (col("list_price") > 0))

# Tính tỷ lệ giảm giá
cellphones_df = cellphones_df.withColumn("discount_rate", 
                                         (col("list_price") - col("current_price")) / col("list_price"))

# Lấy top 5 sản phẩm giảm giá cao nhất
top5_cellphones = cellphones_df.orderBy(col("discount_rate").desc()).limit(5)

print("=== Top 5 Cellphones Highest Discounts ===")
top5_cellphones.show(truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job05_top5_highest_discounts_cellphones"
top5_cellphones.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job05_top5_highest_discounts_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

