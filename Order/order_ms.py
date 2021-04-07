#Flask는 Django에 비해, 간단하며 리소스를 적게 사용
from flask import Flask, jsonify, request
from kafka import KafkaProducer
from flask_restful import reqparse
from datetime import datetime
import flask
import flask_restful
import json
import uuid
import pymysql
app = Flask(__name__)
api = flask_restful.Api(app)

config = {
    'host': '172.19.0.3',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'mydb'
}

#endpoint
@app.route('/')
def index():
    return "Order MicroService!"

#주문 목록
class Order(flask_restful.Resource):
    def __init__(self):
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()
        #KAFKA SERVER 연결
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    
    #GET 메소드
    def get(self, user_id):
        sql = '''select user_id, order_id, coffee_name, coffee_price, coffee_qty 
                from orders where user_id=%s order by user_id desc'''
        self.cursor.execute(sql, [user_id])
        result_set = self.cursor.fetchall()

        row_headers = [x[0] for x in self.cursor.description]

        json_data = []
        for result in result_set:
            json_data.append(dict(zip(row_headers, result)))

        return jsonify(json_data)

    #POST 메소드
    def post(self, user_id):
        json_data = request.get_json()
        json_data['user_id'] = user_id
        json_data['order_id'] = str(uuid.uuid4()) 
        # json_data['ordered_at'] = str(datetime.today())

        # DB insert
        sql = '''INSERT INTO orders(user_id, order_id, coffee_name, coffee_price, coffee_qty) 
                    VALUES(?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sql, [user_id, 
                                json_data['order_id'],
                                json_data['coffee_name'],
                                json_data['coffee_price'],
                                json_data['coffee_qty']])
        self.conn.commit()

        # Kafka message send
        # Kafka Consumer인 new_orders에 전송
        self.producer.send('new_orders', value=json.dumps(json_data).encode())
        self.producer.flush() 

        response = jsonify(json_data)
        response.status_code = 201
        
        return response


#주문 세부사항
class OrderDetail(flask_restful.Resource):
    def get(self, user_id, order_id):
        return {'user_id': user_id, 'order_id': order_id}


#GET http://127.0.0.1:5000//order-ms/<string:user_id>/orders
#POST http://127.0.0.1:5000//order-ms/<string:user_id>/orders {request body }
#Ex)POST http://127.0.0.1:5000/order-ms/USER0002/orders : orders 테이블에 데이터 추가
api.add_resource(Order, '/order-ms/<string:user_id>/orders')
api.add_resource(OrderDetail, '/order-ms/<string:user_id>/orders/<string:order_id>')

if __name__ == '__main__':
    app.run()