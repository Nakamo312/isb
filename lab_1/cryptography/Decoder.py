from typing import Any
from cryptography.alphabet import Alphabet


class Decoder:
    """
    A class that implements text encryption and decryption based on a replacement algorithm
    """

    def __init__(self, text: str, set1: Alphabet = None, set2: Alphabet = None):
        self.replaced = list()
        self.table = list()
        self.set1 = set1
        self.set2 = set2
        self.text = list(text)

    def compare_alphabets(self) -> None:
        """
        А function that matches one alphabet to another, based on frequency analysis
        """
        set1 = [i[0] for i in self.set1.sorted_set()]
        set2 = [i[0] for i in self.set2.sorted_set()]
        result_set = zip(set1, set2)
        self.table = result_set

    def __replace_sym(self, sym1: chr, sym2: chr) -> None:
        for i in range(len(self.text)):
            if self.text[i] == sym1 and not (i in self.replaced):
                self.text[i] = sym2
                self.replaced.append(i)
                self.table.append((sym1, sym2))

    def decode(self, table: tuple[Any, Any] = None) -> str:
        """
        Encryption using a specified lookup table
        """
        if table:
            for char in table:
                self.__replace_sym(char[0], char[1])
            return "".join(self.text)
        self.compare_alphabets()
        for char in self.table:
            self.__replace_sym(char[0], char[1])
        return "".join(self.text)

    def get_key(self) -> dict[str | str]:
        """
        Return lookup table
        """
        return dict(self.table)

    def caesars_cipher(self, key: int, lng="ru") -> str:
        """
        Encrypting the original text by shifting "key"
        """
        alphabet2 = []
        match lng:
            case "ru":
                start = "а"
                end = "я"
            case "eng":
                start = "a"
                end = "z"
        alphabet1 = [chr(i) for i in range(ord(start), ord(end) + 1)]
        for letter in alphabet1:
            if letter.isalpha():
                alphabet2.append(chr((ord(letter) + key - ord(start)) % len(alphabet1) + ord(start)))
        table = zip([i[0] for i in alphabet1], alphabet2)
        return self.decode(table)
