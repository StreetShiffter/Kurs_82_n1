import json
from unittest.mock import MagicMock, patch

import pytest
from pandas import DataFrame

from src.services import info_transaction_filter_phone


# Тест основной функции
@patch("src.services.get_phone_number")
@patch("src.services.logger.info")
def test_info_transaction_filter_phone(mock_logger, mock_get_phone, mock_phone_data):
    mock_get_phone.return_value = mock_phone_data
    mock_df = MagicMock(spec=DataFrame)
    result = info_transaction_filter_phone(mock_df)
    mock_get_phone.assert_called_once_with(mock_df)
    parsed_result = json.loads(result)
    assert isinstance(parsed_result, list)
    assert len(parsed_result) == 1
    assert "+79123456789" in parsed_result[0]["Описание"]

    # Проверяем что было залогировано
    mock_logger.assert_called_once_with('Сформирован JSON-ответ "Сервисы"')


# Тест для обработки ошибок
@patch("src.services.get_phone_number")
def test_info_transaction_filter_phone_error(mock_get_phone):
    mock_get_phone.side_effect = Exception("Test error")
    mock_df = MagicMock(spec=DataFrame)

    with pytest.raises(Exception) as exc_info:
        info_transaction_filter_phone(mock_df)

    assert "Test error" in str(exc_info.value)
