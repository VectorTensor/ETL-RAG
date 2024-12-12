#include <cstdlib>
#include <cstring>
#include <iostream>
#include <unistd.h>
#include <librdkafka/rdkafka.h>



void RunProducer(char  (&topic_)[100], const char *message_){

    char hostname[128];
    char errstr[512];

/// Initialize config pointer for kafka to set up client and server
    rd_kafka_conf_t * conf = rd_kafka_conf_new();

    if (gethostname(hostname, sizeof(hostname))< 0){

        fprintf(stderr, "gethostname() failed: %s \n ", errstr);
        exit(1);
    }

    // Set client

    if (rd_kafka_conf_set(conf, "client.id", hostname,errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK){

        fprintf(stderr, "rd_kafka_conf_set() failed: %s \n", errstr);

    }

    // Set Server
    if (rd_kafka_conf_set(conf, "bootstrap.servers","localhost:9092", errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK){

        fprintf(stderr, "failied bootstraping");


    }

    // Declare config to for topic
    rd_kafka_topic_conf_t  *topic_conf  = rd_kafka_topic_conf_new();

    // Set topic config
    if (rd_kafka_topic_conf_set(topic_conf,"acks","all",errstr, sizeof(errstr)) != RD_KAFKA_CONF_OK) {

        fprintf(stderr,"failed");
    }

// rd_kafka_t type for abi compatibility
    rd_kafka_t *rk;

    if (!(rk = rd_kafka_new(RD_KAFKA_PRODUCER, conf, errstr, sizeof(errstr)))){
        fprintf(stderr, "failed %s \n", errstr);
    }
    // topic pointer

    rd_kafka_topic_t *rkt = rd_kafka_topic_new(rk, topic_, topic_conf);

    // Send payload
    std::cout<<"message: "<<*message_<<std::endl;
    if (rd_kafka_produce(rkt, RD_KAFKA_PARTITION_UA, RD_KAFKA_MSG_F_COPY, (void *) message_, strlen(message_), NULL, 0, NULL) == -1){

        fprintf(stderr, "failed %s \n",errstr);
    }

    rd_kafka_flush(rk, 10000);

    rd_kafka_topic_destroy(rkt);

    rd_kafka_destroy(rk);










}