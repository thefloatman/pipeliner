import json
from kafka import KafkaProducer
from modules.message_formatter import MessageFormatter

class SentimentProducer():
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=["kafka:9093"])
        self.kafka_topic = 'tweets.sentiment_analysis'


    def perform(self, result, tweet):
        pre_produced_message = {
            'tweet': tweet,
            'sentiment_analysis_result': result
        }

        formatted_message = MessageFormatter().format_entry(pre_produced_message)

        data = json.dumps(formatted_message).encode('utf-8')
        self.producer.send(self.kafka_topic, data)