#Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from matplotlib.pyplot import figure


def createWordCloud():
    df = pd.read_csv("normaldatasets/final_output.csv")
    text2 = " ".join(title for title in df.comment)
    # print(text2)
    word_cloud2 = WordCloud(width=500,height=300,random_state=21,max_font_size=119,collocations = False, background_color = 'white').generate(text2)
    plt.imshow(word_cloud2, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("static/output/wordcloud.png")
    plt.close()
#histogram
def createHistogram():
    df = pd.read_csv("normaldatasets/final_output.csv")
    # text2 = " ".join(title for title in df.comment)
    text2=df.comment

    # df = pd.read_csv("normaldatasets/final_output.csv")
    # description_list = df['comment'].values.tolist()
    
    word_frequency = Counter(" ".join(text2).split()).most_common(10)
    print(word_frequency)
    # words = [word for word, _ in word_frequency]
    # counts = [counts for _, counts in word_frequency]
    # plt.bar(words, counts)
    # plt.title("10 most frequent Words in Comments")
    # plt.ylabel("Frequency")
    # plt.xlabel("Words")
    # plt.show()
    # # plt.savefig("static/output/histogram.png")
    # plt.close()

def createGraph():
    positivenum=0
    negativenum=0
    neutralnum=0
    count=0
    df20 = pd.read_csv("normaldatasets/final_output.csv")
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
        df20=pd.read_csv("normaldatasets/final_output.csv")

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
    plt.savefig("static/output/graph.png")
    plt.switch_backend('agg')
    plt.close()
    return result_text

def createScatteredPlot():
    plt.rcParams['figure.figsize']=[7,5]
    df = pd.read_csv("normaldatasets/final_output.csv")
    polarity=[]
    subjectivity=[]
    i=0
    while i<(len(df)):
        df = list(df.iloc[i])
        i=i+1
        print(df[2],'',df[3],'',df[4])
        polarity.append(df[3])
        subjectivity.append(df[4])
        df=pd.read_csv("normaldatasets/final_output.csv")
    x=polarity
    y=subjectivity
    plt.scatter(x,y,color='blue')
    plt.title('Scattered Plot')
    plt.xlabel('<-- Negative ----------------- Positive -->',fontsize=15)
    plt.ylabel('<------------- Subjectivity -------------->',fontsize=15)
    # plt.show()
    plt.savefig("static/output/scatteredplot.png")
    plt.close()

createWordCloud()
createHistogram()
# result_text=createGraph()
# print(result_text)
# createScatteredPlot()