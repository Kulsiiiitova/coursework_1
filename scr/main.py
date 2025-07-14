from open_file import creating_json_file, read_excel_file
from views import (get_cashback, get_greetings, get_info_card, get_info_currencies, get_info_stocks, get_json_answer,
                   get_sum_transaction, get_top_transactions)


def main():
    print_json = {}
    date = input("Введите дату в формате YYYY-MM-DD HH:MM:SS: ")
    excel_data = read_excel_file("data/operations.xls")
    df_data = get_json_answer(excel_data, date)
    greeting = get_greetings(date)
    print_json["greeting"] = greeting
    cards = get_info_card(df_data)
    print_json["cards"] = []
    for i in cards:
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
    print_json["currency_rates"] = get_info_currencies()
    print_json["stock_prices"] = get_info_stocks()

    creating_json_file(print_json, "data/views_output.json")


if __name__ == "__main__":
    main()
