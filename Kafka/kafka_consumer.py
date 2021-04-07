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
#MariaDB 연동
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
            VALUES(?, ?, ?)'''


#최신데이터 실시간 로드
#시스템에 알림을 주는 것은 부하 발생 우려가 있음
def fetch_latest_orders(next_call_in):
    next_call_in += 30 #주기

    batch = consumer.poll(timeout_ms=100)
    if len(batch) > 0:
        for message in list(batch.values())[0]:
            value = message.value.decode()

            delivery_id = str(uuid.uuid4())
            status = 'CONFIRMED'
            # db insert 
            cursor.execute(sql, [delivery_id, value, status])
            conn.commit()

    threading.Timer(next_call_in - time.time(),
                    fetch_latest_orders,
                    [next_call_in]).start()

#주기적으로 데이터 받기
next_call_in = time.time()
fetch_latest_orders(next_call_in)