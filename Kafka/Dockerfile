#파이썬 이미지를 사용한다
FROM python:3.8-alpine 

#작업할 디렉터리를 생성하고 지정
RUN mkdir -p /MSAproject
WORKDIR /MSAproject

RUN pip install pymysql
RUN pip install kafka-python

#의존성 패키지 명시 파일
# COPY requirements.txt /MSAproject
COPY ./kafka_consumer.py /MSAproject/app.py

#라이브러리 설치
# RUN pip install -r requirements.txt

# EXPOSE 6000
CMD ["python", "/MSAproject/app.py"]