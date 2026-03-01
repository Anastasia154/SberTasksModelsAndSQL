import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

# генерация и разбиение датасета на обучающую и тестовую выборки
def create_and_split_dataset(
    random_state: int, 
    train_size: int, 
    n_observations: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    try:
        t = np.arange(0, n_observations)
        np.random.seed(random_state)
        sin_component = 5 * np.sin(2 * np.pi * t / 50) # Синусоидальная компонента
        trend_component = 0.01 * t # Трендовая компонента
        noise_component = np.random.normal(0, 1, n_observations) # Случайный шум
        ts_data = sin_component + trend_component + noise_component # Суммарный ряд

        if train_size > len(ts_data):
            raise ValueError(f"train_size ({train_size}) больше длины ряда ({len(ts_data)})")
        
        train_data = ts_data[:train_size]
        test_data = ts_data[train_size:]
        
        return t, ts_data, train_data, test_data
    except Exception as e:
        print(f"Ошибка при генерации временного ряда: {e}")
        raise

# визуализация исходного датасета
def visualize(t: np.ndarray, ts_data: np.ndarray, train_size: int) -> None:
    try:
        plt.figure(figsize=(14, 6))
        plt.plot(t, ts_data, label='Исходный ряд', color='blue', alpha=0.7)
        plt.axvline(x=train_size, color='red', linestyle='--', label='Граница train/test')
        plt.title('Синтетический временной ряд')
        plt.xlabel('Наблюдения')
        plt.ylabel('Значение')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('Визуализация синтетического временного ряда.png', dpi=150, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Ошибка при визуализации временного ряда: {e}")
        raise