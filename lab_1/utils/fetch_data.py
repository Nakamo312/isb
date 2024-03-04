import logging
from typing import Optional


def read_from_file(path: str) -> Optional[str | None]:
    '''This method reads file data from txt\n
        '''
    try:
        with open(path, 'r', encoding="utf-8") as txt:
            result: str = ""
            for line in txt:
                result += line
            return result
    except FileNotFoundError:
        logging.error(f"FILE '{path}' does not exist")
