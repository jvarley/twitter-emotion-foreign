import docclass as nbc 
import re
import threading
import psycopg2


class MultiThreadClassifier(threading.Thread):
    def __init__(self,classifier_dict,feed_queue):
        self.con = psycopg2.connect("dbname='nlptweets' host='localhost' user='jvarley' password='password'")
        self.cur = self.con.cursor()
        self.classifier = nbc.naivebayes(nbc.getwords,classifier_dict)
        self.feed_queue = feed_queue
        threading.Thread.__init__(self)
        
    def run(self):
        while True :
            #try:
               
            tweet = self.feed_queue.get()

            if tweet == None or len(tweet) < 2:
                break
            text = tweet[0]
            tweet_id = tweet[1]

            classification = self.classifier.classify(text)
            #print "now working on: " + str(tweet_id) + " \nclassification: " + str(classification) + "\n text: " + str(text) + "\n\n"
            self.write_output(tweet_id,classification)

            #except:
                #print "failed!!!"
 
    def write_output(self,row_id,classification):
        self.cur.execute("UPDATE tweets SET emotion = '%s' WHERE id= '%s';" %(classification,row_id))
        self.con.commit()


