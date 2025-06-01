import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("data/googleplaystore_cleaned.csv")

df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")


kolom_korelasi = ["Rating", "Reviews", "Installs", "Price"]
df_subset = df[kolom_korelasi].dropna()

corr_matrix = df_subset.corr().round(2)

plt.figure(figsize=(6, 5))
sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    vmin=0,
    vmax=1,
    square=True,
    linewidths=0.5
)
plt.title("Matriks Korelasi")
plt.tight_layout()
plt.savefig("matriks_korelasi_googleplaystore.png")
plt.show()