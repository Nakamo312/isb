cmake_minimum_required(VERSION 3.11)

project(nist-v1 CXX)

set(CMAKE_CXX_STANDARD 23)

# Специфичные настройки для компилятора Visual Studio
if(MSVC)
    # Генерируем статическую заглушку для динамических библиотек
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS true)

    # Включаем высокий уровень предупреждений
    if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
        string(REGEX REPLACE "/W[0-4]" "/W4" CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
    else()
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
    endif()
endif()


# Объявляем библиотеку
add_library(nist SHARED
    "include/Nist.h"
    "include/nlohmann/json.hpp"
    "src/Nist.cc"

 "src/FetchData.cpp")

target_include_directories(nist PUBLIC "include")

add_executable(nist-v1-main  "main.cpp"  "src/FetchData.cpp")
target_link_libraries(nist-v1-main nist)

add_executable(nist-v1-generate  "generate.cpp"  "src/FetchData.cpp")
target_link_libraries(nist-v1-generate nist)


