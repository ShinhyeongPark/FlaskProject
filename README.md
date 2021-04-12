# MSA Project(Kafka, Flask, MariaDB)
## 개요
> Kafka 서버를 구축하고 설정하는 부분에서 많은 오류들을 접했다.  
> 오류들을 해결하기 위해서 가장 빠른 해결 방법은 검색 보다는 **로그를 분석**하는 것이었다  
> 예를 들어 DB 테이블을 생성할 때 칼럼에 대한 Constraint를 잘못 지정(NOT NULL)했을 때 토픽에 데이터를 저장을 못했다.  
> 또한 서버를 시작하는데서도 오류가 발생해 로그를 찾아보니 plugin의 URL 포트가 잘못 지정되어있어서 발생하는 오류라는 것을 확인했다.  
- - - -
> Flask: 물품을 주문하고 이를 DB에 저장하는 Web을 구동시켜주는 서버  
> Kafka: 데이터를 실시간으로 반영  
> MariaDB: 주문, 배달 테이블로 구성  
> Docker Image 배포  
- - - -
## Kafka
- Site: [Apache Kafka](https://kafka.apache.org/)

## Kafka Server Start
- Zookeeper Server Start(Port: 2181)
```
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

- Kafka Server Start (Port: 9092)
```
$ bin/kafka-server-start.sh config/server.properties
```

> Kafka Server를 구동시켰는데, node를 established 못한다는 에러를 발생`listeners=PLAINTEXT://localhost:9092`로 해결  

- Kafka Topic 생성
```
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```

- Kafka Topic List
```
bin/kafka-topics --list --bootstrap-server localhost:9092 
```

- - - -
## Order
- order-ms.py
GET:  사용자가 주문한 Item의 Data를 조회
	- Ex) GET  http://localhost:5000/order-ms/<string:user_id>/orders

POST: 사용자 주문 데이터 추가(Insert)
	- Ex) POST http://localhost:5000/order-ms/USER0002/orders
```
request body
{
    "coffee_name": "americano",
    "coffee_price": 3000,
    "coffee_qty": 5
}
	
```
	- 데이터를 Json 형식으로 변환한 후 Kafka 서버에 전송

## Delivery
- delivery-ms.py
GET: 물품에 대한 배송 Data 조회(SELECT)
	- GET /delivery-ms/deliveries

PUT: 배송 데이터 업데이트(수정)
	- PUT /delivery-ms/deliveries/<string:delivery_id>

- - - -
## pip List
```
Flask==1.1.2
Flask-RESTful==0.3.8
Flask-SQLAlchemy==2.5.1
Jinja2==2.11.3
kafka-python==2.0.2
SQLAlchemy==1.4.5
```
- - - -
## Source-connect
```
 echo '                                                               
{
  "name" : "shinhyeong_source_connect", 
  "config" : {
    "connector.class" : "io.confluent.connect.jdbc.JdbcSourceConnector",
    "connection.url" : "jdbc:mysql://127.0.0.1:3306/mydb",
    "connection.user" : "root",
    "connection.password" : "mysql",
    "mode": "incrementing",
    "incrementing.column.name" : "id",
    "table.whitelist" : "users",
    "topic.prefix" : "shinhyeong_exam_topic", 
    "tasks.max" : "1"
  }
}
' | curl -X POST -d @- http://localhost:8083/connectors --header "content-Type:application/json"
```
## Sink-connect
```
echo ' {
    "name":"shinhyeong_sink_connect",
    "config":{
"connector.class":"io.confluent.connect.jdbc.JdbcSinkConnector",
"connection.url":"jdbc:mysql://multicampus-clouda.cgx0gwgzdjyz.us-east-1.rds.amazonaws.com:3306/mydb",
"connection.user":"admin",
"connection.password":"test1357",
"auto.create":"true", "auto.evolve":"true", "delete.enabled":"false", "tasks.max":"1", "topics": "shinhyeong_exam_topicusers"
  } }
'| curl -X POST -d @- http://localhost:8083/connectors --header "content-Type:application/json"
```