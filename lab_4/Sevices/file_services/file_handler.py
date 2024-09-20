
import json
import logging
from Model.serialize import Serializable


class FileHandler():
    """
    Service for serializing data in a file system in json format
    """

    def __init__(self, in_path: str, out_path: str):
        self.in_path = in_path
        self.out_path = out_path

    def read(self) -> Serializable:
        """
        Reading data from a json format file
        and presenting it in serializable form

        Returns:
            serialisable data (Serialiazable)
        """
        try:
            with open(self.in_path, mode = "r", encoding="utf-8") as f:
                return Serializable(**json.load(f))
        except Exception as e:
            logging.error(f"[FileHandler]: error read file: {e}")
    
    def write(self, data: Serializable):
        """
        Serializes data into a json file format

        Args:
            data (Serializable): data in serializable format
        """
        try:
            with open(self.out_path, mode = "w", encoding="utf-8") as f:
                json.dump(data.__dict__, f)
        except Exception as e:
            logging.error(f"[FileHandler]: error write file: {e}")