import json
from kafka import KafkaProducer

class TweetsProducer():
    def __init__(self, kafka_topic):
        self.producer = KafkaProducer(bootstrap_servers=["kafka:9093"])
        self.kafka_topic = kafka_topic


    def perform(self, data):
        data = json.dumps(data).encode('utf-8')
        self.producer.send(self.kafka_topic, data)