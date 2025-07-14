from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def report_to_file(name_file):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(name_file, "w") as f:
                f.write(str(result))
            return result

        return wrapper

    return decorator


@report_to_file("data/spending_by_category.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, для создания отчет по тратам по определенной категории"""
    if date is not None:
        finish_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        finish_date = datetime.now().replace(microsecond=0)
    start_date = finish_date - relativedelta(months=3)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= finish_date)
        & (transactions["Категория"] == category)
    ]
    return filtered
