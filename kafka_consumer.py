from kafka import KafkaConsumer
from datetime import datetime
import time
import json
import threading #파이썬에서 쓰레드 사용
import uuid
import mariadb

consumer = KafkaConsumer('new_orders',
                        bootstrap_servers=["localhost:9092"],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        auto_commit_interval_ms=1000,
                        consumer_timeout_ms=1000
                        )

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'mysql',
    'database' : 'mydb'
}

conn = mariadb.connect(**config)
cursor = conn.cursor()
sql = '''INSERT INTO delivery_status(delivery_id, order_json, status)
        VALUE(?,?,?) %s'''
#최신데이터 실시간 로드
#시스템에 알림을 주는 것은 부하 발생 우려가 있음
def fetech_latest_orders(next_call_in):
    next_call_in += 5

    batch = consumer.poll(timeout_ms=100)
    if len(batch) > 0:
        for message in list(batch.values())[0]:
            value = message.value.decode()
            # order_dict = json.loads(value)
            # print(order_dict["ordered_at"])

            delivery_id = str(uuid.uuid4())
            status = 'CONFIRMED'
            cursor.execute(sql, [delivery_id, value, status])
            conn.commit
    # list(batch.values())
    threading.Timer(next_call_in - time.time(), fetech_latest_orders, [next_call_in]).start()

#주기적으로 데이터 받기
next_call_in = time.time()
fetech_latest_orders(next_call_in)

# start = time.time()
# for message in consumer:
#     topic = message.topic
#     partition = message.partition
#     offset = message.offset
#     value = message.value
#     print("Topic:{}, Partition:{}, Offset:{}, Value:{}".format(topic, partition, offset, value))
# print("Elapsed: ", + (time.time() - start))