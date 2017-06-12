# -*- coding: utf-8 -*-

from corpus_parsed import *
import collections
import nltk.classify.util
from nltk.metrics import scores
from nltk.classify import NaiveBayesClassifier
from nltk.classify import MaxentClassifier
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk import word_tokenize
import itertools
from random import shuffle

######################################################################################################

spanish_stopwords = stopwords.words('spanish')
non_words = list(punctuation)
non_words.extend(['¿', '¡', ':'])
non_words.extend(map(str,range(10)))


neg_tweets = []
pos_tweets = []

snowball_stemmer = SnowballStemmer('spanish')

def create_word_features(words):

    useful_words = [ snowball_stemmer.stem(word.lower()) for word in words if word not in non_words]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

######################################################################################################

#Tokenize and stemming COST

######################################################################################################

for (words, sentiment) in tweets_corpus_COST:

    words_filtered =[]

    for e in word_tokenize(words):

        if (len(e)>=3 and e not in spanish_stopwords):
            words_filtered.append(''.join(ch for ch, _ in itertools.groupby(e)))

        else:

            pass

    if (sentiment == 1):
        words = words_filtered
        pos_tweets.append((create_word_features(words), 'Positive'))

    elif (sentiment == 0):
        words = words_filtered
        neg_tweets.append((create_word_features(words), 'Negative'))


train_set = pos_tweets + neg_tweets


######################################################################################################

#Tokenize and stemming TASS

######################################################################################################

neg_tweets = []
pos_tweets = []


for (words, sentiment) in tweets_corpus_TASS:

    words_filtered =[]

    for e in word_tokenize(words):

        if (len(e)>=3 and e not in spanish_stopwords):
            words_filtered.append(''.join(ch for ch, _ in itertools.groupby(e)))
        else:

            pass

    if (sentiment == 'P' or sentiment == 'P+'):
        words = words_filtered
        pos_tweets.append((create_word_features(words), 'Positive'))

    elif (sentiment == 'N' or sentiment == 'N+'):
        words = words_filtered
        neg_tweets.append((create_word_features(words), 'Negative'))

    else:

        words = words_filtered
        none_tweets.append((create_word_features(words), "None"))



test_set = pos_tweets + neg_tweets

shuffle(train_set)
shuffle(test_set)

print ('train on %d instances, test on %d instances' % (len(train_set), len(test_set)))

######################################################################################################


classifier = MaxentClassifier.train(train_set, max_iter=30)

#classifier = NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.util.accuracy(classifier, test_set)

print(accuracy * 100)
print (classifier.show_most_informative_features(30))


refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)


for i, (feats, label) in enumerate(test_set):

    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

indicador = {'pos_precision': scores.precision(refsets['Positive'], testsets['Positive']),
'pos_recall': scores.recall(refsets['Positive'], testsets['Positive']),
'pos_F-measure':scores.f_measure(refsets['Positive'], testsets['Positive']),
'neg_precision': scores.precision(refsets['Negative'], testsets['Negative']),
'neg_recall': scores.recall(refsets['Negative'], testsets['Negative']),
'neg_F-measure':scores.f_measure(refsets['Negative'], testsets['Negative'])}


#print ('pos precision:', scores.precision(refsets['Positive'], testsets['Positive']))
print ('pos precision:', indicador['pos_precision'])

print ('pos recall:', scores.recall(refsets['Positive'], testsets['Positive']))
print ('pos F-measure:', scores.f_measure(refsets['Positive'], testsets['Positive']))
print ('neg precision:', scores.precision(refsets['Negative'], testsets['Negative']))
print ('neg recall:', scores.recall(refsets['Negative'], testsets['Negative']))
print ('neg F-measure:', scores.f_measure(refsets['Negative'], testsets['Negative']))

######################################################################################################

#####   Limpieza Tweets

######################################################################################################

def cleaning_tweets(tweet):

    tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet)
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)
    tweet = re.sub(r'#\w+ ?', '', tweet)
    tweet = re.sub(r'_\w+ ?', '', tweet)
    tweet = re.sub(r'\([^)]*\)', '', tweet)
    tweet = re.sub(r'!', '', tweet)
    tweet = re.sub(r'www\.\S+\.com', '', tweet)


    return tweet
