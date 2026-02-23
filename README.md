# 🛡️ Cyber-Financial Resilience & Market Dynamics Pipeline

### *Distributed Data Engineering Suite: From Raw Ingestion to Executive Intelligence*

## 🌐 Project Overview

This enterprise-grade pipeline orchestrates the ingestion, transformation, and visualization of global cyber-attack data (2021-2025). Processing over **$55B** in cumulative financial impact, the system utilizes a **Medallion Architecture** to convert high-variance raw signals into structured, business-ready intelligence.

The core objective is to bridge the gap between **Security Telemetry** and **Corporate Finance**, providing stakeholders with a granular view of sectoral risk and market volatility.

## 🏗️ Technical Architecture: The Medallion Model

The pipeline is engineered for horizontal scalability and data integrity, leveraging the distributed computing power of **Apache Spark**.

### 1. 🟤 Bronze Layer (Ingestion)

* **Source:** Multi-source CSV ingestion (Incidents Master, Financial Impact, Market Impact).
* **Mechanism:** Automated schema inference with Spark’s CSV reader.

### 2. 🥈 Silver Layer (Integration & Cleansing)

* **Distributed Joins:** Implemented a multi-stage **Left Join** on `incident_id` across three disparate datasets.
* **Schema Hygiene:** Systematic resolution of **Ambiguous Column Conflicts** (e.g., `stock_ticker`, `notes`, `created_at`) through targeted drops and aliasing to ensure downstream RDBMS compatibility.
* **Storage:** Data is persisted in **Parquet** format, utilizing columnar storage for 10x faster query performance compared to row-based formats.

### 3. 🥇 Gold Layer (Enrichment & Business Logic)

* **Data Enrichment:** Dynamic industry mapping from NAICS-based codes to functional business sectors (e.g., "51"  "Information/Tech").
* **Serving Layer:** Automated synchronization with **PostgreSQL** via JDBC, establishing a centralized *Source of Truth* for business consumers.

## 🧠 Statistical Deep Dive: The "Fat-Tailed" Challenge

Predicting cyber-loss is structurally difficult. This project rejects naive linear regression in favor of **Tiered Classification**, addressing the following mathematical realities:

* **Extreme Skewness:** Financial loss data exhibits a **Fat-Tailed** distribution. A standard Mean Squared Error (MSE) loss function would be dominated by rare "Black Swan" events, leading to poor generalization.
* **The Logic:** We implement a **Severity Tiering Algorithm** defined as:


* **Outcome:** By pivoting from regression to ordinal classification, the pipeline provides a stable, actionable risk framework for decision-makers.

## 📊 Analytics & Executive Control Plane

The frontend is a high-performance **Streamlit** application designed for "Slicing and Dicing" data at scale:

* **Geospatial Intelligence:** Interactive **Choropleth Maps** identifying global threat concentrations.
* **Market Volatility Analysis:** Tracking the **1-Day Abnormal Return** of public companies post-disclosure.
* **Operational Metrics:** Real-time correlation analysis between **Downtime Hours** and **Total Financial Loss**.

## 🛠️ Performance Tech Stack

* **Engine:** Apache Spark 3.5.0 (PySpark).
* **Database:** PostgreSQL (Serving Layer).
* **Frontend:** Streamlit & Plotly Express.
* **Environment:** Linux (WSL2) with Zsh Optimization.

## 🚀 How to Deploy

1. **Initialize Database:** Ensure a PostgreSQL instance is running with `cyber_db` initialized.
2. **Dependencies:** `pip install pyspark streamlit pandas sqlalchemy psycopg2-binary plotly`.
3. **Execute Pipeline:** ```zsh
spark-submit --jars postgresql-42.7.2.jar gold_pipeline.py

4. **Boot Dashboard:**
```zsh
streamlit run app.py

```

<img width="1916" height="948" alt="image" src="https://github.com/user-attachments/assets/258fad05-9c49-478e-bc29-ee8040e6f474" />


---

**Developer Profile:** **Rafdi** | Data Engineer 2026 🎯
*Focused on architecting resilient data systems for high-stakes financial environments.*

---

