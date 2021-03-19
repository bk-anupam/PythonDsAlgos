from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "1174182839765614593-BzlZeXgCzoAw8vRqfmVpTcX4VdPK8A"
access_token_secret = "MKsnX6tZLd2jXZen0f3cataVNA2JgjKlrCxJleKRjqTd2"
consumer_key = "QldXjLcANOPgHmqpHvqc1Y5P5"
consumer_secret = "6YqCzPXKPrDqHhaj5b29Qke0JaUzgYO50ocyCXUXf5jmD6gJ9A"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, raw_data):
        print(raw_data)
        return True

    def on_error(self, status_code):
        print(status_code)


if __name__ == "__main__":
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['delhi polls'])
