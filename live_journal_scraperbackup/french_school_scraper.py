from bs4 import BeautifulSoup
from Queue import Queue
import re
import bs4.element as element
import urllib2
import threading
import codecs
import guess_language
from sets import Set
import time
from threading import Lock

#this class finds the blogs
class BlogFinder(threading.Thread):
    def __init__(self,blog_url_queue,runtype,entry_queue):
        self.exit_queue = blog_url_queue
        self.blog_url_dict = {}
        self.runtype = runtype
        self.entry_queue = entry_queue
        threading.Thread.__init__(self)
    

    def run(self):
        if self.runtype == 1:
            self.run_schools()
        else:
            self.run_word_list()


    def run_word_list(self):
        while(True):
            word = self.entry_queue.get()
            url = 'http://www.livejournal.com/interests.bml?int='+word
            user_names = self.scrape_page_for_usernames(url)
            print ("obtained " +str(len(user_names)) +
                   " usernames from: " + str(word) + "page")
            blog_pages = []
            for name in user_names:
                print name
                blog_pages = self.get_blog_pages_for_user(name)
                #gets rid of duplicates
                for blog_url in blog_pages:
                    if not self.blog_url_dict.has_key(blog_url):
                        self.blog_url_dict[blog_url] = True
                        self.exit_queue.put(blog_url)

    def run_schools(self):
        school_url = self.entry_queue.get()
        user_names = self.scrape_page_for_usernames(school_url)
        for name in user_names: 
            print name
            blog_pages = self.get_blog_pages_for_user(name)
            #gets rid of duplicates
            for blog_url in blog_pages:
                if not self.blog_url_dict.has_key(blog_url):
                    self.blog_url_dict[blog_url] = True
                    self.exit_queue.put(blog_url)

        
    #grabs list of words to search livejournal 
    #for to get lots of 
    #emo french users
    def get_emotion_list(self):
        f = open('emotion_list.txt','r+')
        text = f.read()
        word_list = text.split()
        return word_list

       #looks at a topic page, and returns a list of usernames
    def scrape_page_for_usernames(self,url):
        try:
            page_text = urllib2.urlopen(url).read()
            users = re.findall(r'\buser=\w+',page_text)
            users = [user[5:] for user in users]
            #list of all the users whose names appear
            #on the input topic page
            return users
        except:
            print "unable to scrape url: " + unicode(url).encode("utf-8")
            return []
    
    def get_blog_pages_for_user(self,user_name):
        try:
            still_good = True
            blog_urls = []
            skip = "/?skip="
            count = 0
            while (still_good):
                url = 'http://' + user_name + '.livejournal.com' + skip + str(count)
                count += 20
                page_text = urllib2.urlopen(url).read()
                new_blog_urls = re.findall('('+user_name+'.livejournal.com/[0-9]*.html)',page_text)
                if new_blog_urls == [] or count == 400:
                    still_good = False
                blog_urls += new_blog_urls
            return blog_urls
        except:
            print "unable to open page: " + str(url)
            return []

#this class takes individual blog pages urls from the queue, and 
#if they have emotion, then it writes the blog, url and mood to a file
#input: http://username.livejournal.com/5345234
#output: blog,url,mood to file
class BlogPageScraper(threading.Thread):
    def __init__(self,blog_page_url_queue,filename,lock):
        self.entry_queue = blog_page_url_queue
        self.filename = filename
        self.lock = lock
        threading.Thread.__init__(self)
    
    def run(self):
        while True:
            blog_url = self.entry_queue.get()
            try:
                print "BlogPageScraper working on: " + str(blog_url)

                blog = urllib2.urlopen('http://'+blog_url).read()
                soup = BeautifulSoup(blog)
                text_list = soup.findAll(text=True)
                end =0
                start = 0
                for i in range(len(text_list)):
                    if text_list[i].find("Create an Account") != -1:
                        start = i
                    if text_list[i].find("Leave a comment") != -1:
                        end = i
                        break
                text = ''.join([text for text in text_list[start+1:end]])
                lang = guess_language.guessLanguage(text)
                print "language: " + str(lang)

                emotion = None
                for row in soup():
                    found_mood,emotion = self.recursive_mood_find(row,False,emotion)
                    if emotion != None:
                        print " I have found the emotion: "+ unicode(emotion).encode('utf8') + "\n For the page: " + unicode(blog_url).encode('utf8')
                        break

                if emotion != None and emotion != " " and emotion != "":
                    self.lock.acquire()
                    try:
                        fname = self.filename +"_"+ lang
                        f = codecs.open(fname,'a+',"utf-8")
                        f2 = codecs.open(fname + "_emotions.txt",'a+',"utf-8")
                        #print unicode(text).encode("utf8")
                        f.write("\n\n")
                        f.write("###BLOG_URL####" + blog_url.decode("utf8") + "#####")
                        f.write("\n")
                        f.write("#!#Emotion#!#"+emotion.decode("utf8")+ "#!#!#!#")
                        f.write("\n")
                        f.write(text)
                        f.close()

                        f2.write("\n\n")
                        f2.write(blog_url.decode("utf8"))
                        f2.write("\n")
                        f2.write(emotion.decode("utf8"))
                        f2.close()

                    except:
                        print  "failed to write from: "+ unicode(blog_url).encode("utf-8")
                    finally:
                        self.lock.release()
            except:
                "got an error scraping page:" + unicode(blog_url).encode("utf-8")


    def get_children(self,soup):
        try:
            return soup.children
        except:
            return None

    def recursive_mood_find(self,child,found_mood,emotion):
        if emotion != None:
          return found_mood,emotion  
        elif type(child) == element.NavigableString:
            if (found_mood and child != " "):
                found_mood = False
                return found_mood,child
            if (child.find("Current Mood:") != -1 or
                child.find("mood:") != -1 or 
                child.find("Humeur") !=-1 or
                child.find("Mood:") != -1):
                found_mood = True
        else:
            children = self.get_children(child)
            if children != None:
                for c in children:
                    found_mood,emotion = self.recursive_mood_find(c,found_mood,emotion)

        return found_mood,emotion
            

class ProgressWatcher(threading.Thread):
    def __init__(self,finders,scrapers):
        self.finders= finders
        self.scrapers = scrapers
        threading.Thread.__init__(self)
    def run(self):
        while(True):
            time.sleep(1)
            running = False
            for thread in self.finders:
                if thread.is_alive():
                    running = True
            if running == False:
                for thread in self.scrapers:
                    thread._Thread__stop()

class FrenchSchoolURLBuilder(threading.Thread):
    def __init__(self,output_queue):
        self.output_queue = output_queue
        threading.Thread.__init__(self)
        
    def run(self):
        self.fill_school_queue()
        

    def fill_school_queue(self):
        url = "http://www.livejournal.com/schools/?ctc=FR"
        text = urllib2.urlopen(url).read()
        region_ids = re.findall(r'\b&sc=\w.*\'>',text)
        region_ids = [region_id[4:-2] for region_id in region_ids]
        #print region_ids

        for region in region_ids:
            print region
            url = "http://www.livejournal.com/schools/?ctc=FR&sc=" + region
            text = urllib2.urlopen(url).read()
            cities = re.findall(r'\b&cc=\w.+\'>',text)
            cities = [city[4:-2] for city in cities]

            for city in cities:
                url = "http://www.livejournal.com/schools/?ctc=FR&sc=" + region + "&cc=" + city
                text = urllib2.urlopen(url).read()
                school_ids = re.findall(r'\b&sid=\w+',text)
                #print url
                #print school_ids
                school_ids = [school_id[5:] for school_id in school_ids]
                for school_id in school_ids:
                    school_url = url + "&sid=" + school_id
                    self.output_queue.put(school_url)


def fill_words_queue(words_queue):
    f = open('emotion_list.txt','r+')
    text = f.read()
    word_list = text.split()
    for word in word_list:
        print word
        words_queue.put(word)

if __name__ == "__main__":
    #this queue holds blog_urls
    blog_url_queue = Queue()
    words_queue = Queue()
    school_queue = Queue()


    school_thread = FrenchSchoolURLBuilder(school_queue)
    print "filling school queue"
    school_thread.start()
 
    
    print "filling words queue"
    fill_words_queue(words_queue)
    
    print "initializing BlogFinder Threads"
    # fills the queue with urls that have individual blogs
    #1 is finding from paris schools
    #2 is finding from word_list
    bf_thread1 = BlogFinder(blog_url_queue,1,school_queue)
    bf_thread2 = BlogFinder(blog_url_queue,1,school_queue)
    bf_thread3 = BlogFinder(blog_url_queue,2,words_queue)
    bf_thread4 = BlogFinder(blog_url_queue,2,words_queue)
    bf_thread5 = BlogFinder(blog_url_queue,2,words_queue)

    Finder_Threads = [bf_thread1,bf_thread2,bf_thread3,bf_thread4,bf_thread5]

    print "initializing Scraper Threads"
    #takes individual blog page urls, and grabs mood/url/text and
    #writes to file
    lock = Lock()
    bps_thread1 = BlogPageScraper(blog_url_queue,'output5/final_output',lock)
    bps_thread2 = BlogPageScraper(blog_url_queue,'output5/final_output',lock)
    bps_thread3 = BlogPageScraper(blog_url_queue,'output5/final_output',lock)
    bps_thread4 = BlogPageScraper(blog_url_queue,'output5/final_output',lock)
    Scraper_Threads = [bps_thread1,bps_thread2,bps_thread3,bps_thread4]

    #watches progress in order to shut down bps_thread when done
    progress_watcher = ProgressWatcher(Finder_Threads,Scraper_Threads)

    #start the threads
    for thread in Finder_Threads:
        thread.start()
    print "started Finders"
    for thread in Scraper_Threads:
        thread.start()
    print "started scrapers"

    progress_watcher.start()
    
    """
    raw_input("press any key to kill")
    school_thread.shutdown()
    for thread in Finder_Threads:
        thread.shutdown()
    for thread in Scraper_Threads:
        thread.shutdown()

    progress_watcher.shutdown()

    """
    
    
   
