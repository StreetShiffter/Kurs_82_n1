from unittest.mock import MagicMock, mock_open, patch

import pandas as pd

from src.utils import (get_cards_with_spend, get_currency, get_date_interval, get_path_to_file_and_period,
                       get_phone_number, get_stock, get_top_transactions, greet_func)


@patch("src.utils.datetime")
def test_greet_func(mock_datetime):
    mock_datetime.now.return_value.hour = 10
    assert greet_func() == "Доброе утро"

    mock_datetime.now.return_value.hour = 15
    assert greet_func() == "Добрый день"

    mock_datetime.now.return_value.hour = 20
    assert greet_func() == "Добрый вечер"

    mock_datetime.now.return_value.hour = 2
    assert greet_func() == "Доброй ночи"


def test_get_date_interval():
    result = get_date_interval("2023-01-15 12:00:00")
    assert result == ["01.01.2023 12:00:00", "15.01.2023 12:00:00"]


@patch("src.utils.logger.error")
def test_get_date_interval_invalid_format(mock_error):
    try:
        get_date_interval("invalid-date")
        assert False, "Expected ValueError"
    except ValueError:
        pass
    # Проверяем, что ошибка была залогирована
    mock_error.assert_called_once()


@patch("pandas.read_excel")
def test_get_path_to_file_and_period(mock_read_excel, test_df, test_period):
    mock_read_excel.return_value = test_df
    result = get_path_to_file_and_period("test.xlsx", test_period)
    assert len(result) == 2
    assert result.iloc[0]["Номер карты"] == "1234****5678"


def test_get_cards_with_spend(test_df):
    test_df["Дата операции"] = pd.to_datetime(test_df["Дата операции"], dayfirst=True)
    result = get_cards_with_spend(test_df)
    assert len(result) == 1
    assert result[0]["last_digits"] == "12345678"


def test_get_top_transactions(test_df):
    test_df["Дата операции"] = pd.to_datetime(test_df["Дата операции"], dayfirst=True)
    result = get_top_transactions(test_df, 1)
    assert len(result) == 1
    assert float(result[0]["amount"]) == 200


@patch("requests.get")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
def test_get_currency(mock_file, mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"query": {"from": "USD"}, "result": 75.5}
    mock_get.return_value = mock_response

    result = get_currency("test.json")
    assert len(result) == 2
    assert result[0]["currency"] == "USD"


@patch("yfinance.Ticker")
@patch("builtins.open", new_callable=mock_open)
def test_get_stock(mock_file, mock_ticker, mock_stock_data):
    mock_file.return_value.read.return_value = mock_stock_data
    mock_hist = MagicMock()
    mock_hist.empty = False
    mock_hist.__getitem__.return_value = MagicMock(iloc=MagicMock(return_value=150))
    mock_ticker.return_value.history.return_value = mock_hist

    result = get_stock("test.json")
    assert len(result) == 1
    assert result[0]["stock"] == "AAPL"


@patch("pandas.read_excel")
def test_get_phone_number(mock_read_excel, test_df):
    mock_read_excel.return_value = test_df

    result = get_phone_number("test.xlsx")

    # Проверяем основные утверждения
    assert len(result) == 1
    assert "+79123456789" in result[0]["Описание"]

    # Дополнительные проверки структуры результата
    expected_keys = {
        "Дата операции",
        "Дата платежа",
        "Номер карты",
        "Статус",
        "Сумма операции",
        "Валюта операции",
        "Сумма платежа",
        "Валюта платежа",
        "Категория",
        "Описание",
    }
    assert set(result[0].keys()) == expected_keys
