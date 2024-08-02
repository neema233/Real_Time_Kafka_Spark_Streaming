from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp, window, expr, count
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("KafkaStreamingApp") \
    .getOrCreate()


schema = StructType([
    StructField("ip", StringType(), True),
    StructField("uid", StringType(), True),
    StructField("datetime", StringType(), True),
    StructField("method", StringType(), True),
    StructField("filename", StringType(), True),
    StructField("statuscode", StringType(), True),
    StructField("filesize", StringType(), True)
])


df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "172.25.0.12:9092") \
    .option("subscribe", "test-topic3") \
    .load()


parsed_df = df \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("datetime", to_timestamp("datetime", "dd/MMM/yyyy:HH:mm:ss Z"))


aggregated_df = parsed_df \
    .withWatermark("datetime", "5 minutes") \
    .groupBy(window("datetime", "5 minutes"), "method", "statuscode") \
    .agg(
    count(expr("CASE WHEN method = 'GET' AND statuscode = '200' THEN 1 ELSE NULL END")).alias("successful_GET"),
    count(expr("CASE WHEN method = 'POST' AND statuscode = '200' THEN 1 ELSE NULL END")).alias("successful_POST"),
    count(expr("CASE WHEN method = 'GET' AND statuscode != '200' THEN 1 ELSE NULL END")).alias("failed_GET"),
    count(expr("CASE WHEN method = 'POST' AND statuscode != '200' THEN 1 ELSE NULL END")).alias("failed_POST")
    ).select(
    "window.start", "window.end",
    "successful_GET", "successful_POST", "failed_GET", "failed_POST"    
    )


parquet_path = "hdfs://namenode:9000/logs"
checkpoint_location = "hdfs://namenode:9000/user/hdfs/checkpoint"

pivoted_query = aggregated_df \
    .writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", parquet_path) \
    .option("checkpointLocation", checkpoint_location) \
    .start()


pivoted_query.awaitTermination()