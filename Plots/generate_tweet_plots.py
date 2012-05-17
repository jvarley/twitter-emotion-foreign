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

def grab_totals(emotion=None):
    result = grab_all_times(emotion)
    final_dict = {}
    for entry in result:
        day,hour = parse_date_from_result(entry)
 
        key = "day: " + str(day) + " hour: " + str(hour)
 
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
    rx,ry =grab_totals()
    rx_happy,ry_happy = grab_totals("happy")
    rx_sad, ry_sad = grab_totals("sad")
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

    rx = range(len(rx))

    fig = plt.figure()
    plt.xlabel("Hours Since 4pm EST April 26th")
    plt.ylabel("Percentage of Happy Tweets in green Percentage of Sad Tweets in blue")
    plt.title("French Happy and Sad Tweet Proportions")
    ax = fig.add_subplot(111)
    ax.plot(rx,ry_sad,'o-')
    #ax.plot(rx,ry_happy,'o-')
    #ax.plot(rx,ry_calm,'o-')
    plt.show()
plot_happy_calm_and_sad()
