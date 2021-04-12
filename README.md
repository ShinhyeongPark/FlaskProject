# MSA Project(Kafka, Flask, MariaDB)
> Flask: 물품을 주문하고 이를 DB에 저장하는 Web을 구동시켜주는 서버  
> Kafka: 데이터를 실시간으로 반영  
> MariaDB: 주문, 배달 테이블로 구성  
> Docker Image 배포  
- - - -
## Kafka
- Site: [Apache Kafka](https://kafka.apache.org/)

## Kafka Command
	-  Zookeeper Server Start(Port: 2181)

```
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

	-  Kafka Server Start (Port: 9092)

```
$ bin/kafka-server-start.sh config/server.properties

listeners=PLAINTEXT://localhost:9092

```

	-  Kafka Topic 생성

```
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```

	-  Kafka Topic List
  
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
    "connection.user" : "[host]",
    "connection.password" : "[password]]",
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
"connection.url":"[server]",
"connection.user":"[host]",
"connection.password":"[password]]",
"auto.create":"true", "auto.evolve":"true", "delete.enabled":"false", "tasks.max":"1", "topics": "shinhyeong_exam_topicusers"
  } }
'| curl -X POST -d @- http://localhost:8083/connectors --header "content-Type:application/json"
```