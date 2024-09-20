

from Model.serialize import Serializable


class OutCardData(Serializable):
    """
    Represents data about a card, including its number, hash, and validation status.

    This class inherits from Serializable and provides a specific structure for card data.
    It stores the card number, its hash, and whether it is considered valid.

    Attributes:
        number (str): The card number.
        hash_number (str): The hash of the card number.
        is_valid (bool): Whether the card is considered valid.
    """

    def __init__(self, number: str, hash_number: str, is_valid: bool):
        """
        Initializes an OutCardData object with card number, hash, and validation status.

        Args:
            number (str): The card number.
            hash_number (str): The hash of the card number.
            is_valid (bool): Whether the card is considered valid.
        """
        super().__init__(number=number, hash_number=hash_number, is_valid=is_valid)