import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("GameList_CLEAN.csv")

X = df[['Rating']]
y = df['Wishlist']

model = LinearRegression()
model.fit(X, y)

a = model.coef_[0]
b = model.intercept_
print(f"Persamaan regresi:\nWishlist = {a:.2f} * Rating + {b:.2f}")
