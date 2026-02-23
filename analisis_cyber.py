from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, round, when

# 1. Inisialisasi Spark
spark = SparkSession.builder \
    .appName("CyberAttackFinalAnalysis") \
    .getOrCreate()

# 2. Load Dataset Utama
path_data = "data/incidents_master.csv"
df = spark.read.csv(path_data, header=True, inferSchema=True)

industry_data = [
    ("53", "Real Estate & Leasing"),
    ("55", "Management of Comapanies"),
    ("61", "Educational Services"),
    ("62", "Healthcare & Social Assistance"),
    ("92", "Public Administration"),
    ("22", "Utilities"),
    ("51", "Information/Technology"),
    ("52", "Finance & Insurance"),
    ("44-45", "Retail Trade"),
    ("31-33", "Manufacturing")
]

schema = ["code", "industry_name"]
mapping_df = spark.createDataFrame(industry_data, schema)


enriched_df = df.join(mapping_df, df.industry_primary == mapping_df.code, "left") 

final_df = enriched_df.withColumn(
    "industry_name", 
    when(col("industry_name").isNull(), "Other Industries").otherwise(col("industry_name"))
)

print("\n=== ANALISIS DOWNTIME BERDASARKAN NAMA INDUSTRI ===")
final_df.groupBy("industry_name") \
    .agg(round(avg("downtime_hours"), 2).alias("avg_downtime")) \
    .orderBy(col("avg_downtime").desc()) \
    .show()
print("\n[DEBUG] Kode Industri yang belum terdaftar di kamus:")
enriched_df.filter(col("industry_name").isNull()) \
    .select("industry_primary") \
    .distinct() \
    .show()

# Simpan hasil akhir yang sudah bersih ke folder 'processed'
print("\n[INFO] Menyimpan data ke format Parquet...")
final_df.write.mode("overwrite").parquet("data/processed_cyber_report")

spark.stop()