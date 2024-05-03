import logging
import json
import os
from typing import Optional


def read_from_txt(path: str) -> Optional[str | None] | None:
    """
    Reads file data from txt\n
    """
    try:
        with open(path, 'r', encoding="utf-8") as txt:
            result: str = ""
            for line in txt:
                result += line
            return result
    except FileNotFoundError:
        logging.error(f"FILE '{path}' does not exist")
    except Exception as e:
        logging.error(e)


def write_to_txt(text: str, path: str) -> None:
    """
    Write data to txt file\n
    """
    try:
        with open(path, 'w', encoding="utf-8") as txt:
            txt.write(text)

    except Exception as e:
        logging.error(e)


def json_read(path: str) -> dict[str | float] | None:
    """
    Reads file data from json\n
    """
    try:
        with open(path, 'r', encoding="utf-8") as js:
            data = json.load(js)
            return data
    except FileNotFoundError:
        logging.error(f"FILE '{path}' does not exist")
    except Exception as e:
        logging.error(e)


def json_write(data: dict, path: str) -> None:
    """
    Reads file data from json\n
    """
    try:
        with open(path, 'w', encoding="utf-8") as js:
            json.dump(data, js)
    except FileNotFoundError:
        logging.error(f"FILE '{path}' does not exist")
    except Exception as e:
        logging.error(e)
