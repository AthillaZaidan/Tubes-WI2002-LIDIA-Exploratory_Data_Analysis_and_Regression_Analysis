
# 📊 Tugas Besar Literasi Data dan Intelegensi Artifisial  

# Authors
| Nama                           | NIM      |
| ------------------------------ | -------- |
| Kevin Wirya Valerian           | 13524019 |
| Stevanus Agustaf Wongso        | 13524020 |
| Bryan Pratama Putra Hendra     | 13524067 |
| Athilla Zaidan Zidna Fann      | 13524068 |
| Philipp Hamara                 | 13524101 |
---

## 📁 Struktur Folder

```
Tubes/
│
├── docs/                     # Dokumen laporan dan visualisasi
│   ├── WI2002_LaporanTB_K32-4.pdf
│   └── visualisasi/
│
├── src/                      # Source code proyek
│   ├── file/                 # Data mentah dan hasil cleansing
│   └── python/               # Script Python analisis
│       ├── games_datacleansing.py
│       ├── googleplaystore_datacleansing.py
│       ├── Statistik_Deskriptif_Google_Play_Store.py
│       ├── Korelasi_Google_Play_Store.py
│       ├── Regresi_Linear_Harga_dan_Jumlah-Install.py
│       ├── Regresi_Linear_Rating_dan_Jumlah-Install.py
│       ├── Regresi_Linear_Wishlist_dan_Rating.py
│       └── Parsing_Data_Games.py
│
└── README.md                 
```

---

## 🧠 Pertanyaan Penelitian

### 1. Data Google Play Store
- Apakah rating memengaruhi jumlah unduhan aplikasi?
- Apakah aplikasi game lebih sering diperbarui?
- Bagaimana pengaruh harga terhadap jumlah unduhan?
- Apakah aplikasi komunikasi paling banyak diunduh?

### 2. Data Video Game 1980–2023
- Apakah tanggal rilis memengaruhi jumlah pemain?
- Bagaimana tren genre video game dari tahun ke tahun?
- Genre mana yang paling populer berdasarkan unduhan?
- Apa faktor yang memengaruhi wishlist sebuah game?

---

## 🔧 Tools & Teknologi

- Python (pandas, seaborn, matplotlib, scikit-learn)
- Jupyter Notebook / VS Code
- Spreadsheet untuk validasi
- Google Colab (opsional)

---

## 🧪 Metode Analisis

- Data Cleansing & Parsing
- Statistik Deskriptif
- Korelasi (Pearson)
- Regresi Linear Sederhana
- Visualisasi: Histogram, Scatterplot, Heatmap

---

## 📌 Hasil Utama

- Rating tidak selalu berbanding lurus dengan popularitas
- Game sering diperbarui dan memiliki engagement tinggi
- Harga aplikasi berdampak negatif pada unduhan
- Aplikasi komunikasi dan game mendominasi market
- Genre Adventure dan MOBA menonjol dalam tren jangka panjang
- Wishlist game tidak selalu mencerminkan pemain aktif

---

## 📤 Cara Menjalankan

Aktifkan environment Python dan jalankan file sesuai analisis:

```bash
python src/python/games_datacleansing.py
python src/python/googleplaystore_datacleansing.py
python src/python/Korelasi_Google_Play_Store.py
python src/python/Parsing_Data_Games.py
python src/python/Regresi_Linear_Harga_dan_Jumlah-Install.py
python src/python/Regresi_Linear_Rating_dan_Jumlah-Install.py
python src/python/Regresi_Linear_Wishlist_dan_Rating.py
python src/python/Statistik_Deskriptif_Google_Play_Store.py
```