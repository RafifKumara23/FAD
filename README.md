# 🚲 Analisis Data Bike Sharing

Proyek analisis data dataset bike-sharing oleh **Rafif Nur Kumara** untuk kelas Dicoding.

## Pertanyaan Bisnis
Pertanyaan 1: Sejauh mana faktor suhu (temp) dan kelembapan (hum) dapat memprediksi total jumlah penyewaan sepeda harian selama tahun 2012, dan faktor manakah yang memiliki pengaruh paling signifikan?
Pertanyaan 2: Apakah terdapat lonjakan jumlah penyewaan sepeda yang tidak wajar (anomali) pada jam-jam tertentu selama periode hari libur (holiday) di tahun 2011, dan apakah lonjakan tersebut berkaitan dengan kondisi cuaca yang ekstrem?

## Cara Menjalankan Lokal

```bash
pip install -r requirements.txt

# Taruh day.csv dan hour.csv ke folder data/
mkdir data
cp /path/ke/day.csv data/
cp /path/ke/hour.csv data/

streamlit run app.py
```

## Deploy ke Streamlit Cloud

1. Push repo ini ke GitHub (pastikan `data/` ada di `.gitignore`).
2. Buka [share.streamlit.io](https://share.streamlit.io) → **New app** → pilih repo & branch.
3. Set **Main file path** ke `dashboard.py`.
4. Klik **Deploy**.
5. Setelah app berjalan, upload `day.csv` dan `hour.csv` langsung lewat antarmuka app.

