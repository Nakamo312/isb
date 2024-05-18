from typing import List
import math
from scipy.special import erfc, gammainc
from bitarray import bitarray


class Nist:
    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    @staticmethod
    def freq_bit_test(bit_sequence: bitarray) -> float:
        """
        Frequency (Monobit) Test
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
        """
        v = [0 for i in range(4)]
        n = len(bit_sequence)
        m: int = int(n / block_size)
        blocks = [bit_sequence[i * block_size: (i + 1) * block_size] for i in range(m)]

        max_run_lengths = []
        for block in blocks:
            run_length = 0
            max_run = 0
            for bit in block:
                if bit == 1:
                    run_length += 1
                    max_run = max(max_run, run_length)
                else:
                    max_run_lengths.append(max_run)
                    run_length = 0
            max_run_lengths.append(max_run)

            if max_run <= 1:
                v[0] += 1
            elif max_run == 2:
                v[1] += 1
            elif max_run == 3:
                v[2] += 1
            else:
                v[3] += 1
        khi = 0
        for i in range(len(v)):
            khi += pow(v[i] - 16 * Nist.pi[i], 2) / (16 * Nist.pi[i])
        return gammainc(3 / 2, khi / 2)
