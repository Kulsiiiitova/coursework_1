import datetime
import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
API_KEY_STONCKS = os.getenv("API_KEY_STONCKS")


def get_json_answer(dataframe: pd.DataFrame, date: str) -> pd.DataFrame:
    """Функция, для вывода данных об операциях за срок с начала месяца до указанной даты"""
    try:
        finish_date = datetime.datetime.strptime(date, "%Y-%m-%d  %H:%M:%S")
        start_date = finish_date.replace(day=1)
        dataframe["Дата операции"] = pd.to_datetime(dataframe["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        filtered = dataframe[(dataframe["Дата операции"] >= start_date) & (dataframe["Дата операции"] <= finish_date)]
        return filtered
    except ValueError as e:
        print(f"Произошла ошибка формата даты: {e}")
        return pd.DataFrame()
    except TypeError as e:
        print(f"Произошла ошибка типы данных: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
        return pd.DataFrame()


def get_info_currencies() -> list[dict]:
    """Функция, которая выводит данные о валютах"""
    result = []
    currencies = []
    try:
        with open("user_setting.json") as f:
            data = json.load(f)
            user_currencies = data["user_currencies"]
            for currency in user_currencies:
                try:
                    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={'RUB'}&base={currency}"
                    headers = {"apikey": API_KEY}
                    response = requests.get(url, headers)
                    result.append(response.json())
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при запросе курса {currency}: {e}")
                    continue
        for i in result:
            try:
                currencies.append({"currency": i["base"], "rate": i["rates"]["RUB"]})
            except (KeyError, TypeError) as e:
                print(f"Ошибка обработки ответа API: {e}")
    except FileNotFoundError as e:
        print(f"Произошла ошибка открытия файла: {e}")
    except json.JSONDecodeError as e:
        print(f"Произошла ошибка: {e}")
    except KeyError as e:
        print(f"Отсутствует ключ 'user_currencies' {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    return currencies


def get_info_stocks() -> list[dict]:
    """Функция, которая выводит данные об акциях"""
    result = []
    stoncks = []
    try:
        with open("user_setting.json") as f:
            data = json.load(f)
            user_stocks = data["user_stocks"]
            for stock in user_stocks:
                try:
                    url = (
                        f"https://api.twelvedata.com/time_series?apikey={API_KEY_STONCKS}&interval=1min&symbol={stock}"
                    )
                    response = requests.get(url)
                    result.append(response.json())
                except requests.exceptions.RequestException as e:
                    print(f"Ошибка при запросе акции {stock}: {e}")
                    continue
        for i in result:
            try:
                stoncks.append({"stock": i["meta"]["symbol"], "price": i["values"][0]["open"]})
            except (KeyError, TypeError) as e:
                print(f"Ошибка обработки ответа API: {e}")
    except FileNotFoundError as e:
        print(f"Произошла ошибка открытия файла: {e}")
    except json.JSONDecodeError as e:
        print(f"Произошла ошибка: {e}")
    except KeyError as e:
        print(f"Отсутствует ключ 'user_stocks' {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
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
            return "Неправильный формат времени"
    except ValueError as e:
        print(f"Произошла ошибка формата даты: {e}")
    except TypeError as e:
        print(f"Произошла ошибка типы данных: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


def get_info_card(excel_data: pd.DataFrame) -> list:
    """Функция, которая выводит номера карт"""
    cards = excel_data.loc[excel_data["Номер карты"].notnull()]["Номер карты"]
    return cards.unique()


def get_sum_transaction(excel_data: pd.DataFrame, card: str) -> int:
    """Функция, которая выводит общую сумму"""
    excel_data = excel_data[excel_data["Номер карты"] == card]
    data = excel_data["Сумма операции"].map(lambda p: abs(p))
    return sum(data)


def get_top_transactions(excel_data: pd.DataFrame) -> pd.DataFrame:
    """Функция, которая выводит топ 5 операций"""
    data = excel_data.sort_values(by="Сумма операции", ascending=False)
    return data.head()


def get_cashback(excel_data: pd.DataFrame, card: str) -> int:
    """Функция, которая выводит сумму кэшбека"""
    excel_data = excel_data[excel_data["Номер карты"] == card]
    data = excel_data.loc[excel_data["Кэшбэк"].notnull()]["Кэшбэк"].sum()
    return float(data)
