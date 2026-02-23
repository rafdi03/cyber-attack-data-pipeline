from pyspark.sql import SparkSession

# Inisialisasi Spark
spark = SparkSession.builder.appName("VerifyResults").getOrCreate()

# Load data Parquet yang tadi disimpan
path_parquet = "data/processed_cyber_report"
df_hasil = spark.read.parquet(path_parquet)

# Tampilkan skema dan 10 data teratas
print("\n=== VERIFIKASI DATA PARQUET ===")
df_hasil.printSchema()
df_hasil.show(10)

# Hitung jumlah baris untuk memastikan data tidak hilang
print(f"Total baris data: {df_hasil.count()}")

spark.stop()