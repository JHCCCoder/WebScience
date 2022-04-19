import re
import json

import numpy as np
from nltk import word_tokenize
from functools import reduce
from collections import Counter, defaultdict

class NWScore:

    listTerms = [
        "bus", "buses", "bike", "car", "cars", "bicycle", "pavement", "roadway", "corner",
        "tram", "railway", "trams", "underground", "accident", "jams", "tax", "traffic", "tramcar",
        "driver", "park", "emergency", "stop", "conductor", "subway", "trolley"
        "emergency", "accidents", "tfl", "pedestrian"
    ]

    listSpam =['ebay', 'review', 'shopping', 'deal','sale', 'sales','link',
        'click', 'marketing', 'promote', 'discount', 'products', 'store', 'diet',
        'weight', 'porn', 'followback', 'follow back', 'lucky', 'winners', 'prize',
        'hiring']

    def __init__(self, hq_set: list, lq_set: list, most_common=25):
        self.hq_set = hq_set
        self.lq_set = lq_set
        self.bg_set = hq_set + lq_set
        self.ScoreModel()

    def ScoreModel(self):
        self.bg_word_count, self.F_BG = self.GetWordCount(self.bg_set)
        self.hq_word_count, self.F_HQ = self.GetWordCount(self.hq_set)
        self.lq_word_count, self.F_LQ = self.GetWordCount(self.lq_set)
        self.GetTermFrequency()
        self.CNTD()

    def textToWordsProcessor(self, tweets: list):
        for tweet in tweets:
            yield(self.removeNoisy(tweet))

    def removeNoisy(self, clearText):
        clearText = re.sub("['\"“”’‘@]", '', clearText)
        clearText = re.sub('[^a-zA-Z]', ' ', clearText)         # remove stop words
        clearText = re.sub('http\S*', '', clearText)            # remove web url
        clearText = word_tokenize(str(clearText))
        return clearText

    def GetWordCount(self, tweets):
        tweet_text = [tweet['text'] for tweet in tweets]
        data_words = list(self.textToWordsProcessor(tweet_text))
        word_list = reduce(lambda x, y: x + y, data_words)  # transform two-dimension into one-dimension
        counter = Counter(word_list)
        return counter, len(word_list)

    def GetTermFrequency(self):

        self.BGFrequency = defaultdict(lambda: 0)

        self.HQFrequency = defaultdict(lambda: 0)
        for term in self.listTerms:
            if term in self.hq_word_count.keys():
                self.F_HQ += self.hq_word_count[term]
                self.HQFrequency[term] += self.hq_word_count[term]
                self.BGFrequency[term] += self.bg_word_count[term]

        self.LQFrequency = defaultdict(lambda: 0)
        for term in self.listSpam:
            if term in self.lq_word_count.keys():
                self.F_LQ += self.lq_word_count[term]
                self.LQFrequency[term] += self.lq_word_count[term]
                self.BGFrequency[term] += self.bg_word_count[term]

    def CNTD(self):
        self.HQScore = defaultdict(lambda: 0)
        self.LQScore = defaultdict(lambda: 0)

        for term in self.HQFrequency.keys():
            R_HQ = (self.HQFrequency[term] / self.F_HQ) / (self.BGFrequency[term] / self.F_BG)
            if R_HQ >= 1.5:
                self.HQScore[term] = R_HQ

        for term in self.LQFrequency.keys():
            R_LQ = (self.LQFrequency[term] / self.F_LQ) / (self.BGFrequency[term] / self.F_BG)
            if R_LQ >= 1.0:
                self.LQScore[term] = R_LQ

    def GetScore(self, tweet):
        words = self.removeNoisy(tweet['text'])
        term_score = 1
        spam_score = 1
        for word in words:
            if word in self.HQScore.keys():
                term_score += self.HQScore[word]
        for word in words:
            if word in self.LQScore.keys():
                spam_score += self.LQScore[word]
        return np.log2(term_score / spam_score)

    def HQTweet(self, tweet):
        return self.GetScore(tweet) > 0

if __name__ == '__main__':

    with open('data/highFileFeb', 'r') as f:
        HQSet = []
        for line in f.readlines():
           HQSet.append(json.loads(line))

    with open('data/lowFileFeb', 'r') as f:
        LQSet = []
        for line in f.readlines():
            LQSet.append(json.loads(line))
    
    t = NWScore(HQSet, LQSet)
    print(t.HQScore)
    print(t.LQScore)


