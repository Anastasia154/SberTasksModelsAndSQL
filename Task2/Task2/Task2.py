import data_generation as dg
import models as m
import numpy as np

# запись информации о модели в файл
def write_Task2_in_file(
    mse: float, 
    r2: float, 
    vif: str, 
    shapiro: str, 
    mean: float, 
    standard_deviation: float, 
    importance: str
) -> None:
    try:
        with open('Задание_2.txt', 'w', encoding='utf-8') as f:
            f.write(f"\n=== Оценка качества модели ===\n")
            f.write(f"MSE: {mse}\n")
            f.write(f"коэффициент детерминации: {r2}\n")
            f.write(vif)
            f.write(f"\n=== Распределение остатков (тест Шапиро-Уилка на нормальность) ===\n")
            f.write(f"{shapiro}\n")
            f.write(f"Среднее остатков: {mean}\n")
            f.write(f"Стандартное отклонение остатков: {standard_deviation}\n")
            f.write("\n=== Важность признаков (по модулю коэффициентов) ===\n")
            f.write(importance)
    except (PermissionError, OSError) as e:
        print(f"Не удалось записать в файл: {e}")

# по умолчанию:
# случайное состояние генерации 42       
# 1000 наблюдений
# 10 признаков
# размер обучающей выборки 0,2       
def Task(
    random_state: int = 42, 
    n_samples: int = 1000, 
    n_features: int = 10, 
    test_size: float = 0.2
) -> None:
    
    try:
        coefficients = np.random.randn(n_features)
    except Exception as e:
        print(f"Ошибка при генерации коэффициентов: {e}")
        return
    
    feature_names = [f'Признак_{i + 1}' for i in range(n_features)]
    
    try:
        X, y, X_train, X_test, y_train, y_test = dg.create_and_split_dataset(random_state, n_samples, n_features, test_size)
    except Exception as e:
        print(f"Ошибка при генерации и разбиении датасета: {e}")
        return
    
    try:
        y_pred, model = m.create_and_train(X_train, X_test, y_train)
    except Exception as e:
        print(f"Ошибка при обучении модели: {e}")
        return
    
    try:
        mse, r2 = m.evaluate(y_test, y_pred)
    except Exception as e:
        print(f"Ошибка при вычислении метрик: {e}")
        return
    
    try:
        vif = m.multicollinearity(X, y, feature_names)
    except Exception as e:
        print(f"Ошибка при анализе мультиколлинеарности: {e}")
        vif = "Не удалось выполнить анализ мультиколлинеарности"
    
    try:
        shapiro, mean, standard_deviation = m.analysis_of_model_residuals(y_test, y_pred)
    except Exception as e:
        print(f"Ошибка при анализе остатков модели: {e}")
        shapiro, mean, standard_deviation = "Не удалось выполнить анализ", 0.0, 0.0
    
    try:
        importance = m.importance_of_the_features(model, feature_names, coefficients)
    except Exception as e:
        print(f"Ошибка при оценке важности признаков: {e}")
        return
    
    try:
        m.visualize_feature_importance(feature_names, importance)
    except Exception as e:
        print(f"Не удалось сохранить визуализацию важности признаков: {e}")
    
    write_Task2_in_file(mse, r2, vif, shapiro, mean, standard_deviation, importance.to_string(index=False))