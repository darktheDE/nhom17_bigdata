from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, split, count, regexp_extract, when

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("RAM and Storage Distribution") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_df = spark.read.option("header", "true").csv("data/raw/tgdd_raw_data.csv")

# Chuẩn hóa RAM & Storage (loại bỏ ký tự GB)
laptops_df = laptops_df.withColumn("ram_clean", regexp_replace(col("ram"), "[^0-9]", "").cast("int"))
laptops_df = laptops_df.withColumn("storage_clean", regexp_replace(col("storage"), "[^0-9]", "").cast("int"))

# Đếm số lượng sản phẩm theo RAM & Storage
ram_storage_laptops = laptops_df.groupBy("ram_clean", "storage_clean") \
                                .agg(count("*").alias("product_count")) \
                                .orderBy("product_count", ascending=False)

print("=== RAM & Storage Distribution - Laptops ===")
ram_storage_laptops.show(10, truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job10_ram_storage_laptops"
ram_storage_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job10_ram_storage_tgdd")

# -------------------------------
# 3. Xử lý Cellphones
# -------------------------------
# HDFS path: "/raw_data/products_csv/cellphones_raw_data.csv"
cellphones_df = spark.read.option("header", "true").csv("data/raw/cellphones_raw_data.csv")

# Tách RAM/Storage từ raw_specs_string (định dạng: CPU/RAM/STORAGE/...)
# Sử dụng regex để trích xuất chính xác giá trị RAM và Storage
from pyspark.sql.functions import regexp_extract
cellphones_specs = cellphones_df.withColumn("ram", regexp_extract(col("raw_specs_string"), r"(\d+)GB", 1)) \
                                .withColumn("storage", regexp_extract(col("raw_specs_string"), r"(\d+)GB.*?(\d+)(GB|TB)", 2))

# Chuyển đổi TB sang GB nếu cần
cellphones_specs = cellphones_specs.withColumn("storage_unit", regexp_extract(col("raw_specs_string"), r"(\d+)(GB|TB)", 2))
cellphones_specs = cellphones_specs.withColumn("storage_clean", 
    when(col("storage_unit") == "TB", col("storage").cast("int") * 1024)
    .otherwise(col("storage").cast("int"))
)

cellphones_specs = cellphones_specs.withColumn("ram_clean", col("ram").cast("int")).drop("storage_unit", "storage", "ram")

# Đếm số lượng sản phẩm theo RAM & Storage
ram_storage_cellphones = cellphones_specs.groupBy("ram_clean", "storage_clean") \
                                        .agg(count("*").alias("product_count")) \
                                        .orderBy("product_count", ascending=False)

print("=== RAM & Storage Distribution - Cellphones ===")
ram_storage_cellphones.show(10, truncate=False)

# Lưu ra local
# HDFS output: "/processed_data/job10_ram_storage_cellphones"
ram_storage_cellphones.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job10_ram_storage_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

