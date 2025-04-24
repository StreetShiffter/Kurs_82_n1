import json
from typing import Dict, Any
from config import PATH_FILE, FILE_JSON
from src.utils import (greet_func,
                   get_date_interval,
                   get_path_to_file_and_period,
                   get_cards_with_spend,
                   get_top_transactions,
                   get_currency,
                       get_stock)

def main_info(datetime_string: str) -> Dict[str, Any]:
  '''
    функций и главную функцию, принимающую на вход строку с датой и временем в формате "2025-04-22 18:16:00"
    и возвращающую JSON
  '''

  # ПОДГОТОВКА: получаем DataFrame из документа operations.xlsx за определенный интервал
  time_period = get_date_interval(datetime_string)
  sorded_df = get_path_to_file_and_period(PATH_FILE, time_period)

  # ШАГ 1: Приветствие по времени суток
  greeting =greet_func()

  # ШАГ 2: Получение трат по картам за период
  cards = get_cards_with_spend(sorded_df)

  # ШАГ 3: Вывод ТОП 5 транзакций по сумме платежа за период
  top_pay_transactions = get_top_transactions(sorded_df, 5 )

  # ШАГ 4: Вывод курса валют
  currensies = get_currency(FILE_JSON)
  # ШАГ 5: Вывод стоимости акций
  stock_prices = get_stock(FILE_JSON)

# Пример структуры JSON-ответа
  data = {
    "greeting": greeting,
    "cards": cards,
    "top_transactions": top_pay_transactions,
    "currency_rates": currensies,
    "stock_prices": stock_prices,
  }

  json_data = json.dumps(data, ensure_ascii=False, indent=4)
  return json_data