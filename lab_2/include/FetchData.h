#include <fstream>
#include <windows.h>
#include "nlohmann/json.hpp"
#include <iostream>

std::string APIENTRY OpenFileDialog(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow);
std::string APIENTRY SaveFileDialog(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow);
std::string readFromFile(const std::string& filePath);
void writeToFile(const std::string& fileName, const std::string& text);
void write_to_json_file(const std::string& file_path, const nlohmann::json& json_data);