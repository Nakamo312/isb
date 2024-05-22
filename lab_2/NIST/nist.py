import math
import mpmath

from typing import List
from scipy.special import erfc
from bitarray import bitarray


class Nist:
    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    @staticmethod
    def freq_bit_test(bit_sequence: bitarray) -> float:
        """
        Frequency (Monobit) Test
        Args:
            bit_sequence (bitarray): A bitarray representing the bit sequence to be tested.
        Returns:
            (float) The p-value of the test.
        """
        n = len(bit_sequence)
        summ = 0
        for i in range(n):
            bit = 1 if bit_sequence[i] == 1 else -1
            summ += bit

        sn = summ / math.sqrt(n)
        return erfc(sn / math.sqrt(2))

    @staticmethod
    def identical_bit_test(bit_sequence: bitarray) -> float:
        """
        Frequency Test within a Block
        Args:
            bit_sequence (bitarray): A bitarray representing the bit sequence to be tested.
        Returns:
            (float) The p-value of the test.
        """
        n = len(bit_sequence)
        summ = sum(bit_sequence)
        theta = summ / n
        if abs(theta - 1 / 2.0) < (2 / math.sqrt(n)):
            vn = 0
            for i in range(1, n):
                value = 0 if bit_sequence[i] == bit_sequence[i - 1] else 1
                vn += value
            return erfc(abs(vn - 2 * n * theta * (1 - theta)) / (2 * math.sqrt(2 * n) * theta * (1 - theta)))
        return 0.0

    @staticmethod
    def longest_bit_test(bit_sequence: bitarray, block_size: int) -> float:
        """
        Longest Run of Ones in a Block Test
        Args:
            bit_sequence (bitarray): A bitarray representing the bit sequence to be tested.
        Returns:
            (float) The p-value of the test.
        """
        v = [0 for i in range(4)]
        n = len(bit_sequence)
        m: int = int(n / block_size)
        blocks = [bit_sequence[i * block_size: (i + 1) * block_size] for i in range(m)]
        for block in blocks:
            run_length = 0
            max_run = 0
            for bit in block:
                if int(bit) == 1:
                    run_length += 1
                    max_run = max(max_run, run_length)
                else:
                    run_length = 0
            match max_run:
                case 1 if max_run <= 1:
                    v[0] += 1
                case 2:
                    v[1] += 1
                case 3:
                    v[2] += 1
                case _:
                    v[3] += 1
        khi = 0
        for i in range(len(v)):
            khi += ((v[i] - 16 * Nist.pi[i]) ** 2) / (16 * Nist.pi[i])
        p = mpmath.gammainc(3 / 2, khi / 2)
        return float(p)
