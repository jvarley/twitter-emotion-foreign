#!/usr/bin/env python
import numpy as np
import psycopg2
import matplotlib.pyplot as plt

def get_connection():
    conn = psycopg2.connect("dbname='nlptweets' host='localhost' user='jvarley' password='password'")
    return conn


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

def grab_emotion_frequencies():
    connection = get_connection()
    cur = connection.cursor()

    cur.execute("SELECT emotion from tweets;")

    result = cur.fetchall()
    emotion_dict = {}
    for elt in result:
        emotion = elt[0]
        if emotion_dict.has_key(emotion):
            emotion_dict[emotion] +=1
        else:
            emotion_dict[emotion] =0

    results_x = []
    results_y = []
    labels = []
    count = 0
    for key in emotion_dict.keys():
        labels.append(key)
        results_x.append(count)
        results_y.append(emotion_dict[key])
        count += 1

    return (labels,results_x,results_y)

labels,results_x,results_y = grab_emotion_frequencies()
N = 5
N = len(results_y)
menMeans = (20, 35, 30, 35, 27)
menStd =   (2, 3, 4, 1, 2)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars


plt.subplot(111)

#rects1 = plt.bar(ind,menMeans , width,
                    #color='r')
                    #yerr=menStd,
                    #error_kw=dict(elinewidth=6, ecolor='pink'))
rects1 = plt.bar(ind,results_y,width,color='r')


womenMeans = (25, 32, 34, 20, 25)
womenStd =   (3, 5, 2, 3, 3)

#rects2 = plt.bar(ind+width, womenMeans, width,
                    #color='y')
                    #yerr=womenStd,
                    #error_kw=dict(elinewidth=6, ecolor='yellow'))


# add some
plt.ylabel('Scores')
plt.title('Scores by group and gender')
plt.xticks(ind+width, ('G1', 'G2', 'G3', 'G4', 'G5') )

#plt.legend( (rects1[0]), ('Men') )


#autolabel(rects1)
#autolabel(rects2)

plt.show()
