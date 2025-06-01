import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('Playstore.csv')

df = df.dropna(subset=['Rating', 'Installs'])
df['Installs'] = df['Installs'].astype(str).str.replace('[+,]', '', regex=True).astype(int)

X = df[['Rating']]
y = df['Installs']

model = LinearRegression()
model.fit(X, y)

a = model.coef_[0]
b = model.intercept_

print(f'Installs = {a:.2f} * Rating + {b:.2f}')
