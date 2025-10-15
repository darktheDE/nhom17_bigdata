from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("Top 5 Rated Products") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_df = spark.read.option("header", "true").csv("data/raw/tgdd_raw_data.csv")
laptops_df = laptops_df.withColumn("average_rating", col("average_rating").cast("float"))

# Lấy top 5 sản phẩm đánh giá cao nhất
top5_laptops = laptops_df.orderBy(col("average_rating").desc()).limit(5)

print("=== Top 5 Laptops by Average Rating ===")
top5_laptops.show(truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job09_top5_rated_laptops"
top5_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job09_top5_rated_tgdd")

# -------------------------------
# 3. Xử lý Cellphones
# -------------------------------
cellphones_df = spark.read.option("header", "true").csv("/raw_data/products_csv/cellphones_raw_data.csv")

# Giả sử cột rating chưa có, hoặc nếu muốn có thể lấy từ một cột khác, hiện tại tạm thời bỏ qua
# Nếu cellphones không có cột rating, bạn có thể tạo 1 cột rating giả để test:
# cellphones_df = cellphones_df.withColumn("average_rating", col("some_rating_column").cast("float"))

# Lấy top 5 (nếu có average_rating)
# cellphones_df = cellphones_df.withColumn("average_rating", col("average_rating").cast("float"))
# top5_cellphones = cellphones_df.orderBy(col("average_rating").desc()).limit(5)

# print("=== Top 5 Cellphones by Average Rating ===")
# top5_cellphones.show(truncate=False)

# Lưu HDFS (nếu có)
# top5_cellphones.write.mode("overwrite").option("header", "true") \
#     .csv("/processed_data/job09_top5_rated_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

