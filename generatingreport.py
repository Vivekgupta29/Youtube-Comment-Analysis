import pandas as pd
import matplotlib.pyplot as plt

positivenum=0
negativenum=0
neutralnum=0
count=0

df20 = pd.read_csv("final_output.csv")
i=0
all20=[]
while i<98:
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
    df20=pd.read_csv("final_output.csv")

positive_percentage = positivenum / count * 100
negative_percentage = negativenum / count * 100
neutral_percentage = neutralnum / count * 100

size1 = positive_percentage / 100 * 360
size2 = negative_percentage / 100 * 360
size3 = neutral_percentage / 100 * 360


print(" ==> PERCENTAGE OF COMMENTS THAT ARE POSITIVE : ",positive_percentage,"%\n")
print(" ==> PERCENTAGE OF COMMENTS THAT ARE NEGATIVE : ",negative_percentage,"%\n")
print(" ==> PERCENTAGE OF COMMENTS THAT ARE NEUTRAL  : ",neutral_percentage,"%\n")
print(" ==> CALCULATING FINAL RESULT.. :-\n")
print(" ********************************************************************\n")

if positive_percentage >= (neutral_percentage + negative_percentage + 10) :
    print(" ==> GREAT JOB!! You got positive feeback.")
elif negative_percentage>= (neutral_percentage + positive_percentage + 10):
    print(" ==> SORRY!! You got negative feedback.")
else :
    print(" ==> NICE TRY!! You got neutral feedback.")
print("\n ********************************************************************\n")

labels = 'Positive', 'Negative ','Neutral'
sizes = [size1, size2, size3]
colors = ['Green', 'Red', 'gold']
explode = (0.01, 0.01, 0.01)

patches, texts = plt.pie(sizes, explode=explode, colors=colors
,startangle=120)

plt.legend(patches, labels, loc="best")

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%',startangle= 120, textprops={'fontsize': 10})

plt.tight_layout()
plt.axis('equal')
# plt.show()
plt.savefig("graph.png")