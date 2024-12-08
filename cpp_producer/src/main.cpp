#include "faker-cxx/faker.h"
#include <cstring>
#include <iostream>
#include <unistd.h>
#include <librdkafka/rdkafka.h>
#include "services/kafka_producer.h"
int main(){
    auto message_= faker::lorem::paragraph();
    char topic_[100]= "news";
    char char_message[100] = "Hello dude Bye Bye";

    RunProducer(topic_,char_message);








    return 0;
}
