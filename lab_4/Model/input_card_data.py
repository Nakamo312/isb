
from Model.serialize import Serializable


class InCardData(Serializable):
    """
    Represents data about a card for input into the card validation process.

    This class inherits from Serializable and provides a specific structure for card data input.
    It stores the BIN (Bank Identification Number) as a list of strings, the card number's hash, 
    the last digits of the card number, and the total length of the card number.

    Attributes:
        BIN (list[str]): The Bank Identification Number, represented as a list of strings.
        hash_number (str): The hash of the card number.
        last_digits (int): The last digits of the card number.
        length (int): The total length of the card number.
    """
    
    def __init__(self, bin: list[str], hash_number: str, last_digits: int, length:int):
        """
        Initializes an InCardData object with card data for input.

        Args:
            BIN (list[str]): The Bank Identification Number, represented as a list of strings.
            hash_number (str): The hash of the card number.
            last_digits (int): The last digits of the card number.
            length (int): The total length of the card number.
        """
        super().__init__(BIN=bin, hash_number=hash_number, last_digits=last_digits, length=length)