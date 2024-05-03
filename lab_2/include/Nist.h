#include <bitset>
#include <vector>
#include "math.h"
#include <random>

std::bitset<128> BinarySequence();
double FreqBitTest(std::bitset<128> bitSequence);
double IdenticalBitTest(std::bitset<128> bitSequence);
std::vector<std::bitset<16>> split_bitset_into_blocks(const std::bitset<128>& bitSequence);
double LongestBitTest(std::bitset<128> bitSequence);