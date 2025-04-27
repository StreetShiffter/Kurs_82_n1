import json
import logging
import os
from typing import Any, Dict

from config import FILE_JSON, PATH_FILE
from src.utils import (get_cards_with_spend, get_currency, get_date_interval, get_path_to_file_and_period, get_stock,
                       get_top_transactions, greet_func)

# Получаем путь к текущему скрипту
script_dir = os.path.dirname(os.path.abspath(__file__))

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # exist_ok=True — чтобы не было ошибки, если папка уже есть
# Настройка обработчиков
file_handler = logging.FileHandler("logs/views.log", "w", "utf-8")
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


def main_info(datetime_string: str) -> Dict[str, Any]:
    """
    функций и главную функцию, принимающую на вход строку с датой и временем в формате "2025-04-22 18:16:00"
    и возвращающую JSON
    """

    # ПОДГОТОВКА: получаем DataFrame из документа operations.xlsx за определенный интервал
    time_period = get_date_interval(datetime_string)
    logger.info("Получен период времени")
    sorded_df = get_path_to_file_and_period(PATH_FILE, time_period)
    logger.info("Получен отсортированый DataFrame")

    # ШАГ 1: Приветствие по времени суток
    greeting = greet_func()
    logger.info("Работа приветствия ....OK")

    # ШАГ 2: Получение трат по картам за период
    cards = get_cards_with_spend(sorded_df)
    logger.info("Получена информация по тратам")

    # ШАГ 3: Вывод ТОП 5 транзакций по сумме платежа за период
    top_pay_transactions = get_top_transactions(sorded_df, 5)
    logger.info("Получены топ транзакций по категории")

    # ШАГ 4: Вывод курса валют
    currensies = get_currency(FILE_JSON)
    logger.info("Курс валют....ОК")
    # ШАГ 5: Вывод стоимости акций
    stock_prices = get_stock(FILE_JSON)
    logger.info("Стоимость акций....ОК")

    # Пример структуры JSON-ответа
    data = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_pay_transactions,
        "currency_rates": currensies,
        "stock_prices": stock_prices,
    }

    json_data_views = json.dumps(data, ensure_ascii=False, indent=4)
    logger.info('Сформирован JSON-ответ "Главная"')
    return json_data_views  # type: ignore
