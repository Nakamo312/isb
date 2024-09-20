from typing import Any, Iterator, Union, List

from ..event_services.event_track import Tracker

class GeneratorNDigitNumbers(Iterator):
    """
    Service for generating a sequence of N numbers
    with tracked progress, with the ability to specify
    initial and ending sequences of numbers
    """

    def __init__(self, start_seq: Union[List[int], int], end_seq: Union[List[int], int], length: int):
        """
        Args:
            start_seq (Union[List[int], int]): sequence of digits in high order
            end_seq (Union[List[int], int]): sequence of digits in low order
            length (int): generated sequence length
        """
        self.start_seq: Iterator[int] = iter(start_seq) if isinstance(start_seq, list) else iter([start_seq])
        self.end_seq: Iterator[int] = iter(end_seq) if isinstance(end_seq, list) else iter([end_seq])
        self.current_start_seq: int = next(self.start_seq)
        self.current_end_seq: int = next(self.end_seq)
        self.length: int = length
        self.count: int = 0
        self.length_generate_seq: int = length - (len(str(self.current_start_seq)) + len(str(self.current_end_seq)))

    def __iter__(self) -> 'GeneratorNDigitNumbers':
        return self
    
    @Tracker()
    def __next__(self) -> int:
        if len(str(self.count)) > self.length_generate_seq:
            try:
                self.current_end_seq = next(self.end_seq)
                self.count = 0
            except StopIteration:
                try:
                    self.current_start_seq = next(self.start_seq)
                    self.end_seq = iter([])  
                    self.count = 0
                except StopIteration:
                    raise StopIteration

        middle_digits: str = str(self.count).zfill(self.length_generate_seq)
        self.count += 1
        return int(f"{self.current_start_seq}{middle_digits}{self.current_end_seq}")