Tentu, ini adalah draf README.md yang sangat detail dan profesional, dirancang khusus untuk menonjolkan kemampuan teknis kamu sebagai Data Engineer sekaligus pemahaman analitis kamu terhadap data bisnis. Dokumen ini sangat cocok untuk dipamerkan kepada recruiter di perusahaan besar seperti Astra atau FMCG.

🛡️ Cyber Attack Financial & Market Impact Pipeline
End-to-End Data Engineering & Business Intelligence Suite
📌 Gambaran Umum Proyek
Proyek ini mengintegrasikan data terstruktur mengenai serangan siber global utama antara tahun 2021 dan 2025. Fokus utama adalah pada kerugian finansial dan reaksi pasar saham pasca-insiden. Pipeline ini mengubah data mentah menjadi wawasan bisnis yang siap dianalisis untuk mendukung pengambilan keputusan strategis dalam manajemen risiko siber.

Tujuan utama dari proyek ini adalah membangun portofolio yang membuktikan kompetensi dalam mengelola siklus hidup data (Data Lifecycle) dari hulu ke hilir dalam waktu singkat.

🏗️ Arsitektur Data (Medallion Architecture)
Sistem ini menggunakan pendekatan Medallion Architecture untuk menjamin integritas dan kualitas data di setiap tahapannya:

Bronze Layer (Raw):

Data mentah dikumpulkan dari 3 sumber utama: incidents_master.csv, financial_impact.csv, dan market_impact.csv.

Berisi 850+ insiden siber terdokumentasi dengan metrik mentah yang belum terolah.

Silver Layer (Cleansing & Integration):

Pemrosesan menggunakan Apache Spark untuk menangani skalabilitas.

Melakukan Multi-Join antar dataset menggunakan incident_id sebagai Primary Key.

Penanganan duplikasi kolom (stock_ticker, notes) dan standarisasi tipe data.

Penyimpanan ke format Parquet untuk kompresi maksimal dan efisiensi query.

Gold Layer (Business Ready):

Data Enrichment: Melakukan pemetaan (mapping) kode industri menjadi nama sektor yang ramah bisnis.

Business Logic: Penerapan aturan klasifikasi tingkat keparahan (Severity Tiering) otomatis.

Pemuatan data ke PostgreSQL sebagai Serving Layer yang aman dan terstruktur.

🧠 Analisis Teknis: Tantangan "Fat-Tailed Distribution"
Proyek ini mengadopsi pendekatan Severity Classification (Tiering) daripada regresi linier sederhana. Keputusan arsitektur ini diambil berdasarkan karakteristik struktural data kerugian siber:

Masalah Distribusi: Data kerugian finansial memiliki sifat Fat-Tailed (distribusi miring ke kanan secara ekstrem). Segelintir insiden "Black Swan" memiliki dampak ribuan kali lebih besar dari rata-rata, sehingga model regresi tradisional cenderung mengalami overfitting.

Low Signal-to-Noise Ratio: Fitur profil perusahaan seringkali tidak berkorelasi langsung dengan nilai kerugian pasti karena variabel eksternal (kualitas respon insiden, asuransi, sentimen publik).

Solusi: Dengan mengklasifikasikan kerugian ke dalam kategori (Medium, High, Critical), sistem memberikan informasi yang lebih stabil dan berguna bagi manajemen untuk memprioritaskan anggaran keamanan siber.

📊 Fitur Dashboard (Streamlit & Plotly)
Dashboard interaktif ini dirancang untuk memberikan wawasan cepat bagi eksekutif maupun analisis mendalam bagi analis risiko:

Executive KPIs: Menampilkan Total Kerugian ($55B+), rata-rata downtime, dan dampak pasar secara real-time dari database.

Global Attack Map: Visualisasi distribusi serangan berdasarkan lokasi kantor pusat perusahaan.

Correlation Plot: Analisis hubungan antara jam downtime dengan besaran kerugian finansial.

Time-Series Trend: Melacak frekuensi serangan dari bulan ke bulan untuk melihat pola musiman.

Sector Slicing: Filter dinamis untuk membedah data per industri (misalnya: Manufacturing, Finance, atau Information Technology).

🛠️ Tech Stack
Language: Python 3.10+.

Big Data Engine: Apache Spark (PySpark).

Database: PostgreSQL.

Visualization: Streamlit, Plotly, & Pandas.

Environment: Linux Ubuntu (WSL2) & Zsh.

⚙️ Cara Menjalankan
Pastikan PostgreSQL sudah terinstal dan database cyber_db telah dibuat.

Install dependensi: pip install pyspark streamlit pandas sqlalchemy psycopg2-binary plotly.

Jalankan pipeline pengolahan data:

Bash
spark-submit --jars postgresql-42.7.2.jar gold_pipeline.py
Buka dashboard:

Bash
streamlit run app.py
Author: Rafdi