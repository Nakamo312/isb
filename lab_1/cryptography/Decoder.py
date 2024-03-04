from typing import Any

from lab_1.cryptography.alphabet import Alphabet


class Decoder:
    def __init__(self, set1: Alphabet, set2: Alphabet, text: str):
        self.replaced = list()
        self.table = list()
        self.set1 = set1
        self.set2 = set2
        self.text = list(text)

    def compare_alphabets(self):
        set1 = [i[0] for i in self.set1.sorted_set()]
        set2 = [i[0] for i in self.set2.sorted_set()]
        result_set = zip(set1, set2)
        self.table = result_set

    def __replace_sym(self, sym1: chr, sym2: chr):
        for i in range(len(self.text)):
            if self.text[i] == sym1 and not (i in self.replaced):
                self.text[i] = sym2
                self.replaced.append(i)

    def decode(self, table: tuple[Any, Any] = None):
        if table:
            for char in table:
                self.__replace_sym(char[0], char[1])
            return "".join(self.text)
        for char in self.table:
            self.__replace_sym(char[0], char[1])
        return "".join(self.text)
