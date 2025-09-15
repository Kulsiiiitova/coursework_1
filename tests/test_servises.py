import pandas as pd
import pytest

from scr.services import get_cashback_categories


@pytest.fixture
def sample_data():
    data = {
        "Дата платежа": ["01.01.2023", "15.01.2023", "01.02.2023", "15.02.2023", "01.01.2023"],
        "Категория": ["Супермаркеты", "АЗС", "Супермаркеты", "Рестораны", "АЗС"],
        "Сумма операции с округлением": [150, 250, 350, 450, 90],
    }
    return pd.DataFrame(data)


def test_get_cashback_categories_single_month(sample_data):
    result = get_cashback_categories(sample_data, 2023, 1)
    expected = {"Супермаркеты": 1, "АЗС": 2}
    assert result == expected


def test_get_cashback_categories_different_month(sample_data):
    result = get_cashback_categories(sample_data, 2023, 2)
    expected = {"Супермаркеты": 3, "Рестораны": 4}
    assert result == expected


def test_get_cashback_categories_no_matches(sample_data):
    result = get_cashback_categories(sample_data, 2022, 1)
    assert result == {}
