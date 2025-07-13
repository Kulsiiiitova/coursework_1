from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta
from functools import wraps
from open_file import read_excel_file


def report_to_file(name_file):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # result.to_csv(name_file, index=False)
            with open(name_file, 'w') as f:
                f.write(str(result))
            return result
        return wrapper
    return decorator


@report_to_file('data/spending_by_category.csv')
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """ Функция, для создания отчет по тратам по определенной категории"""
    if date != None:
        finish_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    else:
        finish_date = datetime.now().replace(microsecond=0)
    start_date = finish_date - relativedelta(months=3)
    df = transactions.loc[(
                               pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S') >= start_date
                       ) & (
                               pd.to_datetime(transactions['Дата операции'], format='%d.%m.%Y %H:%M:%S') <= finish_date
                       )]
    df_category = df[df['Категория'] == category]
    print(df.loc[:, ['Дата операции', 'Округление на инвесткопилку']])
    return df_category
