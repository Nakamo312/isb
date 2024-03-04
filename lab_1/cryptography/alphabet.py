from typing import Any


class Alphabet:
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


char_freq = {
    " ": 0.128675,
    "О": 0.096456,
    "И": 0.075312,
    "Е": 0.072292,
    "А": 0.064841,
    "Н": 0.061820,
    "Т": 0.061619,
    "С": 0.051953,
    "Р": 0.040677,
    "В": 0.039267,
    "М": 0.029803,
    "Л": 0.029400,
    "Д": 0.026983,
    "Я": 0.026379,
    "К": 0.025977,
    "П": 0.024768,
    "З": 0.015908,
    "Ы": 0.015707,
    "Ь": 0.015103,
    "У": 0.013290,
    "Ч": 0.011679,
    "Ж": 0.010673,
    "Г": 0.009867,
    "Х": 0.008659,
    "Ф": 0.007249,
    "Й": 0.006847,
    "Ю": 0.006847,
    "Б": 0.006645,
    "Ц": 0.005034,
    "Ш": 0.004229,
    "Щ": 0.003625,
    "Э": 0.002416,
    "Ъ": 0.000000,
}
