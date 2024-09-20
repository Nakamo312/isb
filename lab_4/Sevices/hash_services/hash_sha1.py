
import hashlib
from Sevices.hash_services.hash_base import Hasher


class SHA1Hasher(Hasher):
    """
    Service for hashing the input value using the sha1 algorithm
    """

    def hash(self, value: int) -> str:
        """
        Running the Hash algorithm

        Args:
            value (int): value to be hashed
        Returns:
            hashed value (str)
        """
        return hashlib.sha1(str(value).encode()).hexdigest()