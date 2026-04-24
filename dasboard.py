import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analisis Data Bike Sharing – Rafif Nur Kumara",
    page_icon="🚲",
    layout="wide",
)

sns.set(style="whitegrid")

# ── Helper: load data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    day_df  = pd.read_csv(os.path.join(base, "data", "day.csv"))
    hour_df = pd.read_csv(os.path.join(base, "data", "hour.csv"))

    # --- Cleaning ---
    day_df["dteday"]  = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    median_hum = day_df["hum"].median()
    day_df["hum"] = day_df["hum"].replace(0, median_hum)

    season_map   = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map  = {1: "Clear", 2: "Misty/Cloudy", 3: "Light Snow/Rain", 4: "Heavy Rain"}

    day_df["season"]     = day_df["season"].map(season_map)
    day_df["yr"]         = day_df["yr"].map({0: 2011, 1: 2012})
    day_df["weathersit"] = day_df["weathersit"].map(weather_map)

    hour_df["season"] = hour_df["season"].map(season_map)
    hour_df["yr"]     = hour_df["yr"].map({0: 2011, 1: 2012})

    day_df["temp_bin"] = day_df["temp"].round(1)

    return day_df, hour_df

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://img.icons8.com/color/96/bicycle.png", width=80
)
st.sidebar.title("Navigasi")
page = st.sidebar.radio(
    "Pilih halaman:",
    [
        "🏠 Beranda",
        "🔍 Data Wrangling",
        "📊 EDA",
        "📈 Visualisasi & Analisis",
        "✅ Kesimpulan & Rekomendasi",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
**Proyek Analisis Data**  
Bike-sharing Dataset  

👤 Rafif Nur Kumara  
✉️ rafif230805@gmail.com  
🎓 ID Dicoding: CDCC190D6Y0616  
"""
)

# ── Load data (with upload fallback) ─────────────────────────────────────────
data_dir = os.path.join(os.path.dirname(__file__), "data")
data_ready = os.path.isfile(os.path.join(data_dir, "day.csv")) and \
             os.path.isfile(os.path.join(data_dir, "hour.csv"))

if not data_ready:
    st.warning(
        "📂 Dataset belum ditemukan. Silakan upload **day.csv** dan **hour.csv** di bawah ini."
    )
    col1, col2 = st.columns(2)
    with col1:
        up_day = st.file_uploader("Upload day.csv", type="csv")
    with col2:
        up_hour = st.file_uploader("Upload hour.csv", type="csv")

    if up_day and up_hour:
        os.makedirs(data_dir, exist_ok=True)
        with open(os.path.join(data_dir, "day.csv"), "wb") as f:
            f.write(up_day.read())
        with open(os.path.join(data_dir, "hour.csv"), "wb") as f:
            f.write(up_hour.read())
        st.success("Dataset berhasil diupload! Silakan reload halaman.")
        st.stop()
    else:
        st.info(
            "Anda juga bisa menaruh **day.csv** dan **hour.csv** ke folder `data/` "
            "lalu deploy ulang ke Streamlit Cloud."
        )
        st.stop()

day_df, hour_df = load_data()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BERANDA
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Beranda":
    st.title("🚲 Proyek Analisis Data: Bike-sharing Dataset")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Baris (day.csv)",  f"{len(day_df):,}")
    col2.metric("Total Baris (hour.csv)", f"{len(hour_df):,}")
    col3.metric("Periode Data", "2011 – 2012")

    st.markdown("---")
    st.header("📋 Pertanyaan Bisnis")

    with st.expander("Framework SMART Question", expanded=False):
        st.markdown("""
| Elemen | Penjelasan |
|---|---|
| **Specific** | Fokus pada topik tertentu, tidak bermakna ganda |
| **Measurable** | Dapat dijawab dengan angka/metrik konkret |
        | **Action-Oriented** | Memberikan arahan untuk tindakan nyata |
| **Relevant** | Sejalan dengan tujuan bisnis utama |
| **Time-bound** | Memiliki batasan waktu yang jelas |
""")

    st.info(
        "**Pertanyaan 1:** Sejauh mana faktor suhu (*temp*) dan kelembapan (*hum*) dapat "
        "memprediksi total penyewaan sepeda harian selama tahun 2012, dan faktor mana yang "
        "paling signifikan?"
    )
    st.info(
        "**Pertanyaan 2:** Apakah terdapat lonjakan penyewaan yang tidak wajar (anomali) "
        "pada jam-jam tertentu selama hari libur di tahun 2011, dan apakah berkaitan dengan "
        "kondisi cuaca ekstrem?"
    )

    st.markdown("---")
    st.header("🗃️ Pratinjau Dataset")
    tab1, tab2 = st.tabs(["day.csv", "hour.csv"])
    with tab1:
        st.dataframe(day_df.head(10), use_container_width=True)
    with tab2:
        st.dataframe(hour_df.head(10), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DATA WRANGLING
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Data Wrangling":
    st.title("🔍 Data Wrangling")
    st.markdown("---")

    # --- Gathering ---
    st.header("1. Gathering Data")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("day.csv")
        st.write(f"Shape: {day_df.shape}")
        st.dataframe(day_df.dtypes.rename("Dtype").to_frame(), use_container_width=True)
    with col2:
        st.subheader("hour.csv")
        st.write(f"Shape: {hour_df.shape}")
        st.dataframe(hour_df.dtypes.rename("Dtype").to_frame(), use_container_width=True)

    st.markdown("---")

    # --- Assessing ---
    st.header("2. Assessing Data")

    tab1, tab2 = st.tabs(["day_df", "hour_df"])
    with tab1:
        st.subheader("Statistik Deskriptif – day_df")
        st.dataframe(day_df.describe(), use_container_width=True)
        st.metric("Duplikasi", day_df.duplicated().sum())
        st.metric("Missing Values", day_df.isnull().sum().sum())
    with tab2:
        st.subheader("Statistik Deskriptif – hour_df")
        st.dataframe(hour_df.describe(), use_container_width=True)
        st.metric("Duplikasi", hour_df.duplicated().sum())
        st.metric("Missing Values", hour_df.isnull().sum().sum())

    with st.expander("📌 Permasalahan yang Ditemukan"):
        st.markdown("""
1. **Inconsistent Value** – Kolom `dteday` bertipe `object` (string), seharusnya `datetime`.  
2. **Inaccurate Value** – Kolom `hum` di `day_df` memiliki nilai 0 yang tidak logis secara meteorologi.  
3. **Potensi Outlier** – Kolom `cnt` di `hour_df` memiliki lonjakan sangat tinggi pada jam tertentu.
""")

    st.markdown("---")

    # --- Cleaning ---
    st.header("3. Cleaning Data")
    st.markdown("""
- ✅ `dteday` dikonversi ke `datetime` menggunakan `pd.to_datetime()`  
- ✅ Nilai `hum = 0` diganti dengan **median** kelembapan  
- ✅ Kolom kategori (`season`, `yr`, `weathersit`) di-*mapping* ke label deskriptif  
""")
    st.success("Data sudah bersih dan siap untuk analisis lebih lanjut!")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EDA
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 EDA":
    st.title("📊 Exploratory Data Analysis (EDA)")
    st.markdown("---")

    # --- Korelasi ---
    st.header("Matriks Korelasi (day_df)")
    corr = day_df[["temp", "hum", "windspeed", "cnt"]].corr()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    ax.set_title("Korelasi Antar Variabel Numerik")
    st.pyplot(fig)
    plt.close()

    st.markdown("""
**Insight:**
- `temp` berkorelasi **positif kuat** dengan `cnt` → suhu adalah prediktor utama.
- `hum` berkorelasi **negatif lemah** → kelembapan tinggi sedikit menurunkan penyewaan.
- `windspeed` hampir tidak berkorelasi dengan `cnt`.
""")

    st.markdown("---")

    # --- Rata-rata per musim ---
    st.header("Rata-rata Penyewaan per Musim")
    season_stats = day_df.groupby("season")["cnt"].mean().reset_index()
    season_stats.columns = ["Musim", "Rata-rata Penyewaan"]
    season_stats = season_stats.sort_values("Rata-rata Penyewaan", ascending=False)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=season_stats, x="Musim", y="Rata-rata Penyewaan",
                palette="Set2", ax=ax)
    ax.set_title("Rata-rata Total Penyewaan per Musim")
    ax.set_ylabel("Rata-rata cnt")
    st.pyplot(fig)
    plt.close()

    st.markdown("**Insight:** Musim **Fall** memiliki rata-rata penyewaan tertinggi secara konsisten.")

    st.markdown("---")

    # --- Anomali hari libur ---
    st.header("Deteksi Anomali pada Hari Libur")
    holiday_df = hour_df[hour_df["holiday"] == 1]
    Q1 = holiday_df["cnt"].quantile(0.25)
    Q3 = holiday_df["cnt"].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    anomalies = holiday_df[holiday_df["cnt"] > upper_bound]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total data hari libur", len(holiday_df))
    col2.metric("Ambang batas anomali (IQR)", int(upper_bound))
    col3.metric("Jumlah anomali ditemukan", len(anomalies))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: VISUALISASI & ANALISIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Visualisasi & Analisis":
    st.title("📈 Visualisasi & Explanatory Analysis")
    st.markdown("---")

    # ---- Pertanyaan 1 ----
    st.header("Pertanyaan 1: Suhu & Kelembapan vs Penyewaan")

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.regplot(
        x="temp", y="cnt", data=day_df, ax=axes[0],
        scatter_kws={"alpha": 0.3, "color": "skyblue"},
        line_kws={"color": "red"},
    )
    axes[0].set_title("Suhu (Normalized) vs Penyewaan")
    axes[0].set_xlabel("Suhu (Normalized)")
    axes[0].set_ylabel("Total Penyewaan (cnt)")
    axes[0].grid(True, linestyle="--", alpha=0.6)

    sns.regplot(
        x="hum", y="cnt", data=day_df, ax=axes[1],
        scatter_kws={"alpha": 0.3, "color": "lightcoral"},
        line_kws={"color": "darkred"},
    )
    axes[1].set_title("Kelembapan (Normalized) vs Penyewaan")
    axes[1].set_xlabel("Kelembapan (Normalized)")
    axes[1].set_ylabel("Total Penyewaan (cnt)")
    axes[1].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.success(
        "**Analisis:** Garis regresi suhu yang menanjak positif mengonfirmasi bahwa suhu "
        "adalah prediktor utama volume penyewaan. Kelembapan menunjukkan korelasi negatif "
        "yang jauh lebih lemah."
    )

    # Filter tahun untuk Q1
    year_filter = st.selectbox("Filter Tahun", [2011, 2012, "Semua"])
    if year_filter != "Semua":
        filtered = day_df[day_df["yr"] == year_filter]
    else:
        filtered = day_df

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.regplot(
        x="temp", y="cnt", data=filtered, ax=ax2,
        scatter_kws={"alpha": 0.4, "color": "steelblue"},
        line_kws={"color": "crimson"},
    )
    ax2.set_title(f"Suhu vs Penyewaan – {year_filter}")
    ax2.set_xlabel("Suhu (Normalized)")
    ax2.set_ylabel("Total Penyewaan (cnt)")
    ax2.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig2)
    plt.close()

    st.markdown("---")

    # ---- Pertanyaan 2 ----
    st.header("Pertanyaan 2: Deteksi Anomali pada Hari Libur")

    holiday_df = hour_df[hour_df["holiday"] == 1]
    Q1 = holiday_df["cnt"].quantile(0.25)
    Q3 = holiday_df["cnt"].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    hourly_avg  = holiday_df.groupby("hr")["cnt"].mean()

    fig3, ax3 = plt.subplots(figsize=(14, 6))
    sns.scatterplot(
        x="hr", y="cnt", data=holiday_df,
        alpha=0.5, color="steelblue", label="Data Penyewaan", ax=ax3,
    )
    ax3.plot(
        hourly_avg.index, hourly_avg.values,
        color="black", linewidth=2, marker="o", label="Rata-rata Normal",
    )
    ax3.axhline(
        y=upper_bound, color="red", linestyle="--", linewidth=2,
        label=f"Ambang Batas Anomali ({int(upper_bound)})",
    )
    ax3.fill_between(
        range(0, 24), upper_bound, holiday_df["cnt"].max(),
        color="red", alpha=0.1, label="Zona Anomali",
    )
    ax3.set_title("Deteksi Anomali Penyewaan per Jam pada Hari Libur (2011–2012)", fontsize=14)
    ax3.set_xlabel("Jam (0–23)")
    ax3.set_ylabel("Jumlah Penyewaan")
    ax3.set_xticks(range(0, 24))
    ax3.legend(loc="upper left")
    ax3.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig3)
    plt.close()

    st.success(
        "**Analisis:** Lonjakan anomali paling sering terjadi pada pukul 10:00–17:00. "
        "Lonjakan ini tidak terjadi setiap hari libur, mengindikasikan adanya *external events* "
        "seperti festival atau parade kota yang tidak tercatat sebagai variabel eksplisit."
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: KESIMPULAN & REKOMENDASI
# ══════════════════════════════════════════════════════════════════════════════
elif page == "✅ Kesimpulan & Rekomendasi":
    st.title("✅ Kesimpulan & Rekomendasi")
    st.markdown("---")

    st.header("Kesimpulan")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Pertanyaan 1")
        st.markdown("""
Variabel **suhu (temp)** memiliki pengaruh positif yang **signifikan dan kuat** terhadap 
jumlah penyewaan sepeda. Kenaikan suhu (hingga titik optimal) diikuti secara konsisten oleh 
kenaikan jumlah pengguna.

Sebaliknya, **kelembapan (hum)** memiliki pengaruh negatif namun jauh lebih lemah 
dibandingkan suhu.

> 📌 Faktor cuaca termal adalah **prediktor utama** volume permintaan harian.
""")
    with col2:
        st.subheader("Pertanyaan 2")
        st.markdown("""
Terdapat beberapa **lonjakan penyewaan (anomali)** yang sangat ekstrem di luar jam sibuk 
normal (10:00–17:00) pada hari libur.

Lonjakan ini tidak terjadi merata di setiap hari libur, mengindikasikan adanya 
***External Events*** (festival, acara olahraga, parade kota) yang memicu lonjakan 
permintaan mendadak.
""")

    st.markdown("---")
    st.header("Rekomendasi Action Item")

    with st.expander("🌡️ 1. Optimasi Stok Berbasis Cuaca (Predictive Dispatching)"):
        st.markdown("""
Gunakan data prakiraan cuaca (khususnya **suhu**) sebagai basis pengiriman unit sepeda.

Jika suhu esok hari diprediksi meningkat ke level optimal (**0.6–0.7** skala ternormalisasi 
≈ 25–30°C), tim operasional harus:
- Meningkatkan ketersediaan unit di stasiun-stasiun utama **20–30%** lebih banyak dari hari biasanya.
""")

    with st.expander("🎪 2. Manajemen Kapasitas Insidental (Event-Responsive System)"):
        st.markdown("""
- Berkolaborasi dengan pemerintah kota untuk mendapatkan **kalender acara publik**.
- Menyiapkan tim **"Rapid Rebalancing"** yang aktif saat penyewaan melewati ambang batas IQR.
- Memindahkan sepeda dari stasiun penuh ke stasiun kosong secara *real-time*.
""")

    with st.expander("🎁 3. Program Loyalitas pada Kondisi Kurang Optimal"):
        st.markdown("""
Berikan **insentif** (diskon atau poin tambahan) bagi pengguna *registered* yang bersepeda 
saat kondisi cuaca kurang mendukung (kelembapan tinggi / suhu ekstrem) guna menjaga 
stabilitas pendapatan.
""")
