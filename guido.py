import praw
from nltk.tokenize import sent_tokenize, word_tokenize
from time import sleep
import re
from random import randint
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
 
def word_feats(words):
    return dict([(word, True) for word in words])
 
positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'terrific', 'good', 'nice', 'great', ':)','love','bless','like','hot']
negative_vocab = [ 'bad', 'terrible','useless', 'hate', ':(' ,'shit','ugly','awful','disgusting','damn']
neutral_vocab = [ 'reddit','the','sound','was','is','hey','did','know','words','not','hi','these','those','there']
 
positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
 
train_set = negative_features + positive_features + neutral_features
 
classifier = NaiveBayesClassifier.train(train_set) 

posts=[]
usercomments=[]
text=""
positive=("bada bing, bada boom.")
negative=(" fangul!"," marrone!")

p="piss the shit the fuck dude man the thong theo reeetheos bad bad bad reee damn dammit damnit THE MONEY"

with open("posts.txt") as file:
    posts=file.read().splitlines()

def rip(i):
    pass

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def unmention(b):
    g=[]
    g=b.split("/")
    if g[0]=="u" or g[0]=="U":
        a=str(g[1])
        return a
    else:
        return b

def de(f):
    f=f.lower()
    a=word_tokenize(f)
    for n, i in enumerate(a):
        if i =="the":
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
            a[n]="ova"
        elif i=="here":
            a[n]="hea"
        elif i =="with":
            a[n]="wit"
        elif i=="yes":
            a[n]="yea"
    string=" ".join(a)
    return string

def endsentence(f):
    f=f.lower()
    a=sent_tokenize(f)
    for n, i in enumerate(a):
        count=0
        words = i.split(' ')
        for word in words:
            classResult = classifier.classify( word_feats(word))
            if classResult == 'neg':
                count=count-1
            if classResult == 'pos':
                count=count+1
        if count>0:
            c=positive[randint(0,len(positive)-1)]
        elif count<0:
            c=negative[randint(0,len(negative)-1)]
        else:
            c=""
        a[n]=a[n]+c
    string=" ".join(a)
    return string
    
def guidowords(f): 
    f=f.lower()
    a=word_tokenize(f)
    for n, i in enumerate(a):
        if i in ("man","dude","guy","comrade","person","fellow"):
            c=("goombah","paisan")
            a[n]=c[randint(0,1)]
        elif i in ("meat","pork","salami","idiot","fella","loser","retard","fool"):
            a[n]="gabbagool"
        elif i in ("bathroom","restroom","shitter","juulroom"):
            a[n]="bacous"
        elif i in ("dick","cock","penis","johnson","schlong","shvantz"):
            a[n]="stugots"
        elif i in ("balls","testicles","ballsack"):
            a[n]="maroni"
        elif i in ("woman","girl","chick","female"):
            a[n]="broad"
        elif i in ("women","girls","chicks","females"):
            a[n]="broads"
        elif i in ("shark","ususrer","loaner","landlord","boss"):
            a[n]="strozzino"
        elif i in ("nap","rest"):
            a[n]="pizzolino"
        elif i in ("damn","dammit","damnit"):
            a[n]="mannaggia"
        
    string=" ".join(a)
    return string
            

print(guidowords(de(endsentence(p))))
