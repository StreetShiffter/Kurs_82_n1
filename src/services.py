import json
import logging
import os
from typing import Dict, List
from pandas import DataFrame
from src.utils import get_phone_number

# Получаем путь к текущему скрипту
script_dir = os.path.dirname(os.path.abspath(__file__))

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # exist_ok=True — чтобы не было ошибки, если папка уже есть
# Настройка обработчиков
file_handler = logging.FileHandler("logs/services.log", "w", "utf-8")
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


def info_transaction_filter_phone(PATH_FILE: DataFrame) -> List[Dict]:
    """Функция принимающаяя транзакции, отфильтровывает по номеру и формирует JSON"""
    data = get_phone_number(PATH_FILE)  # type: ignore

    json_data_services = json.dumps(data, ensure_ascii=False, indent=4)
    logger.info('Сформирован JSON-ответ "Сервисы"')
    return json_data_services  # type: ignore