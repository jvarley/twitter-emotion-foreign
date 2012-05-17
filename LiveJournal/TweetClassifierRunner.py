import threading
import multiThreadClassifier as mtc
import psycopg2
from Queue import Queue
import time

class TweetPuller(threading.Thread):
    def __init__(self,queue):
        self.queue = queue
        threading.Thread.__init__(self)

    def run(self):
        con = psycopg2.connect("dbname='nlptweets' host='localhost' user='jvarley' password='password'")
        cur = con.cursor()
        cur.execute("SELECT text,id FROM tweets;")
        counter = 0
        while True:
            tweet = cur.fetchone()
            if tweet == None or tweet == [] or len(tweet) < 2:
                break
            while self.queue.qsize() > 500:
                time.sleep(1)
            #print str(tweet) + "\n"
            self.queue.put(tweet)
            counter += 1
            if counter %1000 ==0:
                print counter

#this builds a dictionary from the database.
#keys: category+feature values: count
#this is much faster
def build_dict():
    classifier_dict ={}
    con = psycopg2.connect("dbname='nlptweets' host='localhost' user='jvarley' password='password'")
    cur = con.cursor()
    cur.execute("SELECT * FROM bayes_classifier;")
    counter = 0
    while True:
        item = cur.fetchone()
        if item == None or len(item) < 2:
            break
        feature = item[0]
        category = item[1]
        count = item[2]
        classifier_dict[category+feature] = count
        counter +=1
        if counter %1000 == 0:
            print counter
            print item
    return classifier_dict
#this runs the tweet classifier
if __name__ == "__main__":
    
    #this queue takes all the tweets out and puts them
    #in a queue so different threads can grab them
    q = Queue()
    pull = TweetPuller(q)
    pull.start()
    
    #this dictionary holds:
    #key: category+feature value: count 
    classifier_dict = build_dict()
    
    #a list of threads
    threads = []
    num_threads = 10

    #initialize the threads
    for i in range(num_threads):
        threads.append(mtc.MultiThreadClassifier(classifier_dict,q))
        
    #start the threads running
    for thread in threads:
        thread.start()

    

