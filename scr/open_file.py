import json
import logging
import pandas as pd

logger = logging.getLogger("open_file")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/logs_open_file.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_excel_file(path_file: str) -> pd.DataFrame:
    """ Функция используется для открытия EXCEL-файла"""
    try:
        excel_data = pd.read_excel(path_file)
        logger.info(f"Файл успешно прочитан.")
        return excel_data
    except FileNotFoundError as e:
        logger.error(f"Произошла ошибка открытия файла: {e}")
        return pd.DataFrame()


def creating_json_file(data: pd.DataFrame, name_file: str) -> None:
    """ Функция, которая записывает данные в EXCEL-файл"""
    with open(name_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Данные успешно записаны в файл {name_file}")
