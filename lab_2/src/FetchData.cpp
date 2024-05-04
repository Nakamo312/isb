#include "FetchData.h"


std::string APIENTRY OpenFileDialog(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    OPENFILENAMEA ofn;
    char Txt[512];
    sprintf(Txt, "data.txt");
    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFilter = "Data Files(*.txt)\0*.dat;\0Any Files(*.*)\0\*.*\0";
    ofn.lpstrFile = Txt;
    ofn.nFilterIndex = 1;
    ofn.nMaxFile = 256;
    ofn.lpstrTitle = "Выберите файл:";
    ofn.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST | OFN_HIDEREADONLY;

    if (GetOpenFileName(&ofn))
    {
        std::string filePath = ofn.lpstrFile;
        return filePath;
    }
}
std::string APIENTRY SaveFileDialog(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    OPENFILENAMEA ofn;
    char Txt[512];
    sprintf(Txt, "samples.txt");
    memset(&ofn, 0, sizeof(OPENFILENAME));
    ofn.lStructSize = sizeof(OPENFILENAME);
    ofn.hwndOwner = NULL;
    ofn.lpstrFilter = "Data Files(*.dat)\0*.dat;\0Any Files(*.*)\0\*.*\0";
    ofn.lpstrFile = Txt;
    ofn.nFilterIndex = 1;
    ofn.nMaxFile = sizeof(Txt);
    ofn.lpstrTitle = "������� ����";
    ofn.Flags = OFN_EXPLORER | OFN_OVERWRITEPROMPT;
    if (GetSaveFileNameA(&ofn))
    {
        std::string filePath = ofn.lpstrFile;
        return filePath;
    }
}
std::string readFromFile(const std::string& filePath)
{
    try
    {
        std::ifstream file(filePath);
        if (!file.is_open())
        {
            throw std::runtime_error("FileError");
        }

        std::string data;
        std::string line;
        while (std::getline(file, line))
        {
            data += line + "\n";
        }

        file.close();
        return data;
    }
    catch (const std::exception& e)
    {
        std::cerr << "Errno: " << e.what() << std::endl;
    }

}
void writeToFile(const std::string& fileName, const std::string& text)
{
    try
    {
        std::ofstream file(fileName);

        if (!file.is_open())
        {
            throw std::runtime_error("FileError:");
        }
        file << text;
        file.close();
    }
    catch (const std::exception& e)
    {
        std::cerr << "Errno: " << e.what() << std::endl;
    }
}
void write_to_json_file(const std::string& file_path, const nlohmann::json& json_data)
{
    try {
        std::ofstream file;
        file.open(file_path);

        if (!file.is_open()) {
            throw std::runtime_error("FileError:" + file_path);
        }

        file << json_data;
        file.close();
    }
    catch (const std::exception& e) {
        std::cerr << "Errno: " << e.what() << std::endl;
    }
}