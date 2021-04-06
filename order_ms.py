#Flask는 Django에 비해, 간단하며 리소스를 적게 사용
from flask import Flask, jsonify, request
from kafka import KafkaProducer
from flask_restful import reqparse
from datetime import datetime
import flask
import flask_restful
import mariadb
import json
import uuid

#실행파일 변경: export FLASK_APP='파일명'
#디버그 모드 실행: set FLASK_DEBUG=True -> auto refresh
#app.config['DEBUG'] = True 
app = Flask(__name__)
api = flask_restful.Api(app)

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'mysql',
    'database' : 'mydb'
}

@app.route('/order-ms')
def index():
    return "Order MicroService!"

#주문 목록
class Order(flask_restful.Resource):
    def __init__(self):
        self.conn = mariadb.connect(**config)
        self.cursor = self.conn.cursor()
        
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    def get(self, user_id):
        sql = "select user_id, order_id, coffee_name, coffee_price, coffee_qty from orders where user_id=? order by id desc"
        self.cursor.execute(sql, [user_id])
        result_set = self.cursor.fetchall()

        row_headers = [x[0] for x in self.cursor.descripton]
        json_data = []
        for result in result_set:
            json_data.append(dict(zip(row_headers, result)))

        return jsonify(json_data)

    def post(self, user_id):
        # parser = reqparse.RequestParser()
        # args = parser.parse_args()

        json_data = request.get_json()
        json_data['user_id'] = user_id
        json_data['order_id'] = uuid.uuid4()
        json_data['order_date'] = datetime.today()

        # coffee_name = json_data['coffee_name']
        # coffee_price = json_data['coffee_price']
        # coffee_qty = json_data['coffee_qty']

        #DB Insert
        sql = "INSERT INTO orders(user_id, order_id, coffee_name, coffee_price, coffee_qty) VALUES(?,?,?,?,?)"
        self.cursor.execute(sql, [user_id, 
                                json_data['order_id'],
                                json_data['coffee_name'],
                                json_data['coffee_price'],
                                json_data['coffee_qty']])
        self.conn.commit()

        #Kafka Messeage Send
        self.producer.send('new_orders', value=json.dump(json_data).encode('utf-8'))
        self.producer.flush()

        response = jsonify(json_data)
        response.status_cod = 201
        return response


#주문 세부사항
class OrderDetail(flask_restful.Resource):
    def get(self, user_id, order_id):
        return {'user_id': user_id, 'order_id': order_id}


#GET http://127.0.0.1:5000//order-ms/<string:user_id>/orders
#POST http://127.0.0.1:5000//order-ms/<string:user_id>/orders {request body }
api.add_resource(Order, '/order-ms/<string:user_id>/orders')
api.add_resource(OrderDetail, '/order-ms/<string:user_id>/orders/<string:order_id>')

if __name__ == '__main__':
    app.run()