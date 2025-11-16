# ============================================================
# Dashboard KPI Karyawan – Streamlit + Plotly
# ============================================================

import pandas as pd
import streamlit as st
import plotly.express as px

# ------------------------------------------------------------
# Streamlit UI Setup
# ------------------------------------------------------------
st.set_page_config(page_title="Dashboard KPI", layout="wide")
st.title("📊 Dashboard KPI Karyawan 2025")
st.markdown("Dashboard interaktif untuk memantau performa KPI karyawan berdasarkan jabatan, cabang, dan waktu.")
st.markdown("---")

# ------------------------------------------------------------
# File Upload Section
# ------------------------------------------------------------
st.sidebar.header("🗂 Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Unggah file Excel KPI (format .xlsx)", type=["xlsx"]
)

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file)
        st.sidebar.success("📁 Data berhasil diupload dan dimuat!")
    except Exception as e:
        st.sidebar.error(f"❌ Terjadi kesalahan saat membaca file: {str(e)}")
        st.stop()
else:
    # Jika tidak ada upload, gunakan file default
    st.sidebar.info("📁 Belum ada file diupload. Menggunakan file default.")
    default_file = "Salin dari REKAPITULASI NILAI KPI 2025(1).xlsx"
    df_raw = pd.read_excel(default_file)

# ------------------------------------------------------------
# Preprocessing Data
# ------------------------------------------------------------
df = df_raw.copy()

# Rename columns sesuai struktur file khas
df.columns = [
    "NO", "NIK", "NAMA", "JABATAN", "CABANG",
    "APRIL", "MEI", "JUNI", "JULI", "AGUSTUS", "SEPT",
    "OKT", "NOV", "DES", "TOTAL_SCORE", "RATING"
]

# Hanya ambil data karyawan yang valid
df = df[df["NAMA"].notna()]

# Konversi kolom nilai menjadi numerik
bulan_cols = ["APRIL", "MEI", "JUNI", "JULI", "AGUSTUS", "SEPT", "OKT", "NOV", "DES"]
for col in bulan_cols + ["TOTAL_SCORE"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["JABATAN"] = df["JABATAN"].astype(str)
df["CABANG"] = df["CABANG"].astype(str)

# ------------------------------------------------------------
# Filter Data Bagian
# ------------------------------------------------------------
st.sidebar.header("🔍 Filter Data")
jabatan_list = ["Semua"] + sorted(df["JABATAN"].unique().tolist())
selected_jabatan = st.sidebar.selectbox("Pilih Jabatan", jabatan_list)

if selected_jabatan != "Semua":
    df = df[df["JABATAN"] == selected_jabatan]

# ------------------------------------------------------------
# Highlight Cards
# ------------------------------------------------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rata-rata Skor", f"{df['TOTAL_SCORE'].mean():.2f}")

with col2:
    st.metric("Total Karyawan", df.shape[0])

with col3:
    top_person = df.loc[df["TOTAL_SCORE"].idxmax(), "NAMA"]
    st.metric("Top Performer", top_person)

# ------------------------------------------------------------
# Visual: Tren Rata-rata Skor Bulanan
# ------------------------------------------------------------
st.markdown("---")
st.subheader("📈 Tren Rata-rata Skor Bulanan")

monthly_avg = df[bulan_cols].mean()
fig_line = px.line(
    x=bulan_cols,
    y=monthly_avg,
    labels={"x": "Bulan", "y": "Rata-rata Skor"},
    markers=True,
    title="Rata-rata Skor KPI per Bulan"
)
st.plotly_chart(fig_line, use_container_width=True)

# ------------------------------------------------------------
# Visual: Bar Chart Rata-rata KPI per Jabatan
# ------------------------------------------------------------
st.subheader("📊 Rata-rata KPI per Jabatan")

jabatan_avg = df.groupby("JABATAN")["TOTAL_SCORE"].mean().reset_index()
fig_bar = px.bar(
    jabatan_avg,
    x="JABATAN",
    y="TOTAL_SCORE",
    text_auto=True,
    title="Rata-rata KPI Berdasarkan Jabatan"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ------------------------------------------------------------
# Visual: Horizontal Bar Chart per Cabang
# ------------------------------------------------------------
st.subheader("🏢 Rata-rata KPI per Cabang")

cabang_avg = df.groupby("CABANG")["TOTAL_SCORE"].mean().reset_index()
fig_hbar = px.bar(
    cabang_avg,
    x="TOTAL_SCORE",
    y="CABANG",
    orientation="h",
    text_auto=True,
    title="Rata-rata KPI Berdasarkan Cabang"
)
st.plotly_chart(fig_hbar, use_container_width=True)

# ------------------------------------------------------------
# Visual: Pie Chart Rating Distribusi
# ------------------------------------------------------------
st.subheader("🟢 Distribusi Rating KPI")

fig_pie = px.pie(
    df,
    names="RATING",
    title="Persentase Rating KPI",
    hole=0.4
)
st.plotly_chart(fig_pie, use_container_width=True)

# ------------------------------------------------------------
# Data Table Interaktif
# ------------------------------------------------------------
st.subheader("📄 Data Karyawan (Interaktif)")
st.dataframe(df)

# ------------------------------------------------------------
# End of Dashboard
# ------------------------------------------------------------
