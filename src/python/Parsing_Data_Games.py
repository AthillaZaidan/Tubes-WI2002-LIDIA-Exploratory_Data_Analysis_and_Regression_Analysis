import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import os
import sys

# Fungsi untuk konversi format seperti "3.9K" menjadi 3900
def konversi_k_format(val):
    if pd.isna(val):
        return None
    val = str(val).strip().upper()
    if val.endswith('K'):
        try:
            return float(val[:-1]) * 1000
        except ValueError:
            return None
    try:
        return float(val)
    except ValueError:
        return None

# Cek ketersediaan file CSV
file_path = "games_cleaned.csv"
if not os.path.exists(file_path):
    print(f"File {file_path} tidak ditemukan!")
    sys.exit(1)

# Baca data
df_games = pd.read_csv(file_path)

# Konversi kolom numerik
kolom_numerik = ["Rating", "Times Listed", "Number of Reviews", "Plays", "Playing", "Backlogs", "Wishlist"]

for kolom in kolom_numerik:
    if kolom in df_games.columns:
        if kolom == "Rating":
            df_games[kolom] = pd.to_numeric(df_games[kolom], errors='coerce')
            df_games = df_games[(df_games[kolom] >= 0) & (df_games[kolom] <= 5)]
        else:
            df_games[kolom] = df_games[kolom].apply(konversi_k_format)

# Parsing 'Release Date' ke datetime
df_games['Release Date'] = pd.to_datetime(df_games['Release Date'], errors='coerce')

# Buat kolom 'Release Year' untuk analisis tren tahunan
df_games['Release Year'] = df_games['Release Date'].dt.year

# Parsing kolom Genres dari string list ke list asli
def parse_genres(genres_str):
    try:
        return ast.literal_eval(genres_str)
    except (ValueError, SyntaxError):
        return []

df_games['Genres List'] = df_games['Genres'].apply(parse_genres)

# -----------------------------------------------------
# Analisis korelasi numerik
df_corr = df_games[kolom_numerik].dropna().corr()
plt.figure(figsize=(10, 8))
sns.heatmap(df_corr, annot=True, cmap="coolwarm", fmt=".2f", square=True)
plt.title("Matriks Korelasi Variabel Numerik")
plt.tight_layout()
plt.savefig("korelasi_matrix_updated.png")
plt.close()

# -----------------------------------------------------
# Trend popularitas genre per tahun berdasarkan jumlah Plays
# Kita perlu explode list genre menjadi baris terpisah
df_genre_year = df_games[['Release Year', 'Genres List', 'Plays']].explode('Genres List')
df_genre_year = df_genre_year.dropna(subset=['Release Year', 'Genres List', 'Plays'])

# Grup berdasarkan tahun dan genre, hitung total Plays
genre_year_plays = df_genre_year.groupby(['Release Year', 'Genres List'])['Plays'].sum().reset_index()

# Plot popularitas genre top 5 per tahun (contoh)
top_genres = genre_year_plays.groupby('Genres List')['Plays'].sum().sort_values(ascending=False).head(5).index.tolist()
df_top_genres = genre_year_plays[genre_year_plays['Genres List'].isin(top_genres)]

plt.figure(figsize=(12, 7))
sns.lineplot(data=df_top_genres, x='Release Year', y='Plays', hue='Genres List', marker='o')
plt.title('Trend Popularitas Genre Teratas Berdasarkan Jumlah Plays (1980-2023)')
plt.xlabel('Tahun Rilis')
plt.ylabel('Jumlah Plays')
plt.legend(title='Genre')
plt.grid(True)
plt.savefig('trend_genre_per_tahun.png')
plt.close()

# -----------------------------------------------------
# Genre dengan jumlah unduhan (Plays) paling tinggi total sepanjang periode
genre_total_plays = df_genre_year.groupby('Genres List')['Plays'].sum().sort_values(ascending=False)
print("Top 5 Genre berdasarkan total Plays:")
print(genre_total_plays.head(5))

# -----------------------------------------------------
# Analisis faktor yang mempengaruhi Wishlist tinggi
# Korelasi Wishlist dengan variabel lain
wishlist_corr = df_games[kolom_numerik].corr()['Wishlist'].sort_values(ascending=False)
print("\nKorelasi variabel lain dengan Wishlist:")
print(wishlist_corr)

# Scatter plot Wishlist vs Rating sebagai contoh
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_games, x='Rating', y='Wishlist')
plt.title("Scatter Plot Rating vs Wishlist")
plt.xlabel("Rating")
plt.ylabel("Wishlist")
plt.grid(True)
plt.savefig("scatter_rating_vs_wishlist.png")
plt.close()

# Scatter plot Wishlist vs Times Listed
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_games, x='Times Listed', y='Wishlist')
plt.title("Scatter Plot Times Listed vs Wishlist")
plt.xlabel("Times Listed")
plt.ylabel("Wishlist")
plt.grid(True)
plt.savefig("scatter_timeslisted_vs_wishlist.png")
plt.close()

# Tambahan: Scatter Pair Plot antar semua kolom numerik
sns.pairplot(df_games[kolom_numerik].dropna())
plt.savefig("scatter_pairplot.png")
plt.close()

# ======== HISTOGRAM UNTUK SEMUA KOLOM NUMERIK ========
for kolom in kolom_numerik:
    data = df_games[kolom].dropna()
    if len(data) > 0:
        plt.figure(figsize=(10, 6))
        plt.hist(data, bins=20, edgecolor='black', alpha=0.7)
        plt.title(f"Distribusi {kolom}")
        plt.xlabel(kolom)
        plt.ylabel("Frekuensi")
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        file_name = f"histogram_{kolom.replace(' ', '_')}.png"
        plt.savefig(file_name)
        plt.close()
