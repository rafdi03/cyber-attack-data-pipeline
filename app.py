import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Pro Cyber Suite", layout="wide")

# 1. Load Data
@st.cache_data
def load_data():
    engine = create_engine('postgresql://rafdi_admin:Aryaguna2022@localhost:5432/cyber_db')
    df = pd.read_sql("SELECT * FROM gold_all_impacts", engine)
    df['incident_date'] = pd.to_datetime(df['incident_date'])
    return df

df = load_data()

# --- SIDEBAR FILTER (Ini Kuncinya) ---
st.sidebar.header("🎛️ Control Panel")
all_industries = sorted(df['industry_name'].unique().tolist())
selected_industries = st.sidebar.multiselect(
    "Pilih Sektor Industri:",
    options=all_industries,
    default=all_industries  # Defaultnya pilih semua agar data muncul di awal
)

# Filter dataframe berdasarkan pilihan di sidebar
filtered_df = df[df['industry_name'].isin(selected_industries)]

# --- HEADER & KPI SECTION ---
st.title("🛡️ Cyber Attack Sector-Specific Analytics")

# Metrik sekarang akan berubah otomatis saat filter diubah
c1, c2, c3, c4 = st.columns(4)
c1.metric("Insiden Terpilih", f"{len(filtered_df):,}")
c2.metric("Total Loss (USD)", f"${(filtered_df['total_loss_usd'].sum() / 1e6):.2f}M")
c3.metric("Avg Downtime", f"{filtered_df['downtime_hours'].mean():.1f} Jam")
c4.metric("Market Impact", f"{filtered_df['abnormal_return_1d'].mean():.4f}%")

st.divider()

# --- TAB VIEW ---
tab1, tab2, tab3, tab4 = st.tabs(["🌐 Global Distribution", "📈 Trends & Correlation", "📋 Raw Data", "🧠 Technical Deep Dive"])

with tab1:
    st.subheader("Perbandingan Downtime per Sektor")
    # Grafik ini sekarang hanya menampilkan sektor yang dipilih
    fig_bar = px.bar(filtered_df.groupby("industry_name")["downtime_hours"].mean().reset_index(),
                     x="industry_name", y="downtime_hours", color="industry_name",
                     title="Rata-rata Downtime per Sektor Terpilih")
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Tren Serangan")
        df_trend = filtered_df.set_index('incident_date').resample('M').size().reset_index(name='count')
        st.line_chart(df_trend.set_index('incident_date'))
    
    with col_b:
        st.subheader("Korelasi Downtime vs Loss")
        fig_scatter = px.scatter(filtered_df, x="downtime_hours", y="total_loss_usd", 
                                 color="industry_name", hover_data=['company_name'])
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Master Data Table")
    st.dataframe(df, use_container_width=True)

with tab4:
    st.header("Technical Methodology & Data Challenges")
    
    st.info("""
    **Executive Summary:** Proyek ini tidak menggunakan model regresi linier sederhana untuk memprediksi nilai kerugian. 
    Berdasarkan analisis distribusi, data kerugian finansial siber memiliki sifat *Fat-Tailed*, 
    sehingga pendekatan **Severity Classification** jauh lebih akurat untuk pengambilan keputusan bisnis.
    """)

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("1. Fat-Tailed Distribution")
        st.write("""
        Target distribusi kerugian (`total_loss_usd`) memiliki *extreme right-skew*. 
        Artinya, sebagian besar insiden memiliki kerugian kecil, namun ada segelintir insiden 'Catastrophic' 
        yang nilainya ribuan kali lipat lebih besar. 
        """)
        st.warning("Strategi: Menggunakan log-transformation dan Tiering Classification.")

    with col_b:
        st.subheader("2. Low Signal-to-Noise Ratio")
        st.write("""
        Fitur profil perusahaan (pendapatan, jumlah karyawan) menjelaskan *siapa* yang diserang, 
        tapi tidak selalu berkorelasi langsung dengan *berapa besar* kerugiannya. 
        Outcome finansial sangat bergantung pada kualitas respons insiden yang bersifat eksternal.
        """)

    st.divider()
    
    st.subheader("🛠️ Solusi Arsitektur yang Diterapkan")
    st.success("""
    **Mengapa Menggunakan Severity Tiering?**
    Daripada memprediksi angka pasti yang memiliki varians ekstrem, sistem ini mengelompokkan risiko ke dalam 
    tier (Medium, High, Critical). Hal ini memberikan nilai praktis bagi manajemen risiko di perusahaan (seperti FMCG atau Otomotif) 
    untuk memprioritaskan alokasi anggaran keamanan siber.
    """)

st.sidebar.success(f"Menampilkan {len(filtered_df)} dari {len(df)} total data.")