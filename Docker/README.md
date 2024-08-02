# Overview:
This is outlines the configuration for a Docker setup that integrates several services including Zookeeper, Kafka, Maven, PostgreSQL, Hadoop components, and Spark. The configuration utilizes Docker Compose version 3.7 and defines a multi-container application for data processing and management.

# Services
***Zookeeper***: Manages Kafka’s metadata and service discovery. 

***Kafka1 & Kafka2***: Provides Kafka messaging services. Both Kafka brokers depend on Zookeeper.

***Custom Application***: It's Maven image for running maven project.

***PostgreSQL***: Database service with user, password, and database configuration.

***Hadoop NameNode***: Manages the Hadoop Distributed File System (HDFS).

***Hadoop DataNode***: Stores HDFS data. Communicates with NameNode and ResourceManager.

***Hadoop ResourceManager***: Manages YARN resources. Relies on NameNode and DataNode.

***Hadoop NodeManager***: Executes tasks on the Hadoop cluster. Depends on ResourceManager and DataNode.

***Hadoop HistoryServer***: Provides history of completed YARN applications.

***Spark Master & Worker***: Manages Spark jobs and tasks.

# Localhost Links for Docker Services

 For NameNode web UI `http://localhost:9870`
 
 For DataNode web UI `http://localhost:9864`
 
 For Spark Master  `http://localhost:8080`
 
 For Spark Worker  `http://localhost:8081`
 
