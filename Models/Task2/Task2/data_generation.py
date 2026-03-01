from sklearn.model_selection import train_test_split
import numpy as np
from typing import Tuple

# генерация и разбиение датасета на обучающую и тестовую выборки
def create_and_split_dataset(
    random_state: int, 
    n_samples: int, 
    n_features: int, 
    test_size: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    try:
        np.random.seed(random_state)
        X = np.random.randn(n_samples, n_features)
        coefficients = np.random.randn(n_features)
        noise = np.random.randn(n_samples) * 0.5
        y = X @ coefficients + noise 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X, y, X_train, X_test, y_train, y_test
    except Exception as e:
        print(f"Ошибка при генерации и разбиении датасета: {e}")
        raise