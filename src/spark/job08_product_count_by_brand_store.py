from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, count

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("Product Count by Brand and Store") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_df = spark.read.option("header", "true").csv("data/raw/tgdd_raw_data.csv")

# Giả sử store_name = brand nếu không có cột store
laptops_df = laptops_df.withColumn("store_name", col("brand"))

# Đếm số sản phẩm theo (brand, store)
count_laptops = laptops_df.groupBy("brand", "store_name").agg(count("*").alias("product_count")) \
                          .orderBy("product_count", ascending=False)

print("=== Product Count by Brand & Store - Laptops ===")
count_laptops.show(10, truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job08_product_count_laptops"
count_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job08_product_count_tgdd")

# -------------------------------
# 3. Xử lý Cellphones
# -------------------------------
# HDFS path: "/raw_data/products_csv/cellphones_raw_data.csv"
cellphones_df = spark.read.option("header", "true").csv("data/raw/cellphones_raw_data.csv")

# Tách brand từ product_name
# Nếu từ đầu tiên là "Laptop" thì lấy từ thứ 2, ngược lại lấy từ đầu (bao gồm MacBook)
from pyspark.sql.functions import when, lower
cellphones_df = cellphones_df.withColumn("first_word", split(col("product_name"), " ").getItem(0))
cellphones_df = cellphones_df.withColumn("brand", 
    when(lower(col("first_word")) == "laptop", split(col("product_name"), " ").getItem(1))
    .otherwise(col("first_word"))
)

# Store name = brand (vì CellphoneS không có cột store riêng)
cellphones_df = cellphones_df.withColumn("store_name", col("brand")).drop("first_word")

# Đếm sản phẩm theo (brand, store)
count_cellphones = cellphones_df.groupBy("brand", "store_name").agg(count("*").alias("product_count")) \
                                .orderBy("product_count", ascending=False)

print("=== Product Count by Brand & Store - Cellphones ===")
count_cellphones.show(10, truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job08_product_count_cellphones"
count_cellphones.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job08_product_count_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

