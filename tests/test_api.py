import unittest
from unittest.mock import mock_open, patch

from scr.views import get_info_currencies, get_info_stocks

# Тестовые данные
CURRENCIES_JSON = '{"user_currencies": ["USD", "EUR"]}'
STOCKS_JSON = '{"user_stocks": ["AAPL", "TSLA"]}'

# Моки для успешных ответов API
SUCCESS_CURRENCY_RESPONSES = [{"base": "USD", "rates": {"RUB": 75.50}}, {"base": "EUR", "rates": {"RUB": 85.25}}]

SUCCESS_STOCK_RESPONSES = [
    {"meta": {"symbol": "AAPL"}, "values": [{"open": "150.50"}]},
    {"meta": {"symbol": "TSLA"}, "values": [{"open": "700.25"}]},
]


# Тесты для get_info_currencies
def test_get_info_currencies_success():
    with patch("builtins.open", mock_open(read_data=CURRENCIES_JSON)):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [
                unittest.mock.Mock(json=lambda: SUCCESS_CURRENCY_RESPONSES[0]),
                unittest.mock.Mock(json=lambda: SUCCESS_CURRENCY_RESPONSES[1]),
            ]

            result = get_info_currencies()

            assert len(result) == 2
            assert result[0] == {"currency": "USD", "rate": 75.50}
            assert result[1] == {"currency": "EUR", "rate": 85.25}


def test_get_info_stocks_success():
    with patch("builtins.open", mock_open(read_data=STOCKS_JSON)):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = [
                unittest.mock.Mock(json=lambda: SUCCESS_STOCK_RESPONSES[0]),
                unittest.mock.Mock(json=lambda: SUCCESS_STOCK_RESPONSES[1]),
            ]

            result = get_info_stocks()

            assert len(result) == 2
            assert result[0] == {"stock": "AAPL", "price": "150.50"}
            assert result[1] == {"stock": "TSLA", "price": "700.25"}
