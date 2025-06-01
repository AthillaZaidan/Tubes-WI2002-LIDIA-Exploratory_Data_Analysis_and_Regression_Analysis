import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("Playstore.csv")

df = df.dropna(subset=['Price', 'Installs'])

df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)
df = df[df['Price'].str.replace('.', '', 1).str.isnumeric()]
df['Price'] = df['Price'].astype(float)

df = df[df['Price'] < 250]

X = df[['Price']]
y = df['Installs']

model = LinearRegression()
model.fit(X, y)

a = model.coef_[0]
b = model.intercept_
print(f"Installs(p) = {a:.2f} * p + {b:.2f}")
