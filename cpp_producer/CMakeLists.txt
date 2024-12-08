cmake_minimum_required(VERSION 3.29)
project(cpp_producer)

set(CMAKE_CXX_STANDARD 20)
add_subdirectory(externals/faker-cxx)
set(CMAKE_PREFIX_PATH "/usr/include/")
find_library(RDKAFKA_LIBRARY NAMES rdkafka PATHS /usr/lib)

find_path(RDKAFKA_INCLUDE_DIR NAMES rdkafka.h PATHS /usr/include/librdkafka )

include_directories(${RDKAFKA_INCLUDE_DIR})
include_directories(include/)
add_library(kafka_produce SHARED src/services/kafka_producer.cpp)
add_executable(${PROJECT_NAME}
    src/main.cpp
        include/services/kafka_producer.h)

target_link_libraries(kafka_produce ${RDKAFKA_LIBRARY})
target_link_libraries(${PROJECT_NAME} faker-cxx)
target_link_libraries(${PROJECT_NAME} kafka_produce)
