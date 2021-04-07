#Kafka Start
#Kafka로 간단한 Micro Service 구현

import os
from models import db
from flask import Flask, jsonify, request #jsonify: json파일 사용을 위한 라이브러리
from datetime import datetime
import uuid #Unique ID 생성

app = Flask(__name__)
# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')

# SQLAlchemy 설정

# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()

#annotaion: 매소드나 클래스의 부가 정보
@app.route('/')
def index():#서비스 endpoint 정의
    return "Hello, World!"

#사용자 목록
@app.route('/users')
def users():#서비스 endpoint 정의
    return "** Users List"

#GET: userID 동적할당
@app.route('/users/<userId>')
def users_detail(userId):#서비스 endpoint 정의
    #return "{\"name\":%s}" % (userId)
    return jsonify({"userid": userId}) #직관적으로 확인 가능

# @app.route('/users/<userID>')
# def users_detail(userId):#서비스 endpoint 정의
#     return "Welcome to Flask App, {}".format(userId)

@app.route('/health-check')
def health_check():#서비스 endpoint 정의
    return "server is running on 5000 port"

#POST: 데이터 값을 JSON형태로 전송
@app.route('/users', methods = ['POST'])
def userAdd():
    user = request.get_json()
    user['user_id'] = uuid.uuid4 #Random UUID
    user['created_at'] = datetime.today()
    return jsonify(user)
    #Database에 추가
    #Kafka Server 전달

@app.route('/order-ms/<user_id>/orders')
def orders():
    return "** Users List"

@app.route('/order-ms/<user_id>/orders/<order_id>')
def orders_detail(order_id):
    return jsonify({"orderid": order_id})

@app.route('/order-ms/<user_id>/orders', methods = ['POST'])
def orderAdd():
    order = request.get_json()
    order['coffee_name'] = 'today coffee'
    order['coffee_price'] = '5000'
    order['coffee_qty'] = '3'
    order['order_id'] = uuid.uuid4 #Random UUID
    order['created_at'] = datetime.today()
    return jsonify(order)

if __name__ == "__main__":
    app.run()