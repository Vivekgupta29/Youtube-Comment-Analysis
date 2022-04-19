import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from matplotlib.pyplot import figure
# p = Path("output.csv")
# if p.exists():
#     df = pd.read_csv("output.csv")
#     all=[]
#     i=0
#     while i<100:
#         df = list(df.iloc[i])
#         i=i+1
#         all.append(df)
#         df=pd.read_csv("output.csv")
#     # context={'all':all}
#     print(all)

# print("\n\n")
# q = Path("final_output.csv")
# if q.exists():
#     df1 = pd.read_csv("final_output.csv")
#     all1=[]
#     j=0
#     while j<100:
#         df1 = list(df1.iloc[j])
#         j=j+1
#         all1.append(df1)
#         df1=pd.read_csv("final_output.csv")
#     print(all1)


# col_list = ["comment", "sentiment_type"]
# df30 = pd.read_csv("normaldatasets/final_output.csv", usecols=col_list)
# all2=[]
# k=0
# # print(df30["comment"]+" "+df30["sentiment_type"])
# # comment = df30['comment'].tolist()
# # senti = df30['sentiment_type'].tolist()
# # print(comment)

# while k<(len(df30)):
#     df30 = list(df30.iloc[k])
#     k=k+1
#     all2.append(df30)
#     df30=pd.read_csv("normaldatasets/final_output.csv")
# print(all2)


# count=0
# positivenum=0
# negativenum=0
# neutralnum=0
# plist=[]
# nlist=[]
# poslist=[]
# neglist=[]
# df50 = pd.read_csv("normaldatasets/final_output.csv")
# i=0
# while i<(len(df50)):
#     df50 = list(df50.iloc[i])
#     i=i+1
#     count += 1
#     if df50[2]== 'Positive':
#         plist.append(df50[1])
#         plist.append(df50[2])
#         poslist.append(plist)
        
#     elif df50[2]== 'Negative':
#         nlist.append(df50[1])
#         nlist.append(df50[2])
#         neglist.append(nlist)
#     else:
#         a=1
#         # print(df50[1]+""+df50[2])
#     plist=[]
#     nlist=[]
#     df50=pd.read_csv("normaldatasets/final_output.csv")


# df=pd.read_csv('deepdatasets/deepfinal/deepoutput_apnacollege_pythonvideo.csv')
# text2=str(df.comment)
# word_cloud2 = WordCloud(width=500,height=300,random_state=21,max_font_size=119,collocations = False, background_color = 'white').generate(text2)
# plt.imshow(word_cloud2, interpolation='bilinear')
# plt.axis("off")
# plt.show()
# plt.close()

# df=pd.read_csv('deepdatasets/deepfinal/final_deepoutput_codewithharry_pythonvideo1.csv')
# description_list = df['comment'].values.tolist()
# # print(description_list)
# word_frequency = Counter(" ".join(description_list).split()).most_common(10)
# print(word_frequency)
# words = [word for word, _ in word_frequency]
# counts = [counts for _, counts in word_frequency]

# # words=[text2]
# # counts=[20,30,40,50,60]
# plt.bar(words, counts)
# plt.title("10 most frequent Words in Comments")
# plt.ylabel("Frequency")
# plt.xlabel("Words")
# plt.show()
# # plt.savefig(outpath+"histogram.png")
# plt.close()


# pd.DataFrame.hist(column='comment')
# pd.DataFrame.plot(kind='hist')
# pd.DataFrame.plot.hist()

df.plot(kind='hist',
        alpha=0.7,
        bins=30,
        title='Histogram Of Test Scores',
        rot=45,
        grid=True,
        figsize=(12,8),
        fontsize=15, 
        color=['#A0E8AF', '#FFCF56'])
plt.xlabel('Test Score')
plt.ylabel("Number Of Students")