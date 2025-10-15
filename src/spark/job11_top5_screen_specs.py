from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, split, regexp_extract

# -------------------------------
# 1. Khởi tạo SparkSession
# -------------------------------
spark = SparkSession.builder \
    .appName("Top 5 Screen Specs") \
    .getOrCreate()

# -------------------------------
# 2. Xử lý Laptops
# -------------------------------
# HDFS path: "/raw_data/products_csv/laptops_enriched_data.csv"
laptops_df = spark.read.option("header", "true").csv("data/raw/tgdd_raw_data.csv")

# Đếm số lượng theo screen_size và screen_resolution
screen_laptops = laptops_df.groupBy("screen_size", "screen_resolution") \
                           .agg(count("*").alias("product_count")) \
                           .orderBy("product_count", ascending=False) \
                           .limit(5)

print("=== Top 5 Screen Specs - Laptops ===")
screen_laptops.show(truncate=False)

# Lưu local
# HDFS output: "/processed_data/job11_top5_screen_laptops"
screen_laptops.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job11_top5_screen_tgdd")

# -------------------------------
# 3. Xử lý Cellphones
# -------------------------------
# HDFS path: "/raw_data/products_csv/cellphones_raw_data.csv"
cellphones_df = spark.read.option("header", "true").csv("data/raw/cellphones_raw_data.csv")

# Tách screen size & resolution từ raw_specs_string sử dụng regex
# Định dạng thường là: "CPU/RAM/STORAGE/VGA/SCREEN_SIZE RESOLUTION/OS/..."
# Screen size: dạng "15.6", "13.3", "16.0" (số thập phân + inch)
# Screen resolution: FHD, WUXGA, QHD, UHD, etc.
cellphones_specs = cellphones_df.withColumn("screen_size", 
    regexp_extract(col("raw_specs_string"), r"(\d+\.\d+)", 1)
)
cellphones_specs = cellphones_specs.withColumn("screen_resolution", 
    regexp_extract(col("raw_specs_string"), r"(FHD|WUXGA|QHD|UHD|OLED|Full HD|4K|\d+\s*[xX]\s*\d+)", 1)
)

# Đếm số lượng sản phẩm
screen_cellphones = cellphones_specs.groupBy("screen_size", "screen_resolution") \
                                    .agg(count("*").alias("product_count")) \
                                    .orderBy("product_count", ascending=False) \
                                    .limit(5)

print("=== Top 5 Screen Specs - Cellphones ===")
screen_cellphones.show(truncate=False)

# Lưu local
# HDFS output: "/processed_data/job11_top5_screen_cellphones"
screen_cellphones.write.mode("overwrite").option("header", "true") \
    .csv("data/processed_for_bi/job11_top5_screen_cellphones")

# -------------------------------
# 4. Kết thúc SparkSession
# -------------------------------
spark.stop()

