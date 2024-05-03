
#include "Nist.h"

double FreqBitTest(std::bitset<128> bitSequence)
{
    size_t N = bitSequence.size();
    int summ = 0;
    for (int i = 0; i < N; i++)
    {

        int bit = bitSequence[i] == 1 ? 1 : -1;
        summ += bit;
    }

    double Sn = float(summ) / sqrt(N);
    return erfc(Sn / sqrt(2));
}
double IdenticalBitTest(std::bitset<128> bitSequence)
{
    size_t N = bitSequence.size();
    int summ = 0;
    for (int i = 0; i < N; i++)
    {
        summ += bitSequence[i];
    }
    double dzeta = summ / float(N);
    if (abs(dzeta - 1 / 2.0) < (2 / sqrt(N)))
    {
        int Vn = 0;
        for (size_t i = 0; i < N - 1; i++)
        {
            int value = bitSequence[i] == bitSequence[i + 1] ? 0 : 1;
            Vn += value;
        }
        return erfc(abs(Vn - 2 * N * dzeta * (1 - dzeta)) / (2 * sqrt(2 * N) * (1 - dzeta)));
    }
    return 0;
}
std::vector<std::bitset<16>> split_bitset_into_blocks(const std::bitset<128>& bitSequence) {
    std::vector<std::bitset<16>> blocks;

    for (int i = 0; i < 8; ++i) {
        std::bitset<16> block;
        int k = 0;
        for (int j = i * 16; j < i * 16 + 16; j++)
        {
            block[k] = bitSequence[j];
            k++;
        }
        blocks.push_back(block);
    }

    return blocks;
}
double LongestBitTest(std::bitset<128> bitSequence)
{
    int M = 8;
    int N = bitSequence.size();
    std::vector<int> V(4, 0);

    std::vector<std::bitset<16>> blocks = split_bitset_into_blocks(bitSequence);

    for (const auto& block : blocks)
    {
        int count = 0;
        int max_count = 0;
        for (int i = 0; i < block.size(); ++i)
        {
            if (block[i] == 1)
            {
                count++;
            }
            else
            {
                if (count > max_count) max_count = count;
                count = 0;
            }
        }
        if (max_count <= 1) V[0] += 1;
        else if (max_count == 2) V[1] += 1;
        else if (max_count == 3) V[2] += 1;
        else  V[3] += 1;
    }

    std::vector<float> Pi = { 0.2148, 0.3672, 0.2305,0.1875 };
    double khi = 0;
    for (int i = 0; i < V.size(); ++i)
    {
        khi += pow(V[i] - 16 * Pi[i], 2) / (16 * Pi[i]);
    }
    return khi/2;
}

std::bitset<128> BinarySequence()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);
    std::bitset<128> bitSequence;
    for (int i = 0; i < bitSequence.size(); ++i) {
        bitSequence[i] = dis(gen);
    }
    return bitSequence;
}