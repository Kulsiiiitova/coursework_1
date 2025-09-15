from unittest.mock import patch

import pandas as pd
import pytest

from scr.reports import spending_by_category


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "Дата операции": [
                "08.06.2025 19:37:43",
                "08.06.2025 11:53:58",
                "07.06.2025 17:50:04",
                "01.03.2025 12:00:00",
            ],
            "Категория": ["Переводы", "Переводы", "Другое", "Переводы"],
            "Сумма операции": [500.0, 230.0, 323.5, 100.0],
        }
    )


def test_spending_by_category_filter(sample_data):
    with patch("scr.reports.report_to_file"):
        result = spending_by_category(sample_data, "Переводы")

    assert len(result) == 2
    assert all(result["Категория"] == "Переводы")
    assert "Дата операции" in result.columns


def test_spending_by_category_date_filtering(sample_data):
    with patch("scr.reports.report_to_file"):
        old_date = "2025-04-01 00:00:00"
        result = spending_by_category(sample_data, "Переводы", date=old_date)

    assert len(result) == 1
