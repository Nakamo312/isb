
import time

from .event import Event

class Tracker(Event):
    """
    A class that tracks the execution time and speed of a function.

    This class inherits from the Event class, allowing it to notify subscribers about changes in the tracked function's performance. 
    It provides a decorator (call) that wraps the target function, tracking its execution time and speed. 
    Every 0.1 seconds, the Tracker class calculates and publishes the current speed (iterations per second) and the total execution time.
    """

    start_time = 0
    last_print_time = time.time()
    iterations = 0

    @classmethod
    def call(cls, func):
        """
        A decorator that tracks the execution time and speed of a function.

        This decorator wraps the target function, keeping track of the number of function calls and the total execution time.
        Every 0.1 seconds, it calculates and publishes the current speed (iterations per second) and the total execution time 
        using the Event.invoke method.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The decorated function.
        """
        def wrapper(*args, **kwargs):
            cls.iterations += 1
            now = time.time()
            if now - cls.last_print_time >= 0.1:
                cls.start_time += now - cls.last_print_time
                cls.invoke(cls.iterations // (now - cls.last_print_time), cls.start_time)
                cls.last_print_time = now 
                cls.iterations = 0
            return func(*args, **kwargs)
        return wrapper