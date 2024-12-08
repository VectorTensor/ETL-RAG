#include "faker-cxx/faker.h"
#include <iostream>
#include <unistd.h>
#include <librdkafka/rdkafka.h>
void RunProducer() {

    char hostname[128];
    char errstr[512];

    rd_kafka_conf_t *conf = rd_kafka_conf_new();

    if(gethostname(hostname, sizeof(hostname)) < 0) {
        fprintf(stderr, "gethostname() failed: %s\n", errstr);
        exit(1);
    }

    if(rd_kafka_conf_set(conf, "client.id", hostname, errstr, sizeof(errstr))  != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "rd_kafka_conf_set() failed: %s\n", errstr);
        exit(1);
    }

    if(rd_kafka_conf_set(conf, "bootstrap.servers", "localhost:9092",errstr, sizeof(errstr))  != RD_KAFKA_CONF_OK) {

        fprintf(stderr, "rd_kafka_conf_set() failed for bootstrap.servers: %s\n", errstr);

    }

    rd_kafka_topic_conf_t *topic_conf = rd_kafka_topic_conf_new();

    if(rd_kafka_topic_conf_set(topic_conf, "acks", "all",
        errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {
        fprintf(stderr, "rd_kafka_topic_conf_set() failed: %s\n", errstr);
        }

    rd_kafka_t *rk;

    if(!(rk = rd_kafka_new(RD_KAFKA_PRODUCER, conf, errstr, sizeof(errstr)))) {

        fprintf(stderr, "rd_kafka_new() failed: %s\n", errstr);

    }

    char topic[100] = "news";
    char payload[100] = "Hello everyone this is from C++";
    rd_kafka_topic_t *rkt = rd_kafka_topic_new(rk,topic, topic_conf);

    if(rd_kafka_produce(rkt, RD_KAFKA_PARTITION_UA, RD_KAFKA_MSG_F_COPY,(void *)payload, sizeof(payload), NULL,0,NULL ) == -1) {

        fprintf(stderr, "rd_kafka_produce() failed: %s\n", errstr);

    }

    // Flush to ensure all messages are sent
    rd_kafka_flush(rk, 10000);


    // Clean up
    rd_kafka_topic_destroy(rkt);
    rd_kafka_destroy(rk);

}
int main(){
    const auto para = faker::lorem::paragraph();

    std::cout <<para <<std::endl;


    return 0;
}
