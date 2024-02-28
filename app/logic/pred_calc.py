import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


def load_data_pred():
    df = pd.read_csv("./data/commerce_dataset.csv", sep=";")
    df['dtme'] = pd.to_datetime(df['dtme'])  # Convert 'dtme' to datetime
    df.set_index("dtme", inplace=True)

    return df


def prepare_data(df, split_ratio=0.2):
    # Agregar os dados para obter o total de vendas por dia
    daily_sales = df["total"].resample("D").sum()

    # Dividir os dados em conjunto de treinamento (20%) e teste (80%)
    split_point = int(len(daily_sales) * split_ratio)
    train_data, test_data = daily_sales[:split_point], daily_sales[split_point:]

    return train_data, test_data


def train_sarima(train_data, p=1, d=1, q=1, P=2, D=1, Q=1, m=7):
    # Construir e treinar o modelo SARIMA com o conjunto de treinamento
    model_sarima = SARIMAX(train_data, order=(p, d, q), seasonal_order=(P, D, Q, m))
    model_sarima_fit = model_sarima.fit(disp=False)

    return model_sarima_fit


def make_forecast(model_sarima_fit, test_data):
    # Realizar previsões no conjunto de teste
    forecast = model_sarima_fit.get_forecast(steps=len(test_data))
    forecast_mean = forecast.predicted_mean
    forecast_ci = forecast.conf_int()

    return forecast_mean, forecast_ci
