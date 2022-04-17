import csv
import pandas as pd
import string
import regex as re
from collections import Counter
import matplotlib.pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_scores(sentence):
	sid_obj = SentimentIntensityAnalyzer()
	sentiment_dict = sid_obj.polarity_scores(sentence)
	if sentiment_dict['compound'] >= 0.05 :
		return 'Positive'
	elif sentiment_dict['compound'] <= - 0.05 :
		return 'Negative'
	else :
		return 'Neutral'

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return TextBlob(text).sentiment.polarity

df10 = pd.read_csv("output.csv")
author=[]
comment=[]
all=[]
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
final_words=[]
emotion_list = []

i=0
while i<(len(df10)):
    df10 = list(df.iloc[i])
    i=i+1
    all.append(df10)
    df10=pd.read_csv("output.csv")
# print(all)

c=0
for aut in all:
    #for lower case
    lower_case=aut[1].lower()
    cleaned_text=lower_case.translate(str.maketrans('','',string.punctuation))
    c=c+1
    #for removing Special Characters
    new_list=re.sub('[^A-Za-z0-9\s]+', '', aut[1])

    #for tokenization
    tokenized_words=new_list.split()

    for word in tokenized_words:
        if word in stop_words:
            tokenized_words.remove(word)
    final_words.append(tokenized_words)
for aname in all:
    author.append(aname[0])
for finalcomment in final_words:
    comment.append(' '.join(finalcomment))

polarity1=[]
subjectivity1=[]
sentiment_type1=[]

for elm in comment:
    subjectivity1.append(getSubjectivity(elm))
    polarity1.append(getPolarity(elm))
    sentiment_type1.append(sentiment_scores(elm))


dataframe={"author":author,"comment":comment,"sentiment_type":sentiment_type1,"polarity":polarity1,"subjectivity":subjectivity1}
df20 = pd.DataFrame.from_dict(dataframe,orient='index')
df11=df20.transpose()
df11.columns=['name','comment','sentiment_type','polarity','subjectivity']
df11.to_csv(r"final_output.csv",header=True,encoding='utf-8',index=False)