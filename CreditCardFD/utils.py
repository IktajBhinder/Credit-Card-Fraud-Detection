from typing import BinaryIO
import pandas as pd
import json
import pickle
import base64
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
from matplotlib.figure import Figure
import seaborn as sns
from PIL import Image
import mpld3
def dataview1(name):
    df=pd.read_csv(name)
    df1=df.head(500)
    json_records = df1.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    return data


def pred(name):
    df=pd.read_csv(name)
    print(df)
    global datawithcol
    datawithcol=df
    X = df
    # Getting the values of X and Y (Numpy array with no columns)
    xTest = X.values
    Modelname = 'CreditCardFD\model.pkl'
    #Load the Model back from file
    with open(Modelname, 'rb') as file:
        rfc = pickle.load(file)
    #Predict the value of 'Class' using the reloaded Model
        yPred = rfc.predict(xTest)

    datawithcol.insert(1, "Predicted_Class", yPred, True)
    return datawithcol

def analysis(name):
     dfa=pred(name)  
     describe=dfa.describe()
     describe=describe.to_html()
     dshape=dfa.shape
     uniqueId = dfa["Predicted_Class"].unique() 
     totalrec=dfa["Predicted_Class"].count()
     fraud= dfa["Predicted_Class"].sum()
     fraudper = (fraud/totalrec) *100
     nonf= 100 - fraudper
     nonfcount= totalrec - fraud
     data={"dshape": dshape,"uniqueId":uniqueId,"totalrec":totalrec,"fraud":fraud,"fraudper":fraudper,"nonf":nonf,"nonfcount":nonfcount,"describe":describe}
     return data


def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_piechart(x,y):
    y = np.array([x,y])
    mylabels = ["Fraudulent Cases", "Non-Fraudulent Cases"]
    myexplode = [0, 0]
    mycolor=['red', 'green']
    plt.clf()
    plt.figure()
    plt.pie(y, labels = mylabels, explode = myexplode, radius= 0.8,colors=mycolor,startangle=0)
    plt.legend( mylabels, loc="best")
    #plt.axis('square')
    plt.tight_layout()
    graph=get_graph()
    return graph

def get_barchart(x,y):
    y = np.array([x,y])
    mycolor=['red', 'green']
    mylabels = ["Fraudulent Cases", "Non-Fraudulent Cases"]
    plt.clf()
    plt.figure(figsize = (10, 5))
    colors = {'Fraudulent Cases':'red', 'Non-Fraudulent Cases':'green'}         
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(handles, labels)
# creating the bar plot
    plt.bar(mylabels,y,color=mycolor,
        width = 0.7)
    plt.xlabel("Types of Cases")
    plt.ylabel("Count of Cases")
    plt.title("Bar plot showing cases")
    graph=get_graph()
    return graph

def get_heatmap(name):
    #datawithcol=pred(name)
    plt.clf()
    ht=plt.subplots(figsize=(20,11))
    sns.set(font_scale=1)
    ht = sns.heatmap(datawithcol.iloc[:, 2:30].corr(), linewidths=0.8, annot=True,annot_kws={"size": 6.5}, fmt='.0%',cmap="YlGnBu")
    ht.set_yticklabels(ht.get_yticklabels(), rotation=0)
    ht.set_xticklabels(ht.get_xticklabels(), rotation=90)
    graph=get_graph()
    plt.title("Heatmap", fontsize=20)
    return graph

def line_chart(var='Amount'):
    rsltdf = datawithcol.loc[datawithcol['Predicted_Class'] == 1]
    count=rsltdf['Predicted_Class'].count()

    xside=[]
    for i in range(rsltdf['Predicted_Class'].count()):
        xside.append(i+1)

    ys=rsltdf[var]
    yside=ys.values.tolist()
#colors1 = np.random.rand(rsltdf['Predicted_Class'].count())
    plt.clf()
    plt.figure(figsize = (10, 5))
    plt.plot(xside, yside,marker='o')

    plt.xlabel("Fraudulent Cases")
    plt.ylabel(var)
    linelabel=[]
    linelabel.append(var)
    plt.legend( linelabel,loc="best")
    plt.title("Dynamic Line Chart ", fontsize=20)
    graph=get_graph()
    return graph

def dist_plot():
    plt.clf()
    fig, ax = plt.subplots(1, 2, figsize=(18,10))
    rsltdf = datawithcol.loc[datawithcol['Predicted_Class'] == 1]
    amount_val = rsltdf['Amount'].values
    time_val = rsltdf['Time'].values

    sns.distplot(amount_val, ax=ax[0], color='r')
    ax[0].set_title('Distribution of Transaction Amount', fontsize=14)
    ax[0].set_xlim([min(amount_val), max(amount_val)])

    sns.distplot(time_val, ax=ax[1], color='b')
    ax[1].set_title('Distribution of Transaction Time', fontsize=14)
    ax[1].set_xlim([min(time_val), max(time_val)])
    graph=get_graph()
    return graph