# 🚲 Analisis Data Bike Sharing

Proyek analisis data dataset bike-sharing 
menganalisis data penyewaan sepeda dari sistem Capital Bikeshare di Washington D.C. (2011–2012). Analisis dilakukan untuk menjawab pertanyaan bisnis terkait pengaruh musim/cuaca dan pola penyewaan per jam.

## Pertanyaan Bisnis
- Pertanyaan 1: Sejauh mana faktor suhu (temp) dan kelembapan (hum) dapat memprediksi total jumlah penyewaan sepeda harian selama tahun 2012, dan faktor manakah yang memiliki pengaruh paling signifikan?
- Pertanyaan 2: Apakah terdapat lonjakan jumlah penyewaan sepeda yang tidak wajar (anomali) pada jam-jam tertentu selama periode hari libur (holiday) di tahun 2011, dan apakah lonjakan tersebut berkaitan dengan kondisi cuaca yang ekstrem?

## Struktur Direktori
```
submission/
├── dashboard/
│   ├── day_df.csv        

│   ├── hour_df.csv      
│   └── dashboard.py        
├── data/
│   ├── day.csv              
│   └── hour.csv             
├── Rafif_Proyek_Analisis_Data.ipynb  
├── README.md                
├── requirements.txt         
└── url.txt                  
```

## Setup Environment

### Menggunakan pip
```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```


