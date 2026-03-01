import models as m
import data_generation as dg
import os
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, Any, Tuple

# запись информации о модели в файл
def write_Task1_in_file(message: str, params: Dict[str, Any], gini: float) -> None:
    try:
        with open('Задание_1.txt', 'a', encoding='utf-8') as f:
            f.write(message + '\n')
            f.write('Лучшие гиперпараметры:')
            for param_name, param_value in params.items():
                f.write(f' {param_name}={param_value};')
            f.write(f'\nКоэффициент Джини: {gini}\n\n')
    except (PermissionError, OSError) as e:
        print(f"Не удалось записать в файл: {e}")

# по умолчанию:
# случайное состояние генерации 42      
# 1000 наблюдений
# 2 признака 
# 2 центра кластеров
# стандартное отклонение кластеров 3.8 
# диапазон значений центров (-6.0, 6.0)
# размер обучающей выборки 0,2         
def Task(
    random_state: int = 42, 
    n_samples: int = 1000, 
    n_features: int = 2, 
    centers: int = 2, 
    cluster_std: float = 3.8, 
    center_box: Tuple[float, float] = (-6.0, 6.0), 
    test_size: float = 0.3
) -> None:
   
    try:
        if os.path.exists("Задание_1.txt"):
            os.remove("Задание_1.txt")
    except (PermissionError, OSError) as e:
        print(f"Не удалось удалить файл: {e}")
        
    # подготовка и визуализация датасета
    try:
        X, y, X_train, X_test, y_train, y_test = dg.create_and_split_dataset(random_state, n_samples, n_features, centers, 
                                                                         cluster_std, center_box, test_size)
    except ValueError as e:
        print(f"Ошибка при генерации данных: {e}")
        return

    try:
        dg.visualize_dataset(X, y)
    except Exception as e:
        print(f"Не удалось сохранить визуализацию: {e}")
    
    try:
        X_train_scaled, X_test_scaled = dg.standartize_dataset(X_train, X_test)
    except ValueError as e:
        print(f"Ошибка при стандартизации данных: {e}")
        return

    # Логистическая регрессия
    try:
        lr = LogisticRegression(random_state=random_state)
        param_grid_lr = {'C': [0.1, 1, 10]}
        param_lr, gini_lr = m.train_and_evaluate(lr, param_grid_lr, X_train_scaled, X_test_scaled, y_train, y_test)
        write_Task1_in_file('Логистическая регрессия', param_lr, gini_lr)
    except Exception as e:
        print(f"Ошибка при обучении логистической регрессии: {e}")

    # Машина опорных векторов
    try:
        svm = SVC(probability=True, random_state=random_state)
        param_grid_svm = { 'C': [0.1, 1, 10], 'gamma': [0.01, 0.1, 1] }
        param_svm, gini_svm = m.train_and_evaluate(svm, param_grid_svm, X_train_scaled, X_test_scaled, y_train, y_test)
        write_Task1_in_file('Машина опорных векторов', param_svm, gini_svm)
    except Exception as e:
        print(f"Ошибка при обучении машины опорных векторов: {e}")

    # Дерево решений
    try:
        dt = DecisionTreeClassifier(random_state=random_state)
        param_grid_dt = { 'max_depth': [5, 10, 20], 'min_samples_split': [2, 5, 10]}
        param_dt, gini_dt = m.train_and_evaluate(dt, param_grid_dt, X_train_scaled, X_test_scaled, y_train, y_test)
        write_Task1_in_file('Дерево решений', param_dt, gini_dt)
    except Exception as e:
        print(f"Ошибка при обучении дерева решений: {e}")

    # Случайный лес
    try:
        rf = RandomForestClassifier(random_state=random_state)
        param_grid_rf = { 'n_estimators': [10, 50, 100], 'max_depth': [5, 10, 20] }
        param_rf, gini_rf = m.train_and_evaluate(rf, param_grid_rf, X_train_scaled, X_test_scaled, y_train, y_test)
        write_Task1_in_file('Случайный лес', param_rf, gini_rf)
    except Exception as e:
        print(f"Ошибка при обучении случайного леса: {e}")