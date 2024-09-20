import logging
import multiprocessing as mp
import time
from typing import Tuple, Optional

from PyQt5.QtCore import QThread, pyqtSignal

from Model.input_card_data import InCardData
from Model.output_card_data import OutCardData
from Model.serialize import Serializable
from Model.test_data import TestData

from Sevices.event_services.event_track import Tracker
from Sevices.execute_services.brut_force_execute import BruteForceExecutor
from Sevices.generator_services.gen_n_digit_number import GeneratorNDigitNumbers
from Sevices.hash_services.hash_base import Hasher
from Sevices.hash_services.hash_sha1 import SHA1Hasher
from Sevices.validate_services.check_luhn import LuhnCheck


def check_collision(value: int, target: str, hash_func: Hasher = SHA1Hasher()) -> Optional[int]:
    """
    Checks if the hash of a value matches the target hash.

    Args:
        value (int): Value to be hashed.
        target (str): Target hash.
        hash_func (Hasher): Hashing function.

    Returns:
        The value if its hash matches the target hash, otherwise None.
    """
    hash_result = hash_func(value)
    logging.info(f"Process {mp.current_process().name} testing value: {value} {hash_result}")
    if hash_result == target:
        return value


class WorkerThread(QThread):
    """
    Thread for performing a brute-force attack.
    """
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(TestData)
    progress_signal = pyqtSignal(int)
    iterations_signal = pyqtSignal(float, float)
    out_result_signal = pyqtSignal(Serializable)

    def __init__(self, in_card_data: InCardData, process_count: Optional[int] = None):
        """
        Initializes the thread.

        Args:
            in_card_data (InCardData): Input card data.
            process_count (int): Number of processes.
        """
        super().__init__()
        self.in_card_data = in_card_data
        self.process_count = process_count

    def __del__(self):
        """
        Unsubscribes from tracking events.
        """
        Tracker.unsubscribe(self.progress_event_handle)

    def progress_event_handle(self, value: float, time: float):
        """
        Progress event handler.

        Args:
            value (float): Progress.
            time (float): Time.
        """
        self.iterations_signal.emit(value, time)

    def run(self):
        """
        Starts the thread.
        """
        try:
            self.status_signal.emit("Start working...")
            generator = GeneratorNDigitNumbers(
                self.in_card_data['BIN'], self.in_card_data['last_digits'], self.in_card_data['length']
            )
            hasher = SHA1Hasher()
            executor = BruteForceExecutor(
                check_collision, self.process_count, (self.in_card_data['hash_number'], hasher.hash)
            )
            checker = LuhnCheck()
            Tracker.subscribe(self.progress_event_handle)
            start_time = time.time()
            results: Tuple[int, ...] = executor.run(generator)
            total_time = time.time() - start_time
            for res in results:
                is_valid = checker.check(str(res))
                self.out_result_signal.emit(OutCardData(str(res), self.in_card_data['hash_number'], is_valid))

            self.finished_signal.emit(TestData(self.process_count, total_time, is_valid))
        except Exception as e:
            logging.error(f"[WorkerThread]: Error during execution: {e}")
            self.finished_signal.emit(TestData(self.process_count, time.time() - start_time, False))
      