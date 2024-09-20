import multiprocessing as mp
import time
from typing import Callable, Iterable

from .execute_base import Executor

class BruteForceExecutor(Executor):
    """
    Service for finding a match using direct brute force using several processes
    """
     
    def __init__(self, task: Callable, process_count: int, args: tuple):
        """
        Args:
            task (Callable): сompliance check function
            process_count (int): number of processes used
            args (tuple[Any]): arguments for сompliance check function
        """
        self.task = task
        self.args = args
        self.process_count:int = process_count if process_count else mp.cpu_count()

    def run(self, generator: Iterable,  *args) -> Iterable:
        """
        Running сompliance check function
        on all values ​​of the generated sequence on several processes

        Args:
            generator (Iterable): generator of values ​​necessary for the task being performed
        """
        self.start_time = time.time()
        with mp.Pool(self.process_count) as pool:
            results = pool.starmap(self.task, [(value, *self.args)  for value in generator])
            return filter(lambda x: x, results)