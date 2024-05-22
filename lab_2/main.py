import argparse
import logging
import os

from bitarray import bitarray

import NIST.nist as test
import Tool.fetch_data as wr

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('maindir', help='directory from which the search will be performed', type=str)
    parser.add_argument("-fp", "--file_path", help='path where the file with data sequence', required=True)
    parser.add_argument("-sp", "--save_path", help="path for save results", required=True)

    args = parser.parse_args()

    fp = args.file_path
    sp = args.save_path
    dir = args.maindir

    fp = os.path.join(os.getcwd(), dir, fp)
    sp = os.path.join(os.getcwd(), dir, sp)

    sequence = bitarray(wr.txt_read(file_path=fp))
    test1 = test.Nist.freq_bit_test(sequence)
    test2 = test.Nist.identical_bit_test(sequence)
    test3 = test.Nist.longest_bit_test(sequence, 16)

    wr.json_write(file_path=sp,
                  FreqBitTest=test1,
                  IdenticalBitTest=test2,
                  LongestBitTest=test3,
                  Sequence=str(sequence.tobytes()))
    logging.info("data will be written successfully")
