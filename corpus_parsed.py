# -*- coding: utf-8 -*-

from lxml import etree
from lxml import objectify
import pandas as pd
from nltk.corpus import stopwords
from string import punctuation
from nltk.tokenize import word_tokenize
import re

######################################################################################################


pd.set_option('display.width', 1000)


######################################################################################################

############################################## Parser COST ###########################################

######################################################################################################


general_tweets_corpus_train = pd.read_csv('cost_final.csv', sep = ',', encoding='utf-8', error_bad_lines=False)
tweets_corpus = general_tweets_corpus_train



tweets_corpus['texto'] = tweets_corpus['texto'].map(lambda x: re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', x))
tweets_corpus['texto'] = tweets_corpus['texto'].map(lambda x: re.sub(r'@[A-Za-z0-9]+', "", x))
tweets_corpus['texto'] = tweets_corpus['texto'].map(lambda x: re.sub(r'#\w+ ?', '', x))
tweets_corpus['texto'] = tweets_corpus['texto'].map(lambda x: re.sub(r'_', '', x))
tweets_corpus['texto'] = tweets_corpus['texto'].map(lambda x: re.sub(r'\([^)]*\)', '', x))
tweets_corpus['texto'] = tweets_corpus['texto'].map(lambda x: re.sub(r'!', "", x))
tweets_corpus['texto'] = tweets_corpus['texto'].map(lambda x: re.sub(r',', "", x))


subset = tweets_corpus[['texto', 'polarity']]

tuples = [tuple(x) for x in subset.values]

tweets_corpus_pos = []
tweets_corpus_neg = []

#classify tuples

for item in tuples:

	if item[1]== 1:
		tweets_corpus_pos.append(item)

	elif item[1]== 0:
		tweets_corpus_neg.append(item)


tweets_corpus_COST = tweets_corpus_neg + tweets_corpus_pos

######################################################################################################

#####################################   Parser TASS  #################################################

######################################################################################################



pd.set_option('display.width', 1000)
general_tweets_corpus_train = pd.DataFrame(columns=('user', 'id', 'content', 'polarity', 'agreement'))
xml_data = 'TASS/general-tweets-train-tagged.xml'
xml = objectify.parse(open(xml_data))
root = xml.getroot()
tweets = root.getchildren()

for i in range(0,len(tweets)):

	tweet = tweets[i]
	row = dict(zip(['user', 'id', 'content', 'polarity', 'agreement'], [tweet.user.text, tweet.tweetid.text,
		tweet.content.text, tweet.sentiments.polarity.value.text, tweet.sentiments.polarity.type.text]))

	row_s = pd.Series(row)
	row_s.name = i
	general_tweets_corpus_train = general_tweets_corpus_train.append(row_s)


tweets_corpus = general_tweets_corpus_train


tweets_corpus['content'] = tweets_corpus['content'].map(lambda x: re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', x))
tweets_corpus['content'] = tweets_corpus['content'].map(lambda x: re.sub(r'@[A-Za-z0-9]+', "", x))
tweets_corpus['content'] = tweets_corpus['content'].map(lambda x: re.sub(r'#\w+ ?', '', x))
tweets_corpus['content'] = tweets_corpus['content'].map(lambda x: re.sub(r'_\w+ ?', '', x))
tweets_corpus['content'] = tweets_corpus['content'].map(lambda x: re.sub(r'\([^)]*\)', '', x))
tweets_corpus['content'] = tweets_corpus['content'].map(lambda x: re.sub(r'!', "", x))
tweets_corpus['content'] = tweets_corpus['content'].map(lambda x: re.sub(r'"', "", x))
tweets_corpus['content'] = tweets_corpus['content'].map(lambda x: re.sub(r'RT', "", x))

tweets_corpus = tweets_corpus.query('agreement != "DISAGREEMENT" and polarity != "NONE"')


subset = tweets_corpus[['content', 'polarity']]

tuples = [tuple(x) for x in subset.values]

tweets_corpus_pos = []
tweets_corpus_neg = []

#classify tuples

for item in tuples:

	if item[1]=='P+':
		tweets_corpus_pos.append(item)

	elif item[1]=='P':
		tweets_corpus_pos.append(item)

	elif item[1]=='N+':
		tweets_corpus_neg.append(item)

	elif item[1]=='N':
		tweets_corpus_neg.append(item)

tweets_corpus_TASS = tweets_corpus_neg + tweets_corpus_pos
