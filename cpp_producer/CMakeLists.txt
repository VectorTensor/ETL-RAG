cmake_minimum_required(VERSION 3.29)
project(cpp_producer)

set(CMAKE_CXX_STANDARD 20)
add_subdirectory(externals/faker-cxx)
add_executable(${PROJECT_NAME}
    src/main.cpp)
target_link_libraries(${PROJECT_NAME} faker-cxx)

