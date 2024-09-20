from abc import ABC, abstractmethod

class Hasher(ABC):
    """
    Hash service interface
    """

    @abstractmethod
    def hash(self, value: int) -> str:
        """
        Running the Hash algorithm

        Args:
            value (int): value to be hashed
        Returns:
            hashed value (str)
        """
        pass