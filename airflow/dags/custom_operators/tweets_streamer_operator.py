import tweepy
from modules.tweets_listener import TweetsListener
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""

# World Location
WORLD = [-180,-90,180,90]


class TweetsStreamerOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            topic,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.topic = topic
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

    def execute(self, context):
        streaming_api = tweepy.streaming.Stream(self.auth, TweetsListener(self.topic))    
        streaming_api.filter(locations=WORLD, track=self.topic)
