from datetime import datetime
from functools import wraps
from typing import Optional
import logging
import pandas as pd
from dateutil.relativedelta import relativedelta

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/logs_reports.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_to_file(name_file: str):
    """ Декоратор, который записывает данные в файл"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Начало выполнения функции {func.__name__}")
            result = func(*args, **kwargs)
            with open(name_file, "w", encoding='utf-8') as f:
                f.write(str(result))
            logger.info(f"Результат успешно записан в файл {name_file}")
            return result

        return wrapper

    return decorator


@report_to_file("data/spending_by_category.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, для создания отчет по тратам по определенной категории"""
    filtered = {}
    if date is not None:
        finish_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    else:
        finish_date = datetime.now().replace(microsecond=0)
    start_date = finish_date - relativedelta(months=3)
    logger.info(f"Период анализа: с {start_date} по {finish_date}")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filtered = transactions[
        (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= finish_date)
        & (transactions["Категория"] == category)
    ]
    return filtered
