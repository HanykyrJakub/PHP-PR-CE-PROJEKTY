import dask.dataframe as dd
import dask.array as da
from dask_ml.linear_model import LinearRegression
from dask_ml.model_selection import train_test_split
from dask import delayed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


np.random.seed(0)
dates = pd.date_range(start='2024-05-09', periods=1000, freq='D')
values = np.sin(np.linspace(0, 20, 100)) + np.random.normal(scale=0.6, size=1000)


df = pd.DataFrame({'Date': dates, 'Value': values})
df = ['Day'] = (df['Date'].min()).dt.days

dff = dd.from_pandas(df, npartitions=3)

X = dff[['day']]
y = dff['value']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=5, random_state = 0)


model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

y_test_np = y_test.compute()
y_pred_np = y_pred.compute()

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test_np, y_pred_np)
print(f'Error: {mse}')


#Zobrazení
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Value'], label='Skutečné hodnoty')
plt.plot(df['Date'].iloc[-len(y_test_np):], y_pred_np, 'r.', label='Predikované hodnoty')
plt.xlabel('Datum')
plt.ylabel('Hodnota')
plt.title('Predikce hodnot časové řady')
plt.legend()
plt.show()