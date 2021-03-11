import json
from kafka import KafkaProducer

class SentimentProducer():
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=["kafka:9093"])
        self.kafka_topic = 'tweets.sentiment_analysis'


    def perform(self, result, tweet):
        pre_produced_message = {
            'tweet': tweet,
            'sentiment_analysis_result': result
        }
        data = json.dumps(pre_produced_message).encode('utf-8')
        self.producer.send(self.kafka_topic, data)