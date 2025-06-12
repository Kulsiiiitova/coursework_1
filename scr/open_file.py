import pandas as pd


def read_excel_file(path_file: str):
    excel_data = pd.read_excel(path_file)
    # dict_list = excel_data.to_dict(orient="records")
    return excel_data