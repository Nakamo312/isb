#include "FetchData.h"
#include "Nist.h"


int main()
{
	std::bitset<128> generatedSequence = BinarySequence();
	std::string savePath = SaveFileDialog(GetModuleHandle(NULL), NULL, GetCommandLineA(), SW_SHOWNORMAL);
	writeToFile(savePath, generatedSequence.to_string());
}