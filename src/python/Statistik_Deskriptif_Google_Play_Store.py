import os
import pandas as pd
import matplotlib.pyplot as plt

# Setup directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load data
df_google = pd.read_csv("../file/googleplay/googleplaystore_cleaned.csv")


baris1 = "Rating"
baris2 = "Reviews"
baris3 = "Installs"
baris4 = "Price"
kolom_analisis = [baris1, baris2, baris3, baris4]


df_google[baris1] = pd.to_numeric(df_google[baris1], errors='coerce')
df_google[baris2] = pd.to_numeric(df_google[baris2], errors='coerce')

df_google[baris3] = df_google[baris3].astype(str).str.replace('[+,]', '', regex=True)
df_google[baris3] = pd.to_numeric(df_google[baris3], errors='coerce')

df_google[baris4] = df_google[baris4].astype(str).str.replace('$', '', regex=False)
df_google[baris4] = pd.to_numeric(df_google[baris4], errors='coerce')


all_stats = pd.DataFrame()

for kolom in kolom_analisis:
    data = df_google[kolom].dropna()

    statistik = {
        "Mean": data.mean(),
        "Standard Deviation": data.std(),
        "Percentile 10%": data.quantile(0.10),
        "Percentile 25%": data.quantile(0.25),
        "Median (50%)": data.median(),
        "Percentile 75%": data.quantile(0.75),
        "Percentile 90%": data.quantile(0.90),
        "Minimum": data.min(),
        "Maximum": data.max()
    }
    all_stats = pd.concat([all_stats, pd.DataFrame([statistik], index=[kolom])])

all_stats = all_stats.round(2)

# tabel
print("\n Statistik Deskriptif:")
print(all_stats)

# histogram
for kolom in kolom_analisis:
    data = df_google[kolom].dropna()

    
    if kolom == "Rating":
        data = data[(data >= 0) & (data <= 5)]
    elif kolom == "Price":
        data = data[(data >= 0) & (data <= 100)]
    elif kolom == "Installs":
        data = data[(data >= 0) & (data <= 1e7)]
    elif kolom == "Reviews":
        data = data[(data >= 0) & (data <= 2e6)]

    
    plt.figure()
    plt.hist(data, bins=30, edgecolor='black')
    plt.title(f"Distribusi {kolom}")
    plt.xlabel(kolom)
    plt.ylabel("Frekuensi")

    if kolom == "Rating":
        plt.xlim(0, 5)
    elif kolom == "Price":
        plt.xlim(0, 100)
    elif kolom == "Installs":
        plt.xlim(0, 1e7)
    elif kolom == "Reviews":
        plt.xlim(0, 2e6)

    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()