import json
import logging
import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable

import pandas as pd

# Получаем путь к текущему скрипту
script_dir = os.path.dirname(os.path.abspath(__file__))

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Создаем папку logs, если её нет

# Настройка обработчиков
file_handler = logging.FileHandler("logs/reports.log", "w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)  # Убедимся, что обработчик принимает все уровни

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Форматтеры
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)

console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)

# Добавляем обработчики к логгеру
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def spending_by_category(date: str = None, category: str = None) -> Callable:  # type: ignore
    """Декоратор для фильтрации транзакций по категории и дате."""

    def decorator(func: Callable[..., pd.DataFrame]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> str:
            # Вызываем оригинальную функцию для получения DataFrame
            df = func(*args, **kwargs)

            if df.empty:
                return json.dumps([], ensure_ascii=False, indent=2)

            # Преобразуем дату, если она указана
            end_date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S") if date else datetime.now()
            start_date = end_date - timedelta(days=90)

            # Приводим колонки с датами к datetime
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

            # Фильтруем данные по категории и дате
            filtered = df[
                (df["Категория"] == category) & (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
            ]

            # Конвертируем в список словарей
            result = filtered.to_dict("records")

            # Конвертируем в JSON
            logger.info('Сформирован JSON-ответ "Отчеты"')
            return json.dumps(result, ensure_ascii=False, indent=2, default=str)

        return wrapper

    return decorator


@spending_by_category(date="31.12.2021 16:44:00", category="Супермаркеты")
def get_dataframe(filename: str) -> pd.DataFrame:
    """Функция читающая excel файл и возвращающая DataFrame."""
    try:
        df = pd.read_excel(filename)
        logger.info("DataFrame получен")
        return df
    except Exception as error:
        logger.error("%s", str(error), exc_info=True)
        raise Exception(f"Ошибка при чтении файла: {str(error)}")
