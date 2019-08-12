#! /usr/bin/env python3

import praw
from nltk.tokenize import sent_tokenize, word_tokenize
from time import sleep
import time
import re
from random import randint
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
from nltk.tokenize.treebank import TreebankWordDetokenizer

def word_feats(words):
    return dict([(word, True) for word in words])
 
positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'wonderful' 'good', 'nice', 'great', ':)','love','bless','like','hot']
negative_vocab = [ 'bad', 'terrible','useless', 'hate', ':(' ,'shit','ugly','awful','disgusting','damn']
neutral_vocab = [ 'reddit','the','sound','was','name','is','hey','did','know','words','not','hi','these','those','there','dog']
 
positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
 
train_set = negative_features + positive_features + neutral_features
 
classifier = NaiveBayesClassifier.train(train_set) 

positive=(" bada bing.")
negative=(" fangul!"," marrone!")


class guidobot:
	
	reddit=praw.Reddit("bot1")
	
	def __init__(self, last_time):
		self.last_time = last_time
 
	def replycomment(self):
		for mention in self.reddit.inbox.unread(limit=None):
			if mention.parent_id.split("_")[0]=="t3":
				text=(str(mention.parent().selftext.lower()))[:5000]
				guidoifiedtext=self.guidowords(self.endsentence(text))
			elif mention.parent_id.split("_")[0]=="t1":
				text=str(mention.parent().body.lower())
				guidoifiedtext=self.guidowords(self.endsentence(text))
			else:
				guidoifiedtext="fangul! theres nothing hea fuh me."
			mention.reply(guidoifiedtext)
			self.reddit.inbox.mark_read([mention])

	def endsentence(self, f):
		f=f.lower()
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		a=sent_detector.tokenize(f)
		for n, i in enumerate(a):
			count=0
			words = word_tokenize(i)
			for word in words:
				classResult = classifier.classify(word_feats(word))
				if classResult == 'neg':
					count=count-1
				if classResult == 'pos':
					count=count+1
			if count>1:
				c=positive[randint(0,len(positive)-1)]
			elif count<-1:
				c=negative[randint(0,len(negative)-1)]
			else:
				c=""
			a[n]=a[n]+c
		string=TreebankWordDetokenizer().detokenize(a)
		return string
    
	def guidowords(self, f): 
		f=f.lower()
		a=word_tokenize(f)
		for n, i in enumerate(a):
			if i in ("man","dude","guy","comrade","person","fellow","fella","friend","countryman","classmate","brother"):
				a[n]="paisan"
			elif i in ("men","dudes","guys","comrades","persons","fellows","fellas","friends","countrymen","classmates","brothers","folks","folx","folk"):
				a[n]="paisanos"
			elif i in ("meat","pork","salami","pepperoni","sausage","idiot","loser","retard","fool","moron","dunce","redditor"):
				a[n]="gabbagool"
			elif i in ("meats","porks","salamis","pepperonis","sausages","idiots","losers","retards","fools","morons","dunces","redditors"):
				a[n]="gabbagools"
			elif i in ("dick","cock","penis","johnson","schlong","shvantz","weewee","peepee","phallus"):
				a[n]="stugots"
			elif i in ("dicks","cocks","penises","johnsons","schlongs","shvantzes","weewees","peepees","phalluses"):
				a[n]="stugotses"
			elif i in ("balls","testicles","ballsack","nuts"):
				a[n]="maroni"
			elif i in ("woman","girl","chick","female","wife"):
				a[n]="broad"
			elif i in ("women","girls","chicks","females","wives"):
				a[n]="broads"
			elif i in ("ususrer","loaner","landlord","boss"):
				a[n]="strozzino"
			elif i in ("ususrers","loaners","landlords","bosses"):
				a[n]="strozzinos"
			elif i in ("nap","rest","sleep"):
				a[n]="pizzolino"
			elif i in ("naps"):
				a[n]="pizzolinos"
			elif i in ("dog","woofer","canine","wolf","fox","puppy","puppie","pup"):
				a[n]="dago"
			elif i in ("dogs","woofers","canines","wolves","foxes","puppies","pups"):
				a[n]="dagos"
			elif i =="the":
				c=("de","de","da")
				a[n] = c[randint(0,2)]
			elif i=="for":
				a[n]="fuh"
			elif i=="this":
				a[n]="dis"
			elif i=="these":
				a[n]="dese"
			elif i=="that":
				a[n]="dat"
			elif i=="hey":
				a[n]="eyy"
			elif i=="over":
				c=("ovuh","ova")
				a[n] = c[randint(0,1)]
			elif i=="here":
				a[n]="hea"
			elif i =="with":
				a[n]="wit"
			elif i=="yes":
				a[n]="yea"
		string=TreebankWordDetokenizer().detokenize(a)
		return string
            
	def run(self):
		while True:
			#if 60 seconds has elapsed since last Looking for comments print
			if time.time() - self.last_time >= 60:
				print("Looking for comments...")
				self.last_time = time.time()

			#find and reply to relevant comments
			self.replycomment()

			#make the bot wait a little
			sleep(5)


guido_bot = guidobot(time.time())
guido_bot.run()
