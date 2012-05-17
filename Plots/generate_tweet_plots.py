#Jake Varley
#from terminal to access postgres:
#sudo -u postgres psql nlptweets
#nlptweets=# select created_at from tweets;
import psycopg2
import numpy as np
import matplotlib.pyplot as plt

def get_connection():
    conn = psycopg2.connect("dbname='nlptweets' host='localhost' user='jvarley' password='password'")
    return conn

def grab_all_times(emotion = None):
    connection = get_connection()
    cur = connection.cursor()
    if emotion == None:
        cur.execute("SELECT created_at from tweets;")
    else:
        cur.execute("SELECT created_at from tweets WHERE emotion= '%s';" %(emotion,))
    result = cur.fetchall()
    return result


def parse_date_from_result(entry):
    day= entry[0][8:10]
    if day == "26":
        day = "00"
    elif day == "27":
        day = "01"
    elif day == "28":
        day = "02"
    elif day == "29":
        day = "03"
    elif day == "30":
        day  = "04"
    elif day=="01":
        day = "05"
    elif day=="02":
        day = "06"

    hour = entry[0][11:13]
    return (day,hour)

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
    count = 0
    for key in emotion_dict.keys():
        results_x.append(count)
        results_y.append(emotion_dict[key])
        count += 1
        
    fig = plt.figure()
    plt.xlabel("Hours Since 4pm EST April 26th")
    plt.ylabel("Number of French Tweets")
    plt.title("French Tweet Frequencies")
    ax = fig.add_subplot(111)
    ax.plot(results_x,results_y,'o-')
    plt.show()


def grab_totals(emotion=None):
    compress_to_single_day = True
    result = grab_all_times(emotion)
    final_dict = {}
    for entry in result:
        day,hour = parse_date_from_result(entry)
 
        if not compress_to_single_day:
            key = "day: " + str(day) + " hour: " + str(hour)
        else:
            key = " hour: " + str(hour)
        if final_dict.has_key(key):
            count = final_dict[key][2]
            final_dict[key] = (day,hour,count+1)
        else:
            final_dict[key] =(day,hour,0)
    results_x = []
    results_y = []
    values = []
    for key in final_dict.keys():
        values.append(final_dict[key])
    for elt in sorted(values):
        print elt
        results_x.append("day: " + elt[0] + " hr: " + elt[1])
        results_y.append(elt[2])
        print len(values)
    return (results_x,results_y)

def plot_totals():
    rx,ry =grab_totals()

    rx = range(len(rx))

    fig = plt.figure()
    plt.xlabel("Hours Since 4pm EST April 26th")
    plt.ylabel("Number of French Tweets")
    plt.title("French Tweet Frequencies")
    ax = fig.add_subplot(111)
    ax.plot(rx,ry,'o-')
    plt.show()

def plot_happy():
    rx,ry =grab_totals()
    rx_happy,ry_happy = grab_totals("happy")
    for i in range(len(ry_happy)):
        ry_happy[i] = ry_happy[i]/float(ry[i])

    rx = range(len(rx))

    fig = plt.figure()
    plt.xlabel("Hours Since 4pm EST April 26th")
    plt.ylabel("Number of Happy French Tweets/Total Tweets For Bin")
    plt.title("French Happy Tweet Proportions")
    ax = fig.add_subplot(111)
    ax.plot(rx,ry_happy,'o-')
    plt.show()

def plot_happy_and_sad():
    rx,ry =grab_totals(False)
    rx_happy,ry_happy = grab_totals(False,"happy")
    rx_sad, ry_sad = grab_totals(False,"sad")
    for i in range(len(ry_happy)):
        ry_happy[i] = ry_happy[i]/float(ry[i])
        ry_sad[i] = ry_sad[i]/float(ry[i])

    rx = range(len(rx))

    fig = plt.figure()
    plt.xlabel("Hours Since 4pm EST April 26th")
    plt.ylabel("Percentage of Happy Tweets in green Percentage of Sad Tweets in blue")
    plt.title("French Happy and Sad Tweet Proportions")
    ax = fig.add_subplot(111)
    ax.plot(rx,ry_sad,'o-')
    ax.plot(rx,ry_happy,'o-')
    plt.show()

def plot_happy_calm_and_sad():
    rx,ry =grab_totals()
    rx_happy,ry_happy = grab_totals("happy")
    rx_sad, ry_sad = grab_totals("sad")
    rx_calm,ry_calm = grab_totals("calm")
    for i in range(len(ry_happy)):
        ry_happy[i] = ry_happy[i]/float(ry[i])
        ry_sad[i] = ry_sad[i]/float(ry[i])
        ry_calm[i] = ry_calm[i]/float(ry[i])

    print len(rx)
    print len(rx_sad)
    print len(rx_calm)
    rx = range(len(rx))

    fig = plt.figure()
    plt.xlabel("Hours Since 4pm EST April 26th")
    plt.ylabel("Percentages: Happy-green Sad-blue Calm-red")
    plt.title("French Happy, Sad, and Calm Tweet Proportions")
    ax = fig.add_subplot(111)
    ax.plot(rx,ry_sad,'o-')
    ax.plot(rx,ry_happy,'o-')
    ax.plot(rx,ry_calm,'o-')
    plt.show()

def plot_sad_single_day():
    rx,ry =grab_totals()
    rx_happy,ry_happy = grab_totals("happy")
    rx_sad, ry_sad = grab_totals("sad")
    rx_calm,ry_calm = grab_totals("calm")
    for i in range(len(ry_happy)):
        ry_happy[i] = ry_happy[i]/float(ry[i])
        ry_sad[i] = ry_sad[i]/float(ry[i])
        ry_calm[i] = ry_calm[i]/float(ry[i])

    rx = range(len(rx_sad))

    fig = plt.figure()
    plt.xlabel("Hours Since 4pm")
    plt.ylabel("Percentage of Total Tweets That are Sad")
    plt.title("Daily Sad Tweet Percentages")
    ax = fig.add_subplot(111)
    ax.plot(rx,ry_sad,'o-')
    #ax.plot(rx,ry_happy,'o-')
    #ax.plot(rx,ry_calm,'o-')
    plt.show()

def plot_tired_single_day():
    rx,ry =grab_totals()
    rx_happy,ry_happy = grab_totals("happy")
    rx_sad, ry_sad = grab_totals("sad")
    rx_calm,ry_calm = grab_totals("calm")
    rx_tired,ry_tired = grab_totals("tired")
    for i in range(len(ry_happy)):
        ry_happy[i] = ry_happy[i]/float(ry[i])
        ry_sad[i] = ry_sad[i]/float(ry[i])
        ry_calm[i] = ry_calm[i]/float(ry[i])
        ry_tired[i] = ry_tired[i]/float(ry[i])

    rx = range(len(rx_sad))

    fig = plt.figure()
    plt.xlabel("Hours Since 4pm EST")
    plt.ylabel("Percentage of Total Tweets That are Tired")
    plt.title("Daily Tired Tweet Percentages")
    ax = fig.add_subplot(111)
    ax.plot(rx,ry_tired,'o-')
    #ax.plot(rx,ry_sad,'o-')
    #ax.plot(rx,ry_happy,'o-')
    #ax.plot(rx,ry_calm,'o-')
    plt.show()

def plot_drunk():
    rx,ry =grab_totals()
    rx_happy,ry_happy = grab_totals("happy")
    rx_sad, ry_sad = grab_totals("sad")
    rx_drunk,ry_drunk = grab_totals("drunk")
    #rx_tired,ry_tired = grab_totals("tired")
    for i in range(len(ry_happy)):
        ry_happy[i] = ry_happy[i]/float(ry[i])
        ry_sad[i] = ry_sad[i]/float(ry[i])
        ry_drunk[i] = ry_drunk[i]/float(ry[i])
        #ry_tired[i] = ry_tired[i]/float(ry[i])

    rx = range(len(rx_sad))

    fig = plt.figure()
    plt.xlabel("Hours Since 4pm EST")
    plt.ylabel("Percentage of Total Tweets That are Drunk")
    plt.title("Daily Drunk Tweet Percentages")
    ax = fig.add_subplot(111)
    ax.plot(rx,ry_drunk,'o-')
    #ax.plot(rx,ry_sad,'o-')
    #ax.plot(rx,ry_happy,'o-')
    #ax.plot(rx,ry_calm,'o-')
    plt.show()


#plot_tired_single_day()
#grab_emotion_frequencies()
plot_drunk()
