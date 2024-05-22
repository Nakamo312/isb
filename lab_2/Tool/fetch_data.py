import json
import logging


def txt_read(file_path: str) -> str:
    """
    read data from txt file
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
            return data
    except Exception as e:
        logging.error(f"Failed to read file{e}")


def json_write(file_path: str, **data) -> None:
    """
    write dict-format data to json file
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error(f"Failed to write to a file {e}")
