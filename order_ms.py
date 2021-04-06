#Flask는 Django에 비해, 간단하며 리소스를 적게 사용
from flask import Flask, jsonify, request
from flask_restful import reqparse
from datetime import datetime

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
    'host': '',
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
    def get(self, user_id):
        conn = mariadb.connect(**config)
        cursor = conn.cursor()
        sql = "select * from orders order by id desc"
        cursor.execute(sql, user_id)
        result_set = cursor.fetchall()

        json_data = []
        for result in result_set:
            json_data.append(result)

        return {'user_id': user_id}

    def post(self, user_id):
        # parser = reqparse.RequestParser()
        # args = parser.parse_args()

        json_data = request.get_json()
        json_data['user_id'] = user_id
        json_data['order_id'] = uuid.uuid4()
        json_data['order_date'] = datetime.today()

        coffee_name = json_data['coffee_name']
        coffee_price = json_data['coffee_price']
        coffee_qty = json_data['coffee_qty']

        #DB Insert
        return jsonify(json_data), 201


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