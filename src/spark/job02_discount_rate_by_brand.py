from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, regexp_replace, split

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("Discount Rate by Brand - Laptops and Cellphones") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý TGDD Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_path = "data/raw/tgdd_raw_data.csv"
laptops_df = spark.read.option("header", "true").csv(laptops_path)

# Chuyển giá sang float
laptops_df = laptops_df.withColumn("current_price", col("current_price").cast("float")) \
                       .withColumn("list_price", col("list_price").cast("float"))

# Lọc bỏ các dòng có giá NULL hoặc list_price = 0 để tránh division by zero
laptops_df = laptops_df.filter((col("list_price").isNotNull()) & 
                               (col("current_price").isNotNull()) & 
                               (col("list_price") > 0))

# Tính tỷ lệ giảm giá
laptops_df = laptops_df.withColumn("discount_rate", 
                                   (col("list_price") - col("current_price")) / col("list_price"))

# Tính tỷ lệ giảm giá trung bình theo brand
avg_discount_laptops = laptops_df.groupBy("brand") \
                                 .agg(avg("discount_rate").alias("avg_discount_rate")) \
                                 .orderBy("avg_discount_rate", ascending=False)

print("=== Average Discount Rate per Brand - TGDD Laptops ===")
avg_discount_laptops.show(truncate=False)

# Lưu kết quả ra local
# HDFS output path: "/processed_data/job02_discount_rate_laptops"
avg_discount_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job02_discount_rate_tgdd")

# -------------------------------
# 3. Xử lý CellphoneS
# -------------------------------
# HDFS path: "/raw_data/products_csv/cellphones_raw_data.csv"
cellphones_path = "data/raw/cellphones_raw_data.csv"
cellphones_df = spark.read.option("header", "true").csv(cellphones_path)

# Chuẩn hóa giá
cellphones_df = cellphones_df.withColumn("current_price", 
                                         regexp_replace(col("current_price_raw"), "[.đ]", "").cast("float")) \
                             .withColumn("list_price", 
                                         regexp_replace(col("list_price_raw"), "[.đ]", "").cast("float"))

# Tách brand từ product_name
# Nếu từ đầu tiên là "Laptop" thì lấy từ thứ 2, ngược lại lấy từ đầu (bao gồm MacBook)
from pyspark.sql.functions import when, lower
cellphones_df = cellphones_df.withColumn("first_word", split(col("product_name"), " ").getItem(0))
cellphones_df = cellphones_df.withColumn("brand", 
    when(lower(col("first_word")) == "laptop", split(col("product_name"), " ").getItem(1))
    .otherwise(col("first_word"))
).drop("first_word")

# Lọc bỏ các dòng có giá NULL hoặc list_price = 0 để tránh division by zero
cellphones_df = cellphones_df.filter((col("list_price").isNotNull()) & 
                                     (col("current_price").isNotNull()) & 
                                     (col("list_price") > 0))

# Tính tỷ lệ giảm giá
cellphones_df = cellphones_df.withColumn("discount_rate", 
                                         (col("list_price") - col("current_price")) / col("list_price"))

# Tính tỷ lệ giảm giá trung bình theo brand
avg_discount_cellphones = cellphones_df.groupBy("brand") \
                                      .agg(avg("discount_rate").alias("avg_discount_rate")) \
                                      .orderBy("avg_discount_rate", ascending=False)

print("=== Average Discount Rate per Brand - CellphoneS ===")
avg_discount_cellphones.show(truncate=False)

# Lưu kết quả ra local
# HDFS output path: "/processed_data/job02_discount_rate_cellphones"
avg_discount_cellphones.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job02_discount_rate_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

