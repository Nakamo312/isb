from typing import Any


class Alphabet:
    """
    Сlass storing alphabet frequency table
    """
    def __init__(self, data: str = None, **kwargs):
        if data:
            self.data: str = data
            self.set: set = set(data)
            self.char_freq: dict = {}
            self.__calc_freq()
        if kwargs:
            self.char_freq = dict()
            for char, freq in kwargs.items():
                self.char_freq[char] = freq

    def __calc_freq(self):
        list(map(lambda char: self.char_freq.update({char: self.data.count(char) / len(self.data)}), self.set))

    def sorted_set(self) -> list[tuple[Any, Any]]:
        return sorted(self.char_freq.items(), key=lambda item: item[1], reverse=True)
