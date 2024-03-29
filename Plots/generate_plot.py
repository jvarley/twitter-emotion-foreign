import numpy as np
import matplotlib.pyplot as plt
import os
import random
import re


def plot_emotions():
    pwd = os.path.pardir
    f = open(pwd + '/LiveJournal/output4/final_output_fr_emotions.txt')
    count = 0
    emotions = []
    for line in f.readlines():
        if re.findall(r'\w.html',line) == [] and line != "\n":
            if line[-1] == "\n":
                line = line[:-1]
                if line[0] == " ":
                    line = line[1:]
                
            print "line:" + line
            emotions.append(line)
            count +=1 
            print count
    emotion_set = set(emotions)
    print len(emotion_set)
    emotion_count = {}
    for emotion in emotion_set:
        emotion_count[emotion] = 0
    for emotion in emotions:
        emotion_count[emotion] += 1
    emotion_freq = []
    for key in emotion_count.keys():
        print "key: " + str(key) +  " value: " + str(emotion_count[key])
        emotion_freq.append((emotion_count[key],key))
    #emotion_freq = emotion_freq.sort
    for elt in  sorted(emotion_freq)[::-1]:
        print str(elt)
        


def plot(array):

    N = len(array[0][1][0])
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for emotion_set in array:
        dates = emotion_set[1][0]
        values = emotion_set[1][1]
        emotion = emotion_set[0]
        ax.plot(dates,values,'o-')

    plt.show()

def example_plot():
    date = [0,1,2,3]
    value = [100,5,10,50]
    date2 = [4,1,2,3]
    value2 = [11,12,13,14]
   
    plot([
            ["happy",[date,value]],
            ["sad",[date2,value2]]])

if __name__ == "__main__":
    #example_plot()
    plot_emotions()
