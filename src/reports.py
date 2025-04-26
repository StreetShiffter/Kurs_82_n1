from config import PATH_FILE
import pandas as pd
from datetime import datetime, timedelta
import json
from functools import wraps


def spending_by_category(date=None, category=None):
    """Декоратор для фильтрации транзакций по категории и дате"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Вызываем оригинальную функцию для получения DataFrame
            df = func(*args, **kwargs)

            if df.empty:
                return json.dumps([], ensure_ascii=False, indent=2)

            # Преобразуем дату, если она указана
            end_date = datetime.strptime(date, '%d.%m.%Y %H:%M:%S') if date else datetime.now()
            start_date = end_date - timedelta(days=90)

            # Приводим колонки с датами к datetime
            df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')

            # Фильтруем данные по категории и дате
            filtered = df[
                (df['Категория'] == category) &
                (df['Дата операции'] >= start_date) &
                (df['Дата операции'] <= end_date)
                ]

            # Конвертируем в список словарей
            result = filtered.to_dict('records')

            # Конвертируем в JSON
            return json.dumps(result, ensure_ascii=False, indent=2, default=str)

        return wrapper

    return decorator


# @spending_by_category(date="31.12.2021 16:44:00", category="Супермаркеты")
# def get_dataframe(filename: str) -> pd.DataFrame:
#     """Функция читающая excel файл и возвращающая DataFrame"""
#     try:
#         df = pd.read_excel(filename)
#         return df
#     except Exception as error:
#         raise Exception(f'Ошибка при чтении файла: {str(error)}')


# Пример использования
# result = get_dataframe(PATH_FILE)
# print(result)