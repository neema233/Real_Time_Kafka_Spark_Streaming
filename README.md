# Real_Time_Kafka_Spark_Streaming

This project involves designing a multi-node Kafka cluster for handling metrics and logs from a cluster of 10 servers and a load balancer. The goal is to process and store metrics and logs effectively using Kafka, a relational database, and Hadoop. The system architecture includes:

10 Servers: Each with an agent to send resource consumption metrics.

Load Balancer: Equipped with an agent to send log data.

Kafka Cluster: To handle the incoming data.

Relational Database(Postgres): For storing metrics.

Spark Application: To process logs and calculate moving window counts.


# System Overview
![System Overview](https://github.com/neema233/Real_Time_Kafka_Spark_Streaming/blob/main/System_Overview.png)

# How to get started?
1-Docker set up:
Go to Docker Directory and download all files in it then run:

```docker-compose up -d```

also download src directory keeping it hierarchy and pom.xml file

2- Access Maven for producer:

```docker exec -it custom_app /bin/bash```

then
 
`mvn clean install` then `mvn exec:java`

3- See the topic that it has been created:

you First Accsess the kafka 
```docker exec -it kafka1 /bin/bash```

and then you will verify the topics that has been created with these commands

```kafka-topics.sh --list --bootstrap-server kafka1:9092```

it suppose to give you :

test-topic3 #this for logs 

test-topic4 #this for metrices


4- running the log consumer

 ```
    docker exec -it spark-master /spark/bin/spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 \
    /app/log_sparkstream_consumer.py
```

and then you can access the hdfs on namenode url `http://localhost:9870 `

5- running the metrices consumer 

`docker exec -it spark-master /bin/bash `

and then run the metrices consumer 

`python /app/metrices_consumer.py`
