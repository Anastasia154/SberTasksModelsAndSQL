from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import numpy as np
from typing import Tuple, Optional

# генерация и разбиение датасета на обучающую и тестовую выборки
def create_and_split_dataset(
    random_state: int, 
    n_samples: int, 
    n_features: int, 
    centers: int, 
    cluster_std: float, 
    center_box: Tuple[float, float], 
    test_size: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    try:
        # генерация
        X, y = make_blobs(
        n_samples=n_samples,
        n_features=n_features,
        centers=centers,
        cluster_std=cluster_std,
        center_box=center_box,
        random_state=random_state
        )
        # разбиение
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        return X, y, X_train, X_test, y_train, y_test
    except Exception as e:
        print(f"Ошибка при генерации и разбиении датасета: {e}")
        raise

# визуализация исходного датасета
def visualize_dataset(X: np.ndarray, y: np.ndarray) -> None:
    try:
        plt.figure(figsize=(10, 6))

        colors = ['red', 'green']
        for class_value in [0, 1]:
            plt.scatter(
                X[y == class_value, 0],
                X[y == class_value, 1],
                c=colors[class_value],
                label=f'Класс {class_value}',
                alpha=0.7,
                edgecolors='black',
                linewidth=0.5
            )
        
        plt.title('Визуализация синтетического датасета')
        plt.xlabel('Признак 1')
        plt.ylabel('Признак 2')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('Визуализация синтетического датасета.png', dpi=150, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Ошибка при визуализации датасета: {e}")

# стандартизация датасета
def standartize_dataset(X_train: np.ndarray, X_test: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    try:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        return X_train_scaled, X_test_scaled
    except Exception as e:
        print(f"Ошибка при стандартизации датасета: {e}")
        raise