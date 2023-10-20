import sys
import requests
import argparse
import logging
import csv
import pandas as pd
context={}
def createFirstcsv():
    APIKEY = "YOURAPIKEY"
    limit = 100
    fileType = 'csv'
    order = 'relevance'
    youtubeLink = input("Insert a youtube video link: ")
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

result=createFirstcsv()
author=result[0]
comment=result[1]

dataframe={"author":author,"comment":comment}
df_first = pd.DataFrame.from_dict(dataframe,orient='index')
df1=df_first.transpose()
df1.columns=['author','comment']
df1.to_csv(r"outputdownloadcomments.csv",header=True,encoding='utf-8',index=False)
context['data']=result[2]
context['title']=result[3]
context['viewcount']=result[4]
context['likecount']=result[5]
context['commentcount']=result[6]

print(context)
