import datetime
import logging
import pandas as pd

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/logs_services.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_cashback_categories(data: pd.DataFrame, year: int, month: int) -> dict[str, int]:
    """ Функция, которая выводит кешбэк по категориям"""
    logger.info(f"Начало расчета кешбэка за {month}.{year}")
    categories = {}
    for index, i in data.iterrows():
        date = datetime.datetime.strptime(i["Дата платежа"], "%d.%m.%Y")
        if date.year == year and date.month == month:
            if i["Категория"] not in categories:
                if i["Сумма операции с округлением"] // 100 != 0:
                    categories[i["Категория"]] = i["Сумма операции с округлением"] // 100
            else:
                categories[i["Категория"]] += i["Сумма операции с округлением"] // 100
    return categories
    logger.debug(f"Кешбэк по категориям: {categories}")