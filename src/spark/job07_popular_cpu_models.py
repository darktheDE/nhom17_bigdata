from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, regexp_replace, split, explode, count

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("Popular CPU Models") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_df = spark.read.option("header", "true").csv("data/raw/tgdd_raw_data.csv")

# Chuẩn hóa CPU (lowercase, remove space)
laptops_df = laptops_df.withColumn("cpu_clean", lower(regexp_replace(col("cpu"), "\\s+", "")))

# Đếm số lượng sản phẩm theo cpu
cpu_count_laptops = laptops_df.groupBy("cpu_clean").agg(count("*").alias("count")).orderBy("count", ascending=False)

print("=== Top CPU Models - Laptops ===")
cpu_count_laptops.show(10, truncate=False)  # Hiển thị top 10 CPU

# Lưu ra local
# HDFS output: "/processed_data/job07_popular_cpu_laptops"
cpu_count_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job07_popular_cpu_tgdd")

# -------------------------------
# 3. Xử lý Cellphones
# -------------------------------
# HDFS path: "/raw_data/products_csv/cellphones_raw_data.csv"
cellphones_df = spark.read.option("header", "true").csv("data/raw/cellphones_raw_data.csv")

# Tách CPU từ raw_specs_string (giả sử CPU nằm ở đầu chuỗi, cách "/" hoặc space)
cellphones_cpu_df = cellphones_df.withColumn("cpu_clean", split(col("raw_specs_string"), "/").getItem(0))
cellphones_cpu_df = cellphones_cpu_df.withColumn("cpu_clean", lower(regexp_replace(col("cpu_clean"), "\\s+", "")))

# Đếm số lượng sản phẩm theo CPU
cpu_count_cellphones = cellphones_cpu_df.groupBy("cpu_clean").agg(count("*").alias("count")).orderBy("count", ascending=False)

print("=== Top CPU Models - Cellphones ===")
cpu_count_cellphones.show(10, truncate=False)  # Hiển thị top 10

# Lưu ra local
# HDFS output: "/processed_data/job07_popular_cpu_cellphones"
cpu_count_cellphones.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job07_popular_cpu_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

