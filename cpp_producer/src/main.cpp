#include "faker-cxx/faker.h"
#include <iostream>

int main(){
    const auto id = faker::string::uuid();
    std::cout << id << std::endl; // 59990db5-3a5f-40bf-8af0-7834c29ee884

    return 0;
}
