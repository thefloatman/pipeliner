from kafka import SimpleProducer, KafkaClient

class TweetsProducer():
    def __init__(self):
        self.kafka = KafkaClient("localhost:9092")
        self.producer = SimpleProducer(kafka)

    def perform(kafka_topic, data):
         producer.send_messages(kafka_topic, data.encode('utf-8'))