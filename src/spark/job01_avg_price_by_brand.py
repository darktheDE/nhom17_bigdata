from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, regexp_replace, split

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("Average Price by Brand - Laptops and Cellphones") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_path = "data/raw/tgdd_raw_data.csv"
laptops_df = spark.read.option("header", "true").csv(laptops_path)

# Chuyển current_price sang float
laptops_df = laptops_df.withColumn("current_price", col("current_price").cast("float"))

# Tính giá trung bình theo brand
avg_price_laptops = laptops_df.groupBy("brand") \
    .agg(avg("current_price").alias("avg_price")) \
    .orderBy("avg_price", ascending=False)

print("=== Average Price per Brand - Laptops ===")
avg_price_laptops.show(truncate=False)

# Lưu kết quả ra local
# HDFS output: "/processed_data/avg_price_laptops"
avg_price_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job01_avg_price_tgdd")

# -------------------------------
# 3. Xử lý Cellphones
# -------------------------------
# HDFS path: "/raw_data/products_csv/cellphones_raw_data.csv"
cellphones_path = "data/raw/cellphones_raw_data.csv"
cellphones_df = spark.read.option("header", "true").csv(cellphones_path)

# Chuẩn hóa giá: loại bỏ "." và "đ", convert sang float
cellphones_df = cellphones_df.withColumn("current_price", 
                                         regexp_replace(col("current_price_raw"), "[.đ]", "").cast("float"))

# Tách thương hiệu từ product_name 
# Nếu từ đầu tiên là "Laptop" thì lấy từ thứ 2, ngược lại lấy từ đầu (bao gồm MacBook)
from pyspark.sql.functions import when, lower
cellphones_df = cellphones_df.withColumn("first_word", split(col("product_name"), " ").getItem(0))
cellphones_df = cellphones_df.withColumn("brand", 
    when(lower(col("first_word")) == "laptop", split(col("product_name"), " ").getItem(1))
    .otherwise(col("first_word"))
).drop("first_word")

# Tính giá trung bình theo brand
avg_price_cellphones = cellphones_df.groupBy("brand") \
    .agg(avg("current_price").alias("avg_price")) \
    .orderBy("avg_price", ascending=False)

print("=== Average Price per Brand - Cellphones ===")
avg_price_cellphones.show(truncate=False)

# Lưu kết quả ra local
# HDFS output: "/processed_data/avg_price_cellphones"
avg_price_cellphones.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job01_avg_price_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

