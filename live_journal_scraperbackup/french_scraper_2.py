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

#this class finds the blogs
class BlogFinder(threading.Thread):
    def __init__(self,blog_url_queue):
        self.exit_queue = blog_url_queue
        self.blog_url_dict = {}
        threading.Thread.__init__(self)
    

    def run(self):
        self.run_schools()
        """
        word_list = self.get_emotion_list()
        print "word_list: "+ str(word_list)
        user_names = []
        for word in word_list:
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
        """
    def run_schools(self):
        url = "http://www.livejournal.com/schools/?ctc=FR&sc=Paris&cc=Paris"
        text = urllib2.urlopen(url).read()
        school_ids = re.findall(r'\b&sid=\w+',text)
        school_ids = [school_id[5:] for school_id in school_ids]
        for school_id in school_ids:
            url = "http://www.livejournal.com/schools/?ctc=FR&sc=Paris&cc=Paris&sid=" + school_id
            user_names = self.scrape_page_for_usernames(url)
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
        page_text = urllib2.urlopen(url).read()
        users = re.findall(r'\buser=\w+',page_text)
        users = [user[5:] for user in users]
        #list of all the users whose names appear
        #on the input topic page
        return users
    
    def get_blog_pages_for_user(self,user_name):
        try:
            url = 'http://' + user_name + '.livejournal.com'
            page_text = urllib2.urlopen(url).read()
            blog_urls = re.findall('('+user_name+'.livejournal.com/[0-9]*.html)',page_text)
            return blog_urls
        except:
            print "unable to open page: " + str(url)
            return []

#this class takes individual blog pages urls from the queue, and 
#if they have emotion, then it writes the blog, url and mood to a file
#input: http://username.livejournal.com/5345234
#output: blog,url,mood to file
class BlogPageScraper(threading.Thread):
    def __init__(self,blog_page_url_queue,filename):
        self.entry_queue = blog_page_url_queue
        self.filename = filename
        threading.Thread.__init__(self)
    
    def run(self):
        while True:
            blog_url = self.entry_queue.get()
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
                
            emotion = None
            for row in soup():
                found_mood,emotion = self.recursive_mood_find(row,False,emotion)
                if emotion != None:
                    print " I have found the emotion: "+ unicode(emotion).encode('utf8') + "\n For the page: " + unicode(blog_url).encode('utf8')
                    break

            if emotion != None and emotion != " " and emotion != "" and lang == 'fr':
                f = codecs.open(self.filename,'a+',"utf-8")
                f2 = codecs.open(self.filename[:-4] + "emotions.txt",'a+',"utf-8")
                try:
                    #print unicode(text).encode("utf8")
                    f.write("\n\n")
                    f.write(blog_url.decode("utf8"))
                    f.write("\n")
                    f.write(emotion.decode("utf8"))
                    f.write("\n")
                    f.write(text)
                    f.close()

                    f2.write("\n\n")
                    f2.write(blog_url.decode("utf8"))
                    f2.write("\n")
                    f2.write(emotion.decode("utf8"))
                    f2.close()

                except:
                    f.close()
                    print  "failed to write from: "+ unicode(blog_url).encode("utf-8")

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
    def __init__(self,thread1,thread2):
        self.thread1 = thread1
        self.thread2 = thread2
        threading.Thread.__init__(self)
    def run(self):
        while (self.thread1.is_alive()):
            time.sleep(1)
        self.thread2._Thread__stop()




if __name__ == "__main__":

    q = Queue()

    # fills the queue with urls that have individual blogs
    bf_thread = BlogFinder(q)

    #takes individual blog page urls, and grabs mood/url/text and
    #writes to file
    bps_thread = BlogPageScraper(q,'final_output4.txt')

    #watches progress in order to shut down bps_thread when done
    progress_watcher = ProgressWatcher(bf_thread,bps_thread)

    #start the threads
    bf_thread.start()
    bps_thread.start()
    progress_watcher.start()
    
   
