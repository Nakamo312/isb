from abc import ABC, abstractmethod
from typing import Iterable


class Executor(ABC):
    """
    Execute iterative task service interface
    """

    @abstractmethod
    def run(self, generator: Iterable, *args) -> Iterable:
        """
        Launching a task and iterative algorithm

        Args:
            generator (Iterable): generator of values ​​necessary for the task being performed
        """
        pass