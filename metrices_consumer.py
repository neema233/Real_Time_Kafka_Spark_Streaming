from kafka import KafkaConsumer
import psycopg2
from psycopg2 import sql
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)


consumer = KafkaConsumer('test-topic4', bootstrap_servers=['172.25.0.12:9092'])


db_config = {
    'dbname': 'mydb',
    'user': 'myuser',
    'password': 'mypassword',
    'host': 'postgres', 
    'port': '5432'  
}


try:
    conn = psycopg2.connect(**db_config)
    conn.autocommit = True  
    cur = conn.cursor()


    cur.execute("""
        CREATE TABLE IF NOT EXISTS server_metrics (
            id SERIAL PRIMARY KEY,
            cpu INTEGER,
            mem INTEGER,
            disk INTEGER,
            timestamp TIMESTAMP
        )
    """)
    logging.info("Connected to PostgreSQL and created table 'server_metrics'.")
except psycopg2.Error as e:
    logging.error("Error connecting to PostgreSQL: {}".format(e))
    exit(1)


try:
    for message in consumer:
        try:
            parts = message.value.decode('utf-8').split(',')
            id = int(parts[0].split(':')[1].strip())
            cpu = int(parts[1].split(':')[1].strip())
            mem = int(parts[2].split(':')[1].strip())
            disk = int(parts[3].split(':')[1].strip())
            timestamp = datetime.fromtimestamp(message.timestamp / 1000.0)  
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')

            cur.execute(sql.SQL("""
                INSERT INTO server_metrics (id, cpu, mem, disk, timestamp) 
                VALUES (%s, %s, %s, %s, %s)
            """), (id, cpu, mem, disk, timestamp_str))
            logging.info("Inserted metrics: id={}, cpu={}, mem={}, disk={}, timestamp={}".format(id, cpu, mem, disk, timestamp_str))
        except Exception as e:
            logging.error("Error processing Kafka message or inserting into PostgreSQL: {}".format(e))
except KeyboardInterrupt:
    logging.info("Process interrupted by user.")
except Exception as e:
    logging.error("Unexpected error: {}".format(e))
finally:
    if 'conn' in locals() or 'conn' in globals():
        conn.close()  
        logging.info("Closed PostgreSQL connection.")
