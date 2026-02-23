from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder \
    .appName("CyberMasterPipeline_Final") \
    .config("spark.jars", "postgresql-42.7.2.jar") \
    .getOrCreate()

# 1. Load Dataset
path = "data/"
incidents = spark.read.csv(f"{path}incidents_master.csv", header=True, inferSchema=True)
financial = spark.read.csv(f"{path}financial_impact.csv", header=True, inferSchema=True)
market = spark.read.csv(f"{path}market_impact.csv", header=True, inferSchema=True)

# 2. Buat Mapping Industri (Agar Dashboard tidak Error)
industry_data = [
    ("53", "Real Estate & Leasing"), ("55", "Management of Companies"),
    ("61", "Educational Services"), ("62", "Health Care"),
    ("92", "Public Administration"), ("22", "Utilities"),
    ("51", "Information/Tech"), ("52", "Finance & Insurance"),
    ("44-45", "Retail Trade"), ("31-33", "Manufacturing")
]
mapping_df = spark.createDataFrame(industry_data, ["code", "industry_name"])

# 3. Join & Cleaning
financial_clean = financial.drop("notes", "created_at", "updated_at")
market_clean = market.drop("stock_ticker", "notes", "created_at", "updated_at")

# Gabungkan 3 file + Mapping Industri
integrated_df = incidents.join(financial_clean, "incident_id", "left") \
                         .join(market_clean, "incident_id", "left") \
                         .join(mapping_df, incidents.industry_primary == mapping_df.code, "left")

# 4. Final Transformation (Severity & Handle NULL)
final_df = integrated_df.withColumn("impact_severity", 
    when(col("total_loss_usd") > 1000000, "Critical")
    .when(col("total_loss_usd") > 500000, "High")
    .otherwise("Medium")
).fillna("Other Industries", subset=["industry_name"]) \
 .fillna(0, subset=["total_loss_usd", "abnormal_return_1d"])

# 5. Kirim ke Database
db_properties = {"user": "rafdi_admin", "password": "Aryaguna2022", "driver": "org.postgresql.Driver"}
final_df.write.jdbc("jdbc:postgresql://localhost:5432/cyber_db", "gold_all_impacts", "overwrite", db_properties)

print("[SUCCESS] Pipeline Final Berhasil: Data Terintegrasi + Nama Industri Sudah Ada!")
spark.stop()