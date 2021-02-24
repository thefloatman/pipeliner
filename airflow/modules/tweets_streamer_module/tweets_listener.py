import tweepy
import json
import time

from dateutil import parser
from tweets_streamer_module import TweetsProducer


class TweetsListener(tweepy.StreamListener):
    def __init__ (self, kafka_topic):
        self.kafka_topic = kafka_topic

    def on_status(self, status):
        print(status.text)
        return True

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

    def on_data(self, data):
        """
        Automatic detection of the kind of data collected from Twitter
        This method reads in tweet data as JSON and extracts the data we want.
        """
        try:
            # parse as json
            raw_data = json.loads(data)
            result = {}

            # extract the relevant data
            if "text" in raw_data:
                result['user'] = raw_data["user"]["screen_name"]
                result['created_at'] = parser.parse(raw_data["created_at"])
                result['tweet'] = raw_data["text"]
                result['retweet_count'] = raw_data["retweet_count"]
                result['id_str'] = raw_data["id_str"]

            # publish data to kafka
            TweetsProducer().perform(self.kafka_topic, result)

        except Error as e:
            print(e)
        