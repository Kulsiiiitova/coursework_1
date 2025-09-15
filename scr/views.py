import datetime
import json
import os
import logging
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
API_KEY_STONCKS = os.getenv("API_KEY_STONCKS")


logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/logs_views.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_json_answer(dataframe: pd.DataFrame, date: str) -> pd.DataFrame:
    """Функция, для вывода данных об операциях за срок с начала месяца до указанной даты"""
    try:
        finish_date = datetime.datetime.strptime(date, "%Y-%m-%d  %H:%M:%S")
        start_date = finish_date.replace(day=1)
        dataframe["Дата операции"] = pd.to_datetime(dataframe["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        filtered = dataframe[(dataframe["Дата операции"] >= start_date) & (dataframe["Дата операции"] <= finish_date)]
        logger.info(f"Данные успешно отфитрованы с {start_date} до {finish_date}")
        return filtered
    except ValueError as e:
        logger.error(f"Произошла ошибка формата даты: {e}")
        return pd.DataFrame()
    except TypeError as e:
        logger.error(f"Произошла ошибка типы данных: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        return pd.DataFrame()


def get_info_currencies() -> list[dict]:
    """Функция, которая выводит данные о валютах"""
    result = []
    currencies = []
    try:
        with open("user_setting.json") as f:
            data = json.load(f)
            user_currencies = data["user_currencies"]
            logger.info(f"Получение курсов валют для: {user_currencies}")
            for currency in user_currencies:
                try:
                    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={'RUB'}&base={currency}"
                    headers = {"apikey": API_KEY}
                    response = requests.get(url, headers)
                    result.append(response.json())
                    logger.debug(f"Получены данные по валюте {currency}")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Ошибка при запросе курса {currency}: {e}")
                    continue
        for i in result:
            try:
                currencies.append({"currency": i["base"], "rate": i["rates"]["RUB"]})
            except (KeyError, TypeError) as e:
                logger.error(f"Ошибка обработки ответа API: {e}")
    except FileNotFoundError as e:
        logger.error(f"Произошла ошибка открытия файла: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Произошла ошибка: {e}")
    except KeyError as e:
        logger.error(f"Отсутствует ключ 'user_currencies' {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
    return currencies


def get_info_stocks() -> list[dict]:
    """Функция, которая выводит данные об акциях"""
    result = []
    stoncks = []
    try:
        with open("user_setting.json") as f:
            data = json.load(f)
            user_stocks = data["user_stocks"]
            logger.info(f"Получение данных по акциям: {user_stocks}")
            for stock in user_stocks:
                try:
                    url = (
                        f"https://api.twelvedata.com/time_series?apikey={API_KEY_STONCKS}&interval=1min&symbol={stock}"
                    )
                    response = requests.get(url)
                    result.append(response.json())
                    logger.debug(f"Получены данные по акции {stock}")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Ошибка при запросе акции {stock}: {e}")
                    continue
        for i in result:
            try:
                stoncks.append({"stock": i["meta"]["symbol"], "price": i["values"][0]["open"]})
            except (KeyError, TypeError) as e:
                logger.error(f"Ошибка обработки ответа API: {e}")
    except FileNotFoundError as e:
        logger.error(f"Произошла ошибка открытия файла: {e}")
    except json.JSONDecodeError as e:
        logger.error(f"Произошла ошибка: {e}")
    except KeyError as e:
        logger.error(f"Отсутствует ключ 'user_stocks' {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
    return stoncks


def get_greetings(date: str) -> str:
    """Функция, которая приветствует пользователя в зависимости от времени"""
    try:
        date_string = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_hour = date_string.hour
        if 0 <= date_hour < 6:
            return "Доброй ночи"
        elif 6 <= date_hour < 12:
            return "Доброе утро"
        elif 12 <= date_hour < 18:
            return "Добрый день"
        elif 18 <= date_hour < 24:
            return "Добрый вечер"
        else:
            logger.warning(f"Некорректное значение часа: {date_hour}")
            return "Неправильный формат времени"
    except ValueError as e:
        logger.error(f"Произошла ошибка формата даты: {e}")
    except TypeError as e:
        logger.error(f"Произошла ошибка типы данных: {e}")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")


def get_info_card(excel_data: pd.DataFrame) -> list:
    """Функция, которая выводит номера карт"""
    cards = excel_data.loc[excel_data["Номер карты"].notnull()]["Номер карты"]
    logger.info(f"Найдено {len(cards.unique())} уникальных карт")
    return cards.unique()


def get_sum_transaction(excel_data: pd.DataFrame, card: str) -> int:
    """Функция, которая выводит общую сумму"""
    excel_data = excel_data[excel_data["Номер карты"] == card]
    data = excel_data["Сумма операции"].map(lambda p: abs(p))
    logger.info(f"Общая сумма операций по карте {card}: {sum(data)}")
    return sum(data)


def get_top_transactions(excel_data: pd.DataFrame) -> pd.DataFrame:
    """Функция, которая выводит топ 5 операций"""
    data = excel_data.sort_values(by="Сумма операции", ascending=False)
    logger.info(f"Возвращаем топ 5 операций")
    return data.head()


def get_cashback(excel_data: pd.DataFrame, card: str) -> int:
    """Функция, которая выводит сумму кэшбека"""
    excel_data = excel_data[excel_data["Номер карты"] == card]
    data = excel_data.loc[excel_data["Кэшбэк"].notnull()]["Кэшбэк"].sum()
    logger.info(f"Общий кэшбек по карте {card}: {data}")
    return float(data)
