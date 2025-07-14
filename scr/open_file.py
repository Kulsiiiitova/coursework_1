import json

import pandas as pd


def read_excel_file(path_file: str) -> pd.DataFrame:
    try:
        excel_data = pd.read_excel(path_file)
        return excel_data
    except FileNotFoundError as e:
        print(f"Произошла ошибка открытия файла: {e}")
        return pd.DataFrame()


def creating_json_file(data, name_file):
    with open(name_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
