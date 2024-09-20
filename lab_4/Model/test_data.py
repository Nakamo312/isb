
import time
from Model.serialize import Serializable


class  TestData(Serializable):
    """
    Represents data collected during a test run for card validation.

    This class inherits from Serializable and stores data about the number of processes used, 
    the total execution time, and the success status of the test.

    Attributes:
        process_count (int): The number of processes used during the test.
        total_time (str): The total execution time of the test, formatted as a string.
        succes (bool): Whether the test was successful.
    """

    def __init__(self, process_count: int, total_time: time, succes: bool):
           """
        Initializes a TestData object with test results.

        Args:
            process_count (int): The number of processes used during the test.
            total_time (float): The total execution time of the test in seconds.
            succes (bool): Whether the test was successful.
        """
           super().__init__(process_count=process_count, total_time=str(total_time), succes=succes)