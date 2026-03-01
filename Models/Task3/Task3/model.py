from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Tuple

# создание и обучение AR модели
def create_and_train_AR_model(
    train_data: np.ndarray, 
    ts_data: np.ndarray, 
    ar_order: int = 10
) -> np.ndarray:
    try:
        ar_model = AutoReg(train_data, lags=ar_order).fit()
        ar_forecast = ar_model.predict(start=len(train_data), end=len(ts_data)-1, dynamic=False)
        return ar_forecast
    except Exception as e:
        print(f"Ошибка при создании AR модели: {e}")
        raise

# создание и обучение ETS модели
def create_and_train_ETS_model(
    train_data: np.ndarray, 
    test_data: np.ndarray, 
    seasonal_periods: int = 50
) -> np.ndarray:
    try:
        ets_model = ExponentialSmoothing(
            train_data, 
            trend='add', 
            seasonal='add', 
            seasonal_periods=seasonal_periods
        ).fit()
        ets_forecast = ets_model.forecast(len(test_data))
        return ets_forecast
    except Exception as e:
        print(f"Ошибка при создании ETS модели: {e}")
        raise

# Вычисление метрик MAE и RMSE
def calculate_metrics(actual: np.ndarray, predicted: np.ndarray) -> Tuple[float, float]:
    try:
        mae = mean_absolute_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        return mae, rmse
    except Exception as e:
        print(f"Ошибка при вычислении метрик: {e}")
        raise

# таблица сравнения моделей AR и ETS по метрикам MAE и RMSE
def compare_models(
    test_data: np.ndarray, 
    ar_forecast: np.ndarray, 
    ets_forecast: np.ndarray
) -> str:
    try:
        ar_mae, ar_rmse = calculate_metrics(test_data, ar_forecast)
        ets_mae, ets_rmse = calculate_metrics(test_data, ets_forecast)

        metrics_df = pd.DataFrame({
            'Модель': ['AR', 'ETS'],
            'MAE': [ar_mae, ets_mae],
            'RMSE': [ar_rmse, ets_rmse]
        })
        return metrics_df.to_string(index=False)
    except Exception as e:
        print(f"Ошибка при сравнении моделей: {e}")
        raise

# визуализация прогнозов моделей
def visualize_forecasts(
    train_size: int, 
    n_observations: int, 
    test_data: np.ndarray, 
    ar_forecast: np.ndarray, 
    ets_forecast: np.ndarray
) -> None:
    try:
        test_indices = np.arange(train_size, n_observations)
        
        plt.figure(figsize=(14, 10))
        visualize_model('AR', 1, test_indices, test_data, ar_forecast)
        visualize_model('ETS', 2, test_indices, test_data, ets_forecast)
        plt.tight_layout()
        plt.savefig('Прогнозы моделей на разных графиках.png', dpi=150, bbox_inches='tight')
        plt.close()

        # сравнение прогнозов обеих моделей
        plt.figure(figsize=(14, 6))
        visualize_comparison(test_indices, test_data, ar_forecast, ets_forecast)
        plt.savefig('Прогнозы моделей на одном графике.png', dpi=150, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Ошибка при визуализации прогнозов: {e}")
        raise

# график-сравнение прогноза с истинными значениями для одной (любой) модели
def visualize_model(
    model_name: str, 
    n: int, 
    test_indices: np.ndarray, 
    test_data: np.ndarray, 
    forecast: np.ndarray
) -> None:
    try:
        plt.subplot(2, 1, n)
        plt.plot(test_indices, test_data, label='Истинные значения', color='blue', linewidth=2)
        plt.plot(test_indices, forecast, label=f'Прогноз {model_name}', color='green', linestyle='--', linewidth=2)
        plt.fill_between(test_indices, 
                          test_data, 
                          forecast, 
                          alpha=0.2, 
                          color='green', 
                          label='Ошибка прогноза')
        plt.title(f'Прогнозирование с использованием {model_name} модели')
        plt.xlabel('Наблюдения')
        plt.ylabel('Значение')
        plt.legend()
        plt.grid(True, alpha=0.3)
    except Exception as e:
        print(f"Ошибка при визуализации модели {model_name}: {e}")
        raise

# график-сравнение прогнозов обеих моделей с истинными значениями
def visualize_comparison(
    test_indices: np.ndarray, 
    test_data: np.ndarray, 
    ar_forecast: np.ndarray, 
    ets_forecast: np.ndarray
) -> None:
    try:
        plt.plot(test_indices, test_data, label='Истинные значения', color='black', linewidth=2, alpha=0.8)
        
        plt.plot(test_indices, ar_forecast, label=f'AR', color='red', linestyle='--', linewidth=1.5)
        plt.plot(test_indices, ets_forecast, label=f'ETS', color='green', linestyle='--', linewidth=1.5)
        
        plt.title('Сравнение прогнозов AR и ETS моделей на тестовой выборке')
        plt.xlabel('Наблюдения')
        plt.ylabel('Значение')
        plt.legend()
        plt.grid(True, alpha=0.3)
    except Exception as e:
        print(f"Ошибка при визуализации сравнения моделей: {e}")
        raise