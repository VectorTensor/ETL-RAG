#include "faker-cxx/faker.h"
#include <cstring>
#include <iostream>
#include <unistd.h>
#include <librdkafka/rdkafka.h>
#include "services/kafka_producer.h"
#include <json-c/json.h>
int main(){
    auto message_= faker::lorem::paragraph();
    char topic_[100]= "news";
    char char_message[100] = "Hello dude Bye Bye";

    // RunProducer(topic_,char_message);
    struct json_object *json_obj = json_object_new_object();
    json_object_object_add(json_obj, "id", json_object_new_int(1));
    json_object_object_add(json_obj, "name", json_object_new_string("Test User"));
    json_object_object_add(json_obj, "timestamp", json_object_new_int64(time(NULL)));

    const char *json_message = json_object_to_json_string(json_obj);
    RunProducer(topic_, json_message);









    return 0;
}
