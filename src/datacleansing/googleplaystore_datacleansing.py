import pandas as pd
import numpy as np

# Muat dataset
df = pd.read_csv('../../data/googleplay/googleplaystore.csv')

print("--- INFORMASI DATA SEBELUM CLEANSING ---")
print("Informasi Umum Dataset:")
df.info()
print("\nJumlah Missing Values per Kolom:")
print(df.isnull().sum())
print("\nPersentase Missing Values per Kolom:")
print((df.isnull().sum() / len(df)) * 100)
print(f"\nJumlah Baris Duplikat Awal: {df.duplicated().sum()}")
print("-" * 50)

# --- Langkah Pre-cleansing Umum (Penanganan Baris Anomali dan Duplikat Umum) ---
# Baris ini dikenal sebagai baris yang salah parsing, 'Category' adalah '1.9'
initial_rows = len(df)
df = df[df['Category'] != '1.9']
print(f"\n[UMUM] Baris dihapus karena anomali parsing (Category = '1.9'): {initial_rows - len(df)}")

# Hapus duplikat berdasarkan kolom 'App' untuk memastikan setiap aplikasi unik
rows_before_deduplication = len(df)
df.drop_duplicates(subset=['App'], inplace=True)
print(f"[UMUM] Baris dihapus karena duplikasi (berdasarkan App): {rows_before_deduplication - len(df)}")

# Kolom: Rating
# Tindakan: Hapus baris dengan missing values, pastikan dalam rentang [1.0, 5.0]
print("\n--- CLEANSING 'Rating' ---")
rows_before_rating_clean = len(df)
df.dropna(subset=['Rating'], inplace=True) # Menghapus baris yang memiliki missing values pada 'Rating'
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce') # Konversi ke numerik, ubah error menjadi NaN
df = df[(df['Rating'] >= 1.0) & (df['Rating'] <= 5.0)] # Filter untuk rentang yang valid
print(f"  Baris dihapus (missing/out-of-range): {rows_before_rating_clean - len(df)}")

# Kolom: Reviews
# Tindakan: Konversi ke numerik, hapus jika gagal. Terapkan batas bawah.
df['Reviews'] = df['Reviews'].astype(str).str.replace('+', '', regex=False) # Hapus '+'
df['Reviews'] = df['Reviews'].str.replace(',', '', regex=False) # Hapus ','
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce') # Konversi ke numerik, ubah error menjadi NaN
rows_before_reviews_clean = len(df)
df.dropna(subset=['Reviews'], inplace=True) # Hapus jika gagal konversi (NaN dari coerce)
print(f"\n--- CLEANSING 'Reviews' ---")
print(f"  Baris dihapus (gagal konversi): {rows_before_reviews_clean - len(df)}")

# Penambahan Batas Bawah untuk Reviews
min_reviews_threshold = 10
rows_before_reviews_threshold = len(df)
df = df[df['Reviews'] >= min_reviews_threshold]
print(f"  Baris dihapus (Reviews < {min_reviews_threshold}): {rows_before_reviews_threshold - len(df)}")
df['Reviews'] = df['Reviews'].astype(int) # Ubah ke integer secara permanen

# Kolom: Installs
# Tindakan: Hapus karakter '+', ',', konversi ke numerik, hapus jika gagal. Terapkan batas bawah.
df['Installs'] = df['Installs'].astype(str).str.replace('+', '', regex=False)
df['Installs'] = df['Installs'].str.replace(',', '', regex=False)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
rows_before_installs_clean = len(df)
df.dropna(subset=['Installs'], inplace=True) # Hapus jika gagal konversi
print(f"\n--- CLEANSING 'Installs' ---")
print(f"  Baris dihapus (gagal konversi): {rows_before_installs_clean - len(df)}")

# Penambahan Batas Bawah untuk Installs
min_installs_threshold = 1000
rows_before_installs_threshold = len(df)
df = df[df['Installs'] >= min_installs_threshold]
print(f"  Baris dihapus (Installs < {min_installs_threshold}): {rows_before_installs_threshold - len(df)}")
df['Installs'] = df['Installs'].astype(int) # Ubah ke integer secara permanen

# Kolom: Size
# Tindakan: Konversi 'M'/'k' ke Megabytes, 'Varies with device' ke NaN, lalu imputasi NaN dengan median.
def clean_size(size):
    if isinstance(size, str):
        size = size.replace(',', '') # Hapus koma jika ada
        if 'M' in size:
            return float(size.replace('M', ''))
        elif 'k' in size:
            return float(size.replace('k', '')) / 1024 # Konversi Kilobytes ke Megabytes
        elif 'Varies with device' in size:
            return np.nan # Menjadi NaN
    return np.nan # Untuk nilai yang tidak dikenal atau bukan string

df['Size'] = df['Size'].apply(clean_size)
df['Size'].fillna(df['Size'].median(), inplace=True) # Imputasi NaN pada Size dengan median
print(f"\n--- CLEANSING 'Size' ---")
print("  NaN pada kolom 'Size' diisi dengan median.")

# Kolom: Price
# Tindakan: Hapus karakter '$', konversi ke numerik, hapus jika gagal.
df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
rows_before_price_clean = len(df)
df.dropna(subset=['Price'], inplace=True) # Hapus jika gagal konversi
print(f"\n--- CLEANSING 'Price' ---")
print(f"  Baris dihapus (gagal konversi): {rows_before_price_clean - len(df)}")

# Kolom: Type, Content Rating, Current Ver, Android Ver
# Tindakan: Imputasi missing values dengan modus.
columns_to_impute_mode = ['Type', 'Content Rating', 'Current Ver', 'Android Ver']
for col in columns_to_impute_mode:
    if df[col].isnull().any():
        mode_val = df[col].mode()[0]
        df[col].fillna(mode_val, inplace=True)
        print(f"\n--- CLEANSING '{col}' ---")
        print(f"  Missing values pada '{col}' diisi dengan modus: {mode_val}")

# --- HASIL KESELURUHAN SETELAH CLEANSING ---
print("\n\n--- INFORMASI DATA GOOGLEPLAYSTORE.CSV SETELAH SEMUA CLEANSING ---")
print("Informasi Umum Dataset GooglePlayStore.csv:")
df.info()
print("\nJumlah Missing Values per Kolom GooglePlayStore.csv Setelah Cleansing:")
print(df.isnull().sum())
print("\nPersentase Missing Values per Kolom GooglePlayStore.csv Setelah Cleansing:")
print((df.isnull().sum() / len(df)) * 100)
print("\nStatistik Deskriptif Kolom (termasuk non-numerik):")
print(df.describe(include='all'))
print("\n5 Baris Pertama Data GooglePlayStore.csv Setelah Cleansing:")
print(df.head())

df.to_csv('../../data/googleplay/googleplaystore_cleaned.csv', index=False)