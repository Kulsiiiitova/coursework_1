from open_file import creating_json_file, read_excel_file
from views import (get_cashback, get_greetings, get_info_card, get_info_currencies, get_info_stocks, get_json_answer,
                   get_sum_transaction, get_top_transactions)
import logging

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/logs_main.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main() -> None:
    """ Главная функция, показывающая функционал программы"""
    print_json = {}
    date = input("Введите дату в формате YYYY-MM-DD HH:MM:SS: ")
    logger.info(f"Получена дата от пользователя: {date}")
    excel_data = read_excel_file("data/operations.xls")
    logger.info(f"Прочитано {len(excel_data)} записей из файла")
    df_data = get_json_answer(excel_data, date)
    greeting = get_greetings(date)
    print_json["greeting"] = greeting
    logger.info(f"Сформировано приветствие: {greeting}")
    cards = get_info_card(df_data)
    logger.info(f"Найдено {len(cards)} карт")
    print_json["cards"] = []
    for i in cards:
        logger.debug(f"Обработка карты: {i}")
        sum_transaction = get_sum_transaction(df_data, i)
        cashback = get_cashback(df_data, i)
        print_json["cards"].append({"last_digits": i[1::], "total_spent": sum_transaction, "cashback": cashback})
    top_transactions = get_top_transactions(df_data)
    print_json["top_transactions"] = []
    for index, row in top_transactions.iterrows():
        print_json["top_transactions"].append(
            {
                "date": row["Дата платежа"],
                "amount": row["Сумма платежа"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    logger.info(f"Найдено {len(cards)} карт")
    print_json["currency_rates"] = get_info_currencies()
    logger.info("Получение данных по акциям")
    print_json["stock_prices"] = get_info_stocks()
    logger.info("Сохранение результатов в JSON файл")
    creating_json_file(print_json, "data/views_output.json")
    logger.info("Программа успешно завершена")


if __name__ == "__main__":
    main()
