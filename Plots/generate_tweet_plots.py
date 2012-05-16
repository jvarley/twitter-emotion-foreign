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

def grab_all_times():
    connection = get_connection()
    cur = connection.cursor()
    cur.execute("SELECT created_at from tweets;")
    result = cur.fetchall()
    return result
def grab_totals():
    result = grab_all_times()
    final_dict = {}
    for entry in result:
        #print entry
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
        #print key + " total: " + str(final_dict[key])
        values.append(final_dict[key])
    for elt in sorted(values):
        print elt
        results_x.append("day: " + elt[0] + " hr: " + elt[1])
        results_y.append(elt[2])
        print len(values)
    return (results_x,results_y)

rx,ry =grab_totals()
rx = range(len(rx))
print "rx: " + str(rx)
print "ry: " + str(ry)

fig = plt.figure()
plt.xlabel("Hours Since 4pm EST April 26th")
plt.ylabel("Number of French Tweets")
plt.title("French Tweet Frequencies")
ax = fig.add_subplot(111)
ax.plot(rx,ry,'o-')
plt.show()
