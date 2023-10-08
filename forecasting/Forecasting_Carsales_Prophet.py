

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def load_and_prepare_data(filepath):

    try:
        df = pd.read_excel(filepath, engine='openpyxl')
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

    df = df.rename(columns={'ds': 'ds', 'Sales': 'y'})

    return df

def create_and_fit_model(data, yearly=True, weekly=False, daily=False):

    model = Prophet(yearly_seasonality=yearly, daily_seasonality=daily, weekly_seasonality=weekly)
    model.fit(data)
    return model

def predict(model, periods, freq='M'):

    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)
    return forecast

def plot_forecast(model, forecast):

    model.plot(forecast)
    plt.show()

def save_results(df, forecast, filepath):

    results = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    results = pd.merge(results, df, on='ds', how='left')
    results.to_excel(filepath, index=False)
    print(f"Results saved to {filepath}")

def predict_sales(filepath, periods=12, freq='M', yearly=True, weekly=False, daily=False):

    df = load_and_prepare_data(filepath)
    if df is None:
        return

    model = create_and_fit_model(df, yearly, weekly, daily)
    forecast = predict(model, periods, freq)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods))

    plot_forecast(model, forecast)

    results_filepath = filepath.rsplit('.', 1)[0] + '_forecast.xlsx'
    save_results(df, forecast, results_filepath)


file_path = r'D:\WWW\XF\code\sales_data.xlsx'
predict_sales(file_path, 60, 'M', True, False, False)


"""
Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality, plus holiday effects. 
It works best with time series that have strong seasonal effects and several seasons of historical data. Prophet is robust to missing data and shifts in the trend, and typically handles outliers well.

Prophet is open source software released by Facebook’s Core Data Science team. It is available for download on CRAN and PyPI.

https://facebook.github.io/prophet/
https://peerj.com/preprints/3190/
"""


