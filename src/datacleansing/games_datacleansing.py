import pandas as pd
import numpy as np

# Muat dataset
df_games = pd.read_csv('../../data/games/games.csv')

print("--- INFORMASI DATA GAMES.CSV SEBELUM CLEANSING ---")
print("Informasi Umum Dataset Games.csv:")
df_games.info()
print("\nJumlah Missing Values per Kolom Games.csv:")
print(df_games.isnull().sum())
print("\nPersentase Missing Values per Kolom Games.csv:")
print((df_games.isnull().sum() / len(df_games)) * 100)
print(f"\nJumlah Baris Duplikat Awal Games.csv: {df_games.duplicated().sum()}")
print("\nStatistik Deskriptif Kolom Numerik Awal Games.csv:")
print(df_games.describe())
print("\nContoh 5 Baris Pertama Games.csv:")
print(df_games.head())
print("-" * 50)

# Menghapus duplikat berdasarkan kolom 'Title'
rows_before_deduplication = len(df_games)
df_games.drop_duplicates(subset=['Title'], inplace=True)
print(f"\n--- LANGKAH UMUM: Menghapus Duplikat ---")
print(f"  Baris dihapus karena duplikasi (berdasarkan Title): {rows_before_deduplication - len(df_games)}")

# Kolom: Rating
# Tindakan: Hapus baris dengan missing values, pastikan dalam rentang valid.
rows_before_rating_clean = len(df_games)
df_games['Rating'] = pd.to_numeric(df_games['Rating'], errors='coerce') # Konversi ke numerik, ubah error menjadi NaN
df_games.dropna(subset=['Rating'], inplace=True) # Menghapus baris yang memiliki missing values (termasuk hasil coerce)
# Filter untuk rentang yang valid (jika ada nilai di luar range, hapus)
df_games = df_games[(df_games['Rating'] >= 0.0) & (df_games['Rating'] <= 5.0)]
print(f"\n--- CLEANSING 'Rating' ---")
print(f"  Baris dihapus (missing/out-of-range): {rows_before_rating_clean - len(df_games)}")

# Fungsi bantu untuk konversi string 'K'/'M' ke numerik
def convert_k_m_to_numeric(value):
    if isinstance(value, str):
        value = value.replace(',', '') # Hapus koma jika ada
        if 'K' in value:
            return float(value.replace('K', '')) * 1000
        elif 'M' in value:
            return float(value.replace('M', '')) * 1000000
    return pd.to_numeric(value, errors='coerce') # Konversi langsung atau jadi NaN jika tidak valid

columns_to_convert_and_filter = {
    'Times Listed': 10, # Batas bawah 10 kali terdaftar
    'Number of Reviews': 10, # Batas bawah 10 kali terdaftar
    'Plays': 100, # Batas bawah 100 plays
    'Playing': None, # Tidak ada batas bawah spesifik
    'Backlogs': None, # Tidak ada batas bawah spesifik
    'Wishlist': None # Tidak ada batas bawah spesifik
}

for col, threshold in columns_to_convert_and_filter.items():
    rows_before_col_clean = len(df_games)
    df_games[col] = df_games[col].apply(convert_k_m_to_numeric)
    df_games.dropna(subset=[col], inplace=True) # Hapus jika gagal konversi (NaN dari coerce)
    print(f"\n--- CLEANSING '{col}' ---")
    print(f"  Baris dihapus (gagal konversi/missing): {rows_before_col_clean - len(df_games)}")

    if threshold is not None:
        rows_before_threshold_filter = len(df_games)
        df_games = df_games[df_games[col] >= threshold]
        print(f"  Baris dihapus ({col} < {threshold}): {rows_before_threshold_filter - len(df_games)}")

    df_games[col] = df_games[col].astype(int) # Ubah ke integer secara permanen

# Kolom: Team, Summary
# Tindakan: Imputasi missing values dengan modus.
columns_to_impute_mode = ['Team', 'Summary']
for col in columns_to_impute_mode:
    if df_games[col].isnull().any():
        mode_val = df_games[col].mode()[0]
        df_games[col].fillna(mode_val, inplace=True)
        print(f"\n--- CLEANSING '{col}' ---")
        print(f"  Missing values pada '{col}' diisi dengan modus: {mode_val}")
        
        
# --- HASIL KESELURUHAN SETELAH CLEANSING ---
print("\n\n--- INFORMASI DATA GAMES.CSV SETELAH SEMUA CLEANSING ---")
print("Informasi Umum Dataset Games.csv:")
df_games.info()
print("\nJumlah Missing Values per Kolom Games.csv Setelah Cleansing:")
print(df_games.isnull().sum())
print("\nPersentase Missing Values per Kolom Games.csv Setelah Cleansing:")
print((df_games.isnull().sum() / len(df_games)) * 100)
print("\nStatistik Deskriptif Kolom (termasuk non-numerik):")
print(df_games.describe(include='all'))
print("\n5 Baris Pertama Data Games.csv Setelah Cleansing:")
print(df_games.head())

df_games.to_csv('../../data/games/games_cleaned.csv', index=False)