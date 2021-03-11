from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def perform(self, input_value):
        sentiment_dict = self.analyzer.polarity_scores(input_value)
        result_dict = {
            'pos': sentiment_dict['pos'] * 100,
            'neg': sentiment_dict['neg'] * 100,
            'neu': sentiment_dict['neu'] * 100
        }

        return result_dict