import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import BaggingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
import scipy.stats as stats
from typing import List, Tuple
from sklearn.base import RegressorMixin

# создание и обучение модели (по умолчанию на основе ленейной регрессии)
def create_and_train(
    X_train: np.ndarray, 
    X_test: np.ndarray, 
    y_train: np.ndarray, 
    base_model: RegressorMixin = LinearRegression(), 
    random_state: int = 42
) -> Tuple[np.ndarray, BaggingRegressor]:
    try:
        bagging_model = BaggingRegressor(
            estimator=base_model,
            n_estimators=50,
            random_state=random_state,
            n_jobs=-1
        )
        bagging_model.fit(X_train, y_train)
        y_pred = bagging_model.predict(X_test)
        return y_pred, bagging_model
    except Exception as e:
        print(f"Ошибка при создании и обучении модели: {e}")
        raise

# Вычисление метрик MSE и R**2 на основе предсказанных значений
def evaluate(y_test: np.ndarray, y_pred: np.ndarray) -> Tuple[float, float]:
    try:
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        return mse, r2
    except Exception as e:
        print(f"Ошибка при вычислении метрик: {e}")
        raise

# Матрица корреляции
def correlation_matrix(
    X: np.ndarray, 
    y: np.ndarray, 
    feature_names: List[str], 
    n_features: int = 1000
) -> None:
    try:
        df = pd.DataFrame(X, columns=feature_names)
        df['target'] = y
        plt.figure(figsize=(10, 8))
        correlation_matrix = df[feature_names].corr()
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)
        plt.title('Матрица корреляции признаков')
        plt.tight_layout()
        plt.savefig('Матрица корреляции.png', dpi=150, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Ошибка при построении матрицы корреляции: {e}")
        raise
    
# Мультиколлинеарность признаков (VIF)
def vif(X: np.ndarray, feature_names: List[str]) -> str:
    try:
        X_with_const = add_constant(X)
        vif_data = pd.DataFrame()
        vif_data["Feature"] = ["const"] + feature_names
        vif_data["VIF"] = [variance_inflation_factor(X_with_const, i) for i in range(X_with_const.shape[1])]

        high_vif = vif_data[(vif_data["Feature"] != "const") & (vif_data["VIF"] > 5)]
        if len(high_vif) > 0:
            s_vif = "Признаки с высокой мультиколлинеарностью (VIF > 5):"
            for feature in high_vif["Feature"].values:
                s_vif += " " + feature
        else:
            s_vif = "Мультиколлинеарность не обнаружена (все VIF <= 5)"
        return s_vif
    except Exception as e:
        print(f"Ошибка при вычислении VIF: {e}")
        raise

# нахождение VIF и матрицы корреляции для проверки мультиколлинеарности признаков
def multicollinearity(
    X: np.ndarray, 
    y: np.ndarray, 
    feature_names: List[str], 
    n_features: int = 10
) -> str:
    try:
        correlation_matrix(X, y, feature_names, n_features)
        s_vif = vif(X, feature_names)
        return s_vif
    except Exception as e:
        print(f"Ошибка при анализе мультиколлинеарности: {e}")
        raise

# анализ остатков модели (построение графика и гистограммы остатков, тест Шапиро-Уилка на нормальность)
def analysis_of_model_residuals(
    y_test: np.ndarray, 
    y_pred: np.ndarray
) -> Tuple[str, float, float]:
    try:
        residuals = y_test - y_pred
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # График остатков против предсказанных значений
        axes[0].scatter(y_pred, residuals, alpha=0.5)
        axes[0].axhline(y=0, color='r', linestyle='--')
        axes[0].set_xlabel('Предсказанные значения')
        axes[0].set_ylabel('Остатки')
        axes[0].set_title('Остатки vs Предсказанные значения')

        # Гистограмма остатков
        axes[1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[1].set_xlabel('Остатки')
        axes[1].set_ylabel('Частота')
        axes[1].set_title('Распределение остатков')

        plt.tight_layout()
        plt.savefig('Остатки.png', dpi=150, bbox_inches='tight')
        plt.close()

        # Тест Шапиро-Уилка на нормальность
        residuals_for_test = residuals[:5000] if len(residuals) > 5000 else residuals
        shapiro_stat, shapiro_p = stats.shapiro(residuals_for_test)
        
        if shapiro_p > 0.05:
            shapiro_result = f"Остатки распределены нормально (p={shapiro_p:.4f} > 0.05)"
        else:
            shapiro_result = f"Остатки не распределены нормально (p={shapiro_p:.4f} <= 0.05)"

        mean = float(np.mean(residuals))
        standard_deviation = float(np.std(residuals))
        
        return shapiro_result, mean, standard_deviation
    except Exception as e:
        print(f"Ошибка при анализе остатков модели: {e}")
        raise

# важность признаков    
def importance_of_the_features(
    bagging_model: BaggingRegressor, 
    feature_names: List[str], 
    coefficients: np.ndarray
) -> pd.DataFrame:
    try:
        all_coefs = []
        for estimator in bagging_model.estimators_:
            if hasattr(estimator, 'coef_'):
                all_coefs.append(estimator.coef_)

        avg_coefficients = np.mean(all_coefs, axis=0)

        importance_df = pd.DataFrame({
            'Признаки': feature_names,
            'Истинные коэффициенты': coefficients,
            'Оцененные коэффициенты': avg_coefficients,
            'Абсолютная важность': np.abs(avg_coefficients)
        })

        importance_df = importance_df.sort_values('Абсолютная важность', ascending=False)
        return importance_df
    except Exception as e:
        print(f"Ошибка при оценке важности признаков: {e}")
        raise

# Визуализация важности признаков 
def visualize_feature_importance(
    feature_names: List[str], 
    importance_df: pd.DataFrame
) -> None:
    try:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Сравнение истинных и оцененных коэффициентов
        y_pos = np.arange(len(feature_names))
        axes[0].barh(y_pos, importance_df['Истинные коэффициенты'].values, 
                     alpha=0.5, label='Истинные', color='blue', height=0.4)
        axes[0].barh(y_pos + 0.4, importance_df['Оцененные коэффициенты'].values, 
                     alpha=0.5, label='Оцененные', color='red', height=0.4)
        axes[0].set_yticks(y_pos + 0.2)
        axes[0].set_yticklabels(importance_df['Признаки'].values)
        axes[0].set_xlabel('Значение коэффициента')
        axes[0].set_title('Сравнение истинных и оцененных коэффициентов')
        axes[0].legend()

        # Важность признаков (по модулю)
        axes[1].barh(importance_df['Признаки'], importance_df['Абсолютная важность'], color='green', alpha=0.7)
        axes[1].set_xlabel('Важность (|коэффициент|)')
        axes[1].set_title('Важность признаков')

        plt.tight_layout()
        plt.savefig('Важность признаков.png', dpi=150, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Ошибка при визуализации важности признаков: {e}")
        raise