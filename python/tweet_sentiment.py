############################################################################
#### Collecting Twitter Streaming API####
import tweepy
from tweepy import OAuthHandler

consumer_key = 'dG5YKZA7UUzj8zASL6HqJ8S5E'
consumer_secret = 'Qx70JFu8cbx8fciZcnZ9RWTkGNA8QAHrQFf9ovh3JpqGNuk4cz'
access_token = '854203928636006400-MFsbyBvbpCToPgh8fgBgWkTxqtQ5ErN'
access_secret = 'PpITeoGd3tmQcc8EX1wWPsxtymdjYnm1hzIN2gKTiTw7g'

 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

from tweepy import Stream
from tweepy.streaming import StreamListener
import os
os.chdir('/Users/jaygkay/Desktop/')

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('tweetsAPI.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['chicago']) #$AAPL
############################################################################


############################################################################
#### functions to manipulate the API data
import os
os.chdir('/Users/jaygkay/Desktop/jaygkay/project')
import pandas as pd
import numpy as np
import json

def readfile(file):
    
    tweets_data = []
    tweets_file = open(file, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    return tweets_data

    def tweets(file, readfile):
    tweets_data = readfile(file)
    
    tweets = pd.DataFrame()
    tweets['created_at'] = list(map(lambda tweet: tweet['created_at'], tweets_data))
    tweets['username'] = list(map(lambda tweet: tweet['user']['name'] if 'user' in tweet else None, tweets_data))
    tweets['location'] = list(map(lambda tweet: tweet['user']['location'] if 'user' in tweet else None, tweets_data))
    tweets['text'] = list(map(lambda tweet: tweet['text'], tweets_data))
    #return tweets

    import datetime
    created = [i for i in tweets['created_at']]
    tweetext = [j for j in tweets['text']]
    time = []
    text = []
    for i in range(len(created)):
        #10 to 3 based on New York time (14 ~ 19)
        #12pm to 4pm () based on New york///// chicago 11am-3pm & LA 9am ~ 1pm
        if created[i].split()[3] >= '13:00:00' and created[i].split()[3] < '19:00:00' :
            time.append(created[i])
            text.append(tweetext[i])
    df = pd.DataFrame()
    df['time'] = time
    df['text'] = text
    df.shape, df.head()
    
    textonly = df['text']
    puretext = textonly.str.lower()

 
 	  return puretext


from textblob import TextBlob
import re
def cleantext(file):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(rt)", " ", file).split())
    
def cleanit(file, tweets):
    a = []
    puretext = tweets(file, readfile)
    for i in puretext:
        a.append(cleantext(i))
    return a   

def sentiment(text):
        analysis = TextBlob(cleantext(text))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

def thus(file, cleanit, tweets):
    a = cleanit(file, tweets)
    sent = []
    
    for i in a:
        sent.append(sentiment(i))
    #print(['pos', 'neu', 'neg'])
    b = [sent.count('positive'), sent.count('neutral'),  sent.count('negative')]
    
    return b
############################################################################




############################################################################
#### Stock Prices ####
import pandas_datareader.data as web
import datetime
start = datetime.datetime(2017,5,19)
end = datetime.datetime(2017,6,6)

apple = web.DataReader("AAPL", "google", start, end)
print(apple)

#daily reutrns
df = apple
a = df['Close']
rev = []
for i in range(len(a)):
    if a[i] > a[i-1]:
        rev.append(1) #1 if increase
    else:
        rev.append(0)
print(rev)
print('Revenue with time seriese ', rev[1:])

############################################################################



############################################################################
#### Logistic Regression####
xVar = thus('May22.json', cleanit, tweets), thus('May23.json', cleanit, tweets),thus('May24.json', cleanit, tweets),thus('May25.json', cleanit, tweets), thus('May26.json', cleanit, tweets), thus('Jun5.json', cleanit, tweets)
xVar
yVar = rev[1],rev[2],rev[3],rev[4],rev[5],rev[-1] 
yVar

df = pd.DataFrame()
df['positive'] = xVar[0][0], xVar[1][0], xVar[2][0], xVar[3][0], xVar[4][0], xVar[5][0]
df['neutral'] = xVar[0][1], xVar[1][1], xVar[2][1], xVar[3][1], xVar[4][1], xVar[5][1]
df['negative'] = xVar[0][2], xVar[1][2], xVar[2][2], xVar[3][2], xVar[4][2],xVar[5][2],
df['target'] = yVar
df

from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

df.describe()

x_var = np.array(df[['positive', 'neutral', 'negative']])
y_var = np.array(df['target'])
print(x_var.shape, y_var.shape)

#Standardized
scaler = StandardScaler()
x_var = scaler.fit_transform(x_var)
print(x_var)

xTrain, xTest, yTrain, yTest = train_test_split(x_var, y_var, test_size=0.3, random_state = 10)
print("xTrain size: ", xTrain.shape)
print("xTest size: ", xTest.shape)
print("yTrain size: ", yTrain.shape)
print("yTest size: ", yTest.shape)

model = LogisticRegression()
model.fit(xTrain, yTrain)

print('Logistic Regression score for training set: %f' %model.score(xTrain, yTrain))
print('===========================================================================')
print("classification Report")
print(classification_report(yTest, model.predict(xTest)))

############################################################################
