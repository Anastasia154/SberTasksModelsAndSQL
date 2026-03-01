import data_generation as dg
import model as m

# запись информации о модели в файл
def write_Task3_to_file(metrics: str) -> None:
    try:
        with open('Задание_3.txt', 'w', encoding='utf-8') as f:
            f.write('=== Сравнение метрик ===\n')
            f.write(metrics)
    except (PermissionError, OSError) as e:
        print(f"Не удалось записать в файл: {e}")

# по умолчанию:
# случайное состояние генерации 42        
# 1000 наблюдений
# размер обучающей выборки 0,8 (80%)
def Task() -> None:
    random_state: int = 42
    n_observations: int = 1000
    train_size: int = int(0.8 * n_observations)
    
    try:
        t, ts_data, train_data, test_data = dg.create_and_split_dataset(random_state, train_size, n_observations)
    except Exception as e:
        print(f"Ошибка при генерации временного ряда: {e}")
        return
    
    try:
        dg.visualize(t, ts_data, train_size)
    except Exception as e:
        print(f"Не удалось сохранить визуализацию исходного ряда: {e}")

    try:
        ar_forecast = m.create_and_train_AR_model(train_data, ts_data)
    except Exception as e:
        print(f"Ошибка при обучении AR модели: {e}")
        ar_forecast = None
    
    try:
        ets_forecast = m.create_and_train_ETS_model(train_data, test_data)
    except Exception as e:
        print(f"Ошибка при обучении ETS модели: {e}")
        ets_forecast = None
    
    if ar_forecast is None or ets_forecast is None:
        print("Не удалось обучить одну или обе модели. Сравнение невозможно.")
        return
    
    try:
        metrics = m.compare_models(test_data, ar_forecast, ets_forecast)
    except Exception as e:
        print(f"Ошибка при сравнении моделей: {e}")
        return

    write_Task3_to_file(metrics)

    try:
        m.visualize_forecasts(train_size, n_observations, test_data, ar_forecast, ets_forecast)
    except Exception as e:
        print(f"Не удалось сохранить визуализацию прогнозов: {e}")