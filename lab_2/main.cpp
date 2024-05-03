#include <iostream>
#include "Nist.h"
#include "FetchData.h"


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

int main() {
    std::string filePath = OpenFileDialog(GetModuleHandle(NULL), NULL, GetCommandLineA(), SW_SHOWNORMAL);
    std::string data = readFromFile(filePath);
    std::bitset<128> generatedSequence(data.erase(data.length() - 1));

    double test1 = FreqBitTest(generatedSequence);
    double test2 = IdenticalBitTest(generatedSequence);
    double test3 = LongestBitTest(generatedSequence);

    nlohmann::json json_data;
    json_data["Sequence"] = data;
    json_data["FreqBitTest"] = test1;
    json_data["IdenticalBitTest"] = test2;
    json_data["LongestBitTest"] = test3;
    std::string savePath = SaveFileDialog(GetModuleHandle(NULL), NULL, GetCommandLineA(), SW_SHOWNORMAL);
    write_to_json_file(savePath, json_data);
    return 0;
}
