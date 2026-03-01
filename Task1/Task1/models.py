from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
from sklearn.base import BaseEstimator
import numpy as np
from typing import Dict, Any, Tuple

# обучение модели
def gridsearch(
    model: BaseEstimator, 
    param_grid: Dict[str, Any], 
    X_train_scaled: np.ndarray, 
    y_train: np.ndarray, 
    cv: int = 5, 
    scoring: str = 'roc_auc'
) -> GridSearchCV:
    try:
        grid = GridSearchCV(model, param_grid, cv=cv, scoring=scoring)
        grid.fit(X_train_scaled, y_train)
        return grid
    except Exception as e:
        print(f"Ошибка при обучении модели: {e}")
        raise

# вычисление коэффициента Джини
def gini(grid: GridSearchCV, X_test_scaled: np.ndarray, y_test: np.ndarray) -> float:
    try:
        y_pred_proba = grid.predict_proba(X_test_scaled)[:, 1]
        return 2 * roc_auc_score(y_test, y_pred_proba) - 1
    except Exception as e:
        print(f"Ошибка при вычислении коэффициента Джини: {e}")
        raise

# обучение модели, поиск лучших гиперпараметров и вычисление коэффициента Джини
def train_and_evaluate(
    model: BaseEstimator, 
    param_grid: Dict[str, Any], 
    X_train_scaled: np.ndarray, 
    X_test_scaled: np.ndarray, 
    y_train: np.ndarray, 
    y_test: np.ndarray
) -> Tuple[Dict[str, Any], float]:
    grid = gridsearch(model, param_grid, X_train_scaled, y_train)
    param = grid.best_params_
    gini_value = gini(grid, X_test_scaled, y_test)
    return param, gini_value