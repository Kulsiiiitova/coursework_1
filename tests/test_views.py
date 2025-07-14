import numpy as np
import pandas as pd
import pytest

from scr.views import (get_cashback, get_greetings, get_info_card, get_json_answer, get_sum_transaction,
                       get_top_transactions)


@pytest.fixture
def transaction_test():
    """Фикстура с корректными тестовыми данными"""
    return pd.DataFrame(
        {
            "Дата операции": [
                "01.05.2025 10:00:00",
                "15.05.2025 12:30:00",
                "31.05.2025 23:59:59",
                "01.06.2025 00:00:00",
                "30.04.2025 20:00:00",
            ],
            "Сумма операции": [100, 200, 300, 400, 500],
        }
    )


def test_normal_case(transaction_test):
    result = get_json_answer(transaction_test, "2025-05-31 23:59:59")
    assert len(result) == 2


def test_get_greetings_night():
    assert get_greetings("2023-01-01 00:00:00") == "Доброй ночи"
    assert get_greetings("2023-01-01 05:59:59") == "Доброй ночи"


def test_get_greetings_morning():
    assert get_greetings("2023-01-01 06:00:00") == "Доброе утро"
    assert get_greetings("2023-01-01 11:59:59") == "Доброе утро"


def test_get_greetings_day():
    assert get_greetings("2023-01-01 12:00:00") == "Добрый день"
    assert get_greetings("2023-01-01 17:59:59") == "Добрый день"


def test_get_greetings_evening():
    assert get_greetings("2023-01-01 18:00:00") == "Добрый вечер"
    assert get_greetings("2023-01-01 23:59:59") == "Добрый вечер"


def test_get_greetings_invalid_format(capsys):
    assert get_greetings("invalid-date") is None
    captured = capsys.readouterr()
    assert "Произошла ошибка формата даты" in captured.out

    assert get_greetings(123) is None
    captured = capsys.readouterr()
    assert "Произошла ошибка типы данных" in captured.out


@pytest.fixture
def sample_data():
    data = {
        "Номер карты": ["1234", "5678", "1234", "1011", "1011", "5678"],
        "Сумма операции": [100, -200, 300, 400, 500, -600],
        "Кэшбэк": [1.0, None, 2.0, 3.0, None, 4.0],
    }
    return pd.DataFrame(data)


def test_get_info_card(sample_data):
    result = get_info_card(sample_data)
    expected = np.array(["1234", "5678", "1011"], dtype=object)
    np.testing.assert_array_equal(result, expected)


def test_get_info_card_empty():
    empty_df = pd.DataFrame(columns=["Номер карты", "Сумма операции", "Кэшбэк"])
    result = get_info_card(empty_df)
    assert len(result) == 0


def test_get_sum_transaction(sample_data):
    assert get_sum_transaction(sample_data, "1234") == 400
    assert get_sum_transaction(sample_data, "5678") == 800


def test_get_sum_transaction_nonexistent_card(sample_data):
    assert get_sum_transaction(sample_data, "0000") == 0


def test_get_top_transactions(sample_data):
    result = get_top_transactions(sample_data)
    assert len(result) == 5
    print(result.iloc[0]["Сумма операции"]) == 500
    assert result.iloc[1]["Сумма операции"] == 400
    assert result.iloc[2]["Сумма операции"] == 300
    assert result.iloc[3]["Сумма операции"] == 100
    assert result.iloc[4]["Сумма операции"] == -200


def test_get_top_transactions_less_than_5():
    small_data = pd.DataFrame({"Сумма операции": [100, 200], "Номер карты": ["1", "2"], "Кэшбэк": [0, 0]})
    result = get_top_transactions(small_data)
    assert len(result) == 2


def test_get_cashback(sample_data):
    assert get_cashback(sample_data, "1234") == 3.0
    assert get_cashback(sample_data, "5678") == 4.0
    assert get_cashback(sample_data, "1011") == 3.0


def test_get_cashback_nonexistent_card(sample_data):
    assert get_cashback(sample_data, "0000") == 0.0
