from django.shortcuts import render,HttpResponse
import sys
import requests
import argparse
import logging
import csv
import pandas as pd
import os
from pathlib import Path
import string
import regex as re
from collections import Counter
import matplotlib.pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from wordcloud import WordCloud

context={}
def createScatteredPlot(df,outpath):
    plt.rcParams['figure.figsize']=[7,5]
    df1 = df
    polarity=[]
    subjectivity=[]
    i=0
    # print(df1)
    while i<(len(df1)):
        df1 = list(df1.iloc[i])
        i=i+1
        # print(df1[3])
        polarity.append(df1[3])
        subjectivity.append(df1[4])
        df1 = df
    x=polarity
    y=subjectivity
    plt.scatter(x,y,color='blue')
    plt.title('Scattered Plot')
    plt.xlabel('<-- Negative ----------------- Positive -->',fontsize=15)
    plt.ylabel('<------------- Subjectivity -------------->',fontsize=15)
    plt.savefig(outpath+"scatteredplot.png")
    plt.close()

def createdataset(fname,username_elems,comment_elems):
    all_authors=[]
    all_comments=[]
    for username, comment in zip(username_elems, comment_elems):
        all_authors.append(username.text)
        all_comments.append(comment.text)

    dataframe={"author":all_authors,"comment":all_comments}
    df_first = pd.DataFrame.from_dict(dataframe,orient='index')
    df1=df_first.transpose()
    df1.columns=['author','comment']
    df1.to_csv(fname,header=True,encoding='utf-8',index=False)

def scrape(url,filename1):
    driver=webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(6)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    print("First height at Start: ",last_height)

    c=1
    while True:
        # driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        driver.execute_script("window.scroll(0, 200000);")
        time.sleep(6)
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        print("New height after :",new_height,"at iteration no",c)
        c=c+1

        if new_height == last_height:
            createdataset(filename1,username_elems,comment_elems)
            break
        if new_height>10000 and new_height<13000:
            print("\nSaving For first time\n")
            createdataset(filename1,username_elems,comment_elems)
        if new_height>20000 and new_height<23000:
            print("\nSaving For second time\n")
            createdataset(filename1,username_elems,comment_elems)
        if new_height>30000 and new_height<33000:
            print("\nSaving For third time\n")
            createdataset(filename1,username_elems,comment_elems)
        if new_height>50000 and new_height<53000:
            print("\nSaving For fourth time\n")
            createdataset(filename1,username_elems,comment_elems)
        if new_height>70000 and new_height<73000:
            print("\nSaving For Fifth time\n")
            createdataset(filename1,username_elems,comment_elems)
        if new_height>90000 and new_height<93000:
            print("\nSaving For Sixth time\n")
            createdataset(filename1,username_elems,comment_elems)

        last_height = new_height

    driver.close()

def createWordCloud(df,outpath):
    try:
        text2 = " ".join(title for title in df.comment)
        word_cloud2 = WordCloud(width=500,height=300,random_state=21,max_font_size=119,collocations = False, background_color = 'white').generate(text2)
        plt.imshow(word_cloud2, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(outpath+"wordcloud.png")
        plt.close()
    except Exception as e:
        print("An exception occurred ",e)

def createHistogram(df,outpath):
    description_list = df['comment'].values.tolist()
    word_frequency = Counter(" ".join(description_list).split()).most_common(10)
    words = [word for word, _ in word_frequency]
    counts = [counts for _, counts in word_frequency]
    plt.bar(words, counts)
    plt.title("10 most frequent Words in Comments")
    plt.ylabel("Frequency")
    plt.xlabel("Words")
    # plt.show()
    plt.savefig(outpath+"histogram.png")
    plt.close()

def createGraph(df,outpath):
    positivenum=0
    negativenum=0
    neutralnum=0
    count=0
    df20 = df
    i=0
    all20=[]
    while i<(len(df20)):
        df20 = list(df20.iloc[i])
        i=i+1
        count += 1
        if df20[2]== 'Positive':
            positivenum+=1
        elif df20[2]== 'Negative':
            negativenum+= 1
        else:
            neutralnum+= 1   
        all20.append(df20[2])
        df20=df

    positive_percentage = positivenum / count * 100
    negative_percentage = negativenum / count * 100
    neutral_percentage = neutralnum / count * 100
    
    size1 = positive_percentage / 100 * 360
    size2 = negative_percentage / 100 * 360
    size3 = neutral_percentage / 100 * 360

    result_text=''
    if positive_percentage >= (neutral_percentage + negative_percentage) :
        result_text="YEAH! This Video has Positive Feedback!"
    elif negative_percentage>= (neutral_percentage + positive_percentage):
        result_text="SORRY!! This video got Negative Feedback."
    else :
        result_text="This Video has Neutral Feedback"

    labels = 'Positive', 'Negative ','Neutral'
    sizes = [size1, size2, size3]
    colors = ['Green', 'Red', 'gold']
    explode = (0.01, 0.01, 0.01)

    patches, texts = plt.pie(sizes, explode=explode, colors=colors,startangle=120)

    plt.legend(patches, labels, loc="best")

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%',startangle= 120, textprops={'fontsize': 10})

    plt.tight_layout()
    plt.axis('equal')
    plt.savefig(outpath+"graph.png")
    plt.switch_backend('agg')
    plt.close()
    return result_text

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

def createFirstcsv(data):
    LINK=data
    APIKEY = "AIzaSyAT-aO9o-kfKTSUWNO4u2Yg8f5hy7w5LJM"
    limit = 100
    fileType = 'csv'
    order = 'relevance'
    youtubeLink = LINK
    if(youtubeLink=="e" or youtubeLink=="exit"):
        quit()
    if youtubeLink.find("v="):
        youtubeLink = youtubeLink.split("v=")[1].split("&")[0]
        print(youtubeLink)
    else:
        youtubeLink = youtubeLink.split("/")[3]
        print(youtubeLink)

    v = requests.get(url="https://www.googleapis.com/youtube/v3/videos?id="+youtubeLink+"&part=snippet&part=statistics&key="+APIKEY).json()
    r = requests.get(url = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + APIKEY + "&textFormat=plainText&part=snippet&videoId="+youtubeLink+"&order="+order+"&maxResults="+str(limit)).json()
    response=v
    title=response["items"][0]["snippet"]["title"]
    viewcount=response["items"][0]["statistics"]["viewCount"]
    likecount=response["items"][0]["statistics"]["likeCount"]
    commentcount=response["items"][0]["statistics"]["commentCount"]
    author1=[]
    comment1=[]
    for f in r["items"]:
        author1.append(f["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
        comment1.append(f["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
    return author1,comment1,youtubeLink,title,viewcount,likecount,commentcount

def createFinalCsv(df10,filefrom,fileto):
    all10=[]
    author10=[]
    comment10=[]
    stop_words = ["I","i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
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
        df10 = list(df10.iloc[i])
        i=i+1
        all10.append(df10)
        df10=pd.read_csv(filefrom)
    c=0
    for aut in all10:
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
    for aname in all10:
        author10.append(aname[0])
    for finalcomment in final_words:
        comment10.append(' '.join(finalcomment))

    polarity1=[]
    subjectivity1=[]
    sentiment_type1=[]

    for elm in comment10:
        subjectivity1.append(getSubjectivity(elm))
        polarity1.append(getPolarity(elm))
        sentiment_type1.append(sentiment_scores(elm))


    dataframe={"author":author10,"comment":comment10,"sentiment_type":sentiment_type1,"polarity":polarity1,"subjectivity":subjectivity1}
    df20 = pd.DataFrame.from_dict(dataframe,orient='index')
    df11=df20.transpose()
    df11.columns=['name','comment','sentiment_type','polarity','subjectivity']
    df11.to_csv(fileto,header=True,encoding='utf-8',index=False)

# Create your views here.
def index(request):
    
    if request.method == 'POST':
        # analysis_type=request.POST.get('analysis-type')
        choice=request.POST.get('choice')
        data=request.POST.get('youtube-video-link')
        predata=request.POST.get('preprocess-data')
        
        # print("Link Entered By User : ",data)
        if data and choice == 'choice1':
            result=createFirstcsv(data)
            author=result[0]
            comment=result[1]

            dataframe={"author":author,"comment":comment}
            df_first = pd.DataFrame.from_dict(dataframe,orient='index')
            df1=df_first.transpose()
            df1.columns=['author','comment']
            df1.to_csv(r"normaldatasets/output.csv",header=True,encoding='utf-8',index=False)
            context['data']=result[2]
            context['title']=result[3]
            context['viewcount']=result[4]
            context['likecount']=result[5]
            context['commentcount']=result[6]

            ## Final Output Generator
            df10 = pd.read_csv("normaldatasets/output.csv")
            filefrom="normaldatasets/output.csv"
            fileto="normaldatasets/final_output.csv"
            createFinalCsv(df10,filefrom,fileto)

        else:
            print("no Data")
            context['data']=''
        
        if data and choice == 'choice2':
            link= data
            filename1="deepdatasets/output_deep_from_bot.csv"
            scrape(link,filename1)
        else:
            print("Normal Analysis Selected")
        # if request.POST.get('preprocess_data') == 'preprocess_data':
        # else:
        #     print("No Pre Data ")

        # if request.POST.get('show_result') == 'show_result':
        # else:
        #     print("show_result Button doesnot clicked")

    p = Path("normaldatasets/output.csv")

    if p.exists():
        df = pd.read_csv("normaldatasets/output.csv")
        all=[]
        i=0
        while i<(len(df)):
            df = list(df.iloc[i])
            i=i+1
            all.append(df)
            df=pd.read_csv("normaldatasets/output.csv")
        # context={'all':all}
        context['all'] = all

    q = Path("normaldatasets/final_output.csv")
    if q.exists():
        df1 = pd.read_csv("normaldatasets/final_output.csv")
        all1=[]
        j=0
        while j<(len(df1)):
            df1 = list(df1.iloc[j])
            j=j+1
            all1.append(df1)
            df1=pd.read_csv("normaldatasets/final_output.csv")

        plist=[]
        nlist=[]
        poslist=[]
        neglist=[]

        df50 = pd.read_csv("normaldatasets/final_output.csv")
        i=0
        while i<(len(df50)):
            df50 = list(df50.iloc[i])
            i=i+1
            if df50[2]== 'Positive':
                plist.append(df50[1])
                plist.append(df50[2])
                poslist.append(plist)
                
            elif df50[2]== 'Negative':
                nlist.append(df50[1])
                nlist.append(df50[2])
                neglist.append(nlist)
            else:
                a=1

            plist=[]
            nlist=[]
            df50=pd.read_csv("normaldatasets/final_output.csv")
        context['all1'] = all1
        # print(poslist)
        #wordcloud
        df9 = pd.read_csv("normaldatasets/final_output.csv")
        outpath="static/output/"
        createWordCloud(df9,outpath)
        #histogram
        createHistogram(df9,outpath)
        
        # Graph Maker
        result_text=createGraph(df9,outpath)
        print(result_text)

        #Scattered Plot
        createScatteredPlot(df9,outpath)

        context['result_text']=result_text
        context['poslist'] = poslist
        context['neglist'] = neglist
    return render(request,"index.html",context)

def deepanalyser(request):
    result_codewithharry=createFirstcsv('https://www.youtube.com/watch?v=gfDE2a7MKjA')
    result_apnacollege=createFirstcsv('https://www.youtube.com/watch?v=vLqTf2b6GZw')
    context['data1']=result_codewithharry[2]
    context['title1']=result_codewithharry[3]
    context['viewcount1']=result_codewithharry[4]
    context['likecount1']=result_codewithharry[5]
    context['commentcount1']=result_codewithharry[6]

    context['data2']=result_apnacollege[2]
    context['title2']=result_apnacollege[3]
    context['viewcount2']=result_apnacollege[4]
    context['likecount2']=result_apnacollege[5]
    context['commentcount2']=result_apnacollege[6]

    file1="deepdatasets/deepoutput_codewithharry_pythonvideo1.csv"
    file2="deepdatasets/deepfinal/final_deepoutput_codewithharry_pythonvideo1.csv"
    df1=pd.read_csv(file1)
    filefrom=file1
    fileto=file2
    createFinalCsv(df1,filefrom,fileto)

    df9=pd.read_csv(file2)
    outpath="static/output/pythonvideo1/"
    createWordCloud(df9,outpath)
    createHistogram(df9,outpath)
    createScatteredPlot(df9,outpath)
    result_text=createGraph(df9,outpath)


    file3="deepdatasets/deepoutput_apnacollege_pythonvideo.csv"
    file4="deepdatasets/deepfinal/deepoutput_apnacollege_pythonvideo.csv"

    df5=pd.read_csv(file3)
    filefrom5=file3
    fileto5=file4
    createFinalCsv(df5,filefrom5,fileto5)

    df6=pd.read_csv(file4)
    outpath5="static/output/pythonvideo2/"
    createWordCloud(df6,outpath5)
    createHistogram(df6,outpath5)
    createScatteredPlot(df6,outpath5)
    result_text=createGraph(df6,outpath5)
    # context['data']='After Datatable'
    return render(request,"deepanalyser.html",context)