from abc import ABC, abstractmethod

class Checker(ABC):
    """
    Validation service interface
    """

    @abstractmethod
    def check(self, value: str) -> bool:
        """
        Running the algorithm

        Args:
            value (str): value to be validated
        Returns:
            is valide value (bool)
        """
        pass