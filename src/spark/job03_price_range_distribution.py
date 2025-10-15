from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count
from pyspark.sql.functions import regexp_replace, split

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("Price Range Distribution - Laptops and Cellphones") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_df = spark.read.option("header", "true").csv("data/raw/tgdd_raw_data.csv")
laptops_df = laptops_df.withColumn("current_price", col("current_price").cast("float"))

# Tạo cột price_range
laptops_df = laptops_df.withColumn("price_range", 
    when(col("current_price") < 5000000, "<5M")
   .when((col("current_price") >= 5000000) & (col("current_price") < 10000000), "5-10M")
   .when((col("current_price") >= 10000000) & (col("current_price") < 15000000), "10-15M")
   .when((col("current_price") >= 15000000) & (col("current_price") < 20000000), "15-20M")
   .otherwise(">20M")
)

# Đếm số lượng theo price_range
price_distribution_laptops = laptops_df.groupBy("price_range").agg(count("*").alias("count")).orderBy("price_range")
print("=== Laptops Price Range Distribution ===")
price_distribution_laptops.show(truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job03_price_range_laptops"
price_distribution_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job03_price_range_tgdd")

# -------------------------------
# 3. Xử lý Cellphones
# -------------------------------
# HDFS path: "/raw_data/products_csv/cellphones_raw_data.csv"
cellphones_df = spark.read.option("header", "true").csv("data/raw/cellphones_raw_data.csv")
cellphones_df = cellphones_df.withColumn("current_price", 
    regexp_replace(col("current_price_raw"), "[.đ]", "").cast("float"))

# Tạo cột price_range
cellphones_df = cellphones_df.withColumn("price_range", 
    when(col("current_price") < 5000000, "<5M")
   .when((col("current_price") >= 5000000) & (col("current_price") < 10000000), "5-10M")
   .when((col("current_price") >= 10000000) & (col("current_price") < 15000000), "10-15M")
   .when((col("current_price") >= 15000000) & (col("current_price") < 20000000), "15-20M")
   .otherwise(">20M")
)

# Đếm số lượng theo price_range
price_distribution_cellphones = cellphones_df.groupBy("price_range").agg(count("*").alias("count")).orderBy("price_range")
print("=== Cellphones Price Range Distribution ===")
price_distribution_cellphones.show(truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job03_price_range_cellphones"
price_distribution_cellphones.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job03_price_range_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

