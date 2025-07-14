import datetime


def get_cashback_categories(data, year, month):
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
