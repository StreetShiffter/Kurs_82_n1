import json
from config import PATH_FILE
from pandas import DataFrame
from typing import List, Dict, Any
from src.utils import get_phone_number

def info_transaction_filter_phone(PATH_FILE: DataFrame)-> List[Dict]:
    """Функция принимающаяя транзакции, отфильтровывает по номеру и формирует JSON"""
    data = get_phone_number(PATH_FILE)

    json_data_services = json.dumps(data, ensure_ascii=False, indent=4)
    return json_data_services

