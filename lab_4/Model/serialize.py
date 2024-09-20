from typing import  Generator

class Serializable:
    """
    A class that represents a serializable object, allowing data to be stored and retrieved in a dictionary-like manner.

    This class provides a simple way to manage data that can be easily serialized into a dictionary and deserialized back from a dictionary.
    It uses a dictionary (self.dict) to store the object's attributes.

    Attributes:
        dict (dict): A dictionary storing the object's attributes.
    """
     
    def __init__(self, **kwargs):
        """
        Initializes the Serializable object with optional keyword arguments.

        Args:
            **kwargs: Keyword arguments to initialize the object's attributes.
        """
        self.__dict__.update(kwargs)

    def __getitem__(self,key):
        """
        Gets the value of an attribute by its key.

        Args:
            key (str): The key of the attribute to retrieve.

        Returns:
            object: The value of the attribute if the key exists, otherwise None.
        """
        if key in self.__dict__:
            return self.__dict__.get(key)
        
    def get(self) -> Generator:
        """
        Returns a generator that iterates over the values of the object's attributes.

        Returns:
            Generator: A generator yielding each attribute value.
        """
        for attr in self.__dict__.values():
            yield attr
