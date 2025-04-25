from datetime import datetime
from pandas import DataFrame
from pprint import pprint
from typing import Dict, Any, List
import pandas as pd
from dotenv import load_dotenv
import re
import requests
import json
import os
import yfinance as yf
import time

from config import PATH_FILE

URL = "https://api.apilayer.com/exchangerates_data/convert"

# Загрузка переменных из .env-файла
load_dotenv()

# Получаем API-ключ из переменных окружения
API_KEY = os.getenv("API_KEY")  # Убедитесь, что в .env есть строка API_KEY=ваш_ключ
headers = {"apikey": API_KEY}



def greet_func()-> str:
    """Функция определяющая время суток и приветствует"""
    time_now = datetime.now().hour
    if 6 < time_now <= 12:
        greet = "Доброе утро"
    elif 12 < time_now <= 18:
            greet = "Добрый день"
    elif 18 < time_now <= 23:
            greet = "Добрый вечер"
    else:
        greet = "Доброй ночи"

    return greet



def get_date_interval(datetime_string: str, data_format="%Y-%m-%d %H:%M:%S") -> list[str]:
    '''
        2. Функция получения периода даты. Если дата на вход подана дата: 20.05.2020,то данные для анализа
        будут в диапазоне 01.05.2020 - 20.05.2020.
        Дополнительно: преобразование даты из "%Y-%m-%d %H:%M:%S" в "%d.%m.%Y %H:%M:%S" (согласно формату даты в Excel)
    '''

    today_day_by_period = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    first_day_by_period = today_day_by_period.replace(day=1)

    return [
        first_day_by_period.strftime("%d.%m.%Y %H:%M:%S"),
        today_day_by_period.strftime("%d.%m.%Y %H:%M:%S")
    ]







def get_path_to_file_and_period(path_to_file: str, time_period: list) -> DataFrame:
    '''
        3. Функция принимает путь к Excel файлу и полученный период из ф-ии get_data_period
        и осуществляет возврат таблицы в заданном периоде
    '''
    # Читаем данные построчно
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")

    # Преобразуем строки колонки "Дата операции" в формат даты
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    # Задаём начальный день периода (индекс 0 из списка периода и приводим к формату "%d.%m.%Y %H:%M:%S)
    start_date = datetime.strptime(time_period[0], "%d.%m.%Y %H:%M:%S")
    # Задаём конечный день периода  (индекс 1 из списка периода и приводим к формату "%d.%m.%Y %H:%M:%S)
    end_date = datetime.strptime(time_period[1], "%d.%m.%Y %H:%M:%S")

    # фильтруем ип получаем данные в filtered_df по колонке "Дата операции" с 1-ого по крайний день
    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= end_date)
        ]
    # Сортируем полученные данные из filtered_df по возрастанию
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)

    return sorted_df


def get_cards_with_spend(sorded_df: DataFrame) -> list[dict]:
    '''
        4. Функция принимает DataFrame и возвращает список карт с расходами
    '''
    card_expenses_transactions = []
    card_sorted = sorded_df[
        [
            "Номер карты",
            "Сумма операции",
            "Кэшбэк",
            "Сумма операции с округлением",
        ]
    ]
    for index, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", '')
            total_spent = row["Сумма операции с округлением"]
            cashback = float(total_spent) // 100
            row = {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": cashback
            }
            card_expenses_transactions.append(row)

    return card_expenses_transactions

def get_top_transactions(sorted_df: DataFrame, get_top):
    """
        5. Функция принимает DataFrame и возвращает get_top топ-транзакций по сумме платежа
    """
    top_pay_transactions = []
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_transactions = sorted_pay_df.head(get_top)
    top_transactions_sorted = top_transactions[
        [
            "Дата платежа",
            "Сумма операции",
            "Категория",
            "Описание"
        ]
    ]

    for i, row in top_transactions_sorted.iterrows():
        transaction = {
          "date": f'{row["Дата платежа"]}',
          "amount": f'{row["Сумма операции"]}',
          "category": f'{row["Категория"]}',
          "description": f'{row["Описание"]}'
        }
        top_pay_transactions.append(transaction)

    return top_pay_transactions


def get_currency(path_to_json: str) -> list[dict]:
    """
        6. Функция принимает путь к json файлу и полученный и возвращает курс валют
    """
    currency_rates = []
    with open (path_to_json, "r", encoding="utf8") as file:
        data = json.load(file)
        # обращение к ключу "user_currencies" для получения списка значений, хранящейся в нём валюты
        currencies = data["user_currencies"]
        for currency in currencies:
           params = {
               "amount" : 1,
               "from" : currency,
               "to" : "RUB"
           }
           # Работа с API
           headers = {
               "apikey": API_KEY
           }

           # отправляем по HTTP GET-запрос к указанному URL с заданными параметрами (params) и заголовками (headers),
           response = requests.get(URL, headers=headers, params=params)

           # сохраняем статус-код ответа в переменную status_code
           status_code = response.status_code
           if status_code == 200:
               result = response.json()
               currency_code_response = result["query"]["from"]
               currency_amount = round(result["result"], 2)
               currency_rates.append(
                   {
               "currency" : currency_code_response,
               "rate" : currency_amount
           })
    return currency_rates


def get_stock(path_to_json: str, max_retries: int = 3) -> list[dict]:
    """
    7. Функция принимает путь к json файлу и полученный и возвращает стоимость акций
    """
    stock_rates = []

    with open(path_to_json, "r", encoding="utf8") as file:
        data = json.load(file)

    for stock in data["user_stocks"]:
        for attempt in range(max_retries):
            try:
                ticker = yf.Ticker(stock)
                hist = ticker.history(period='1d')

                if not hist.empty:
                    stock_rates.append({
                        "stock": stock,
                        "price": round(float(hist['Close'].iloc[-1]), 2),
                    })
                    break

            except Exception as e:
                if attempt == max_retries - 1:
                    stock_rates.append({
                        "ticker": stock,
                        "error": str(e)
                    })
                time.sleep(1)

    return stock_rates


def get_phone_number(filename: str)-> Dict[str, Any]:
    """Функция читающая excel файл, и ищет информацию по транзакции, в которой указан номер телефона"""
    try:
        df = pd.read_excel(filename)
    except Exception as error:
        raise Exception(f'Ошибка при чтении файла: {str(error)}')

    pattern = r'\+[\d()\s-]+'
    result = []

    df_open = df[
        ['Дата операции',
         'Дата платежа',
         'Номер карты',
         'Статус',
         'Сумма операции',
         'Валюта операции',
         'Сумма платежа',
         'Валюта платежа',
         'Категория',
         'Описание'
         ]
    ]

    df_open = df_open.fillna('Не определено')
    for _, value in df_open.iterrows():
        search_info = re.search(pattern, value['Описание'])
        if search_info:
            answer_info = {
                'Дата операции': f'{value['Дата операции']}',
                'Дата платежа': f'{value['Дата платежа']}',
                'Номер карты': f'{value['Номер карты']}',
                'Статус': f'{value['Статус']}',
                'Сумма операции': f'{value['Сумма операции']}',
                'Валюта операции': f'{value['Валюта операции']}',
                'Сумма платежа': f'{value['Сумма платежа']}',
                'Валюта платежа': f'{value['Валюта платежа']}',
                'Категория': f'{value['Категория']}',
                'Описание': f'{value['Описание']}'
            }
            result.append(answer_info)


    return result