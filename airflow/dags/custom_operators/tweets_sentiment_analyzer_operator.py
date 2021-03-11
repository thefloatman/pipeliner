from modules.sentiment_analyzer import SentimentAnalyzer
from modules.sentiment_producer import SentimentProducer

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from kafka import KafkaConsumer
from json import loads


class TweetsSentimentAnalyzerOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            *args, **kwargs):
        super().__init__(*args, **kwargs)


    def execute(self, context):
        consumer = KafkaConsumer(
            'tweets',
            group_id='tweets_group',
            auto_offset_reset='earliest',
            bootstrap_servers=['kafka:9093'],
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            consumer_timeout_ms=10000
        )

        for message in consumer:
            consumer.commit()
            print(message)
            tweet = message.value['tweet']
            result = SentimentAnalyzer().perform(tweet)
            SentimentProducer().perform(result, tweet)

        consumer.close()