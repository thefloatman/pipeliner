from kafka import KafkaProducer

class TweetsProducer():
    def __init__(self):
        self.producer = producer = KafkaProducer(bootstrap_servers=["kafka:9092"])

    def perform(kafka_topic, data):
         producer.send_messages(kafka_topic, data.encode('utf-8'))