#Jake Varley
#takes a list of french words, searches for users 
#on live journal using those words.
#Goes into those users pages and scrapes the blog entries of posts 
#with emotion tags.

import urllib2
import re
import guess_language
from bs4 import BeautifulSoup
import bs4.element as element
MOOD = True
emotion_indicators= {"Current Mood":True,"Current mood": True,"mood:":True,"Humeor": True}

#grabs list of words to search livejournal for to get lots of 
#emo french users
def get_emotion_list():
    f = open('emotion_list.txt','r+')
    text = f.read()
    word_list = text.split()
    return word_list


#looks at a topic page, and returns a list of usernames
def scrape_emotion_page(key_word= 'aimer'):
    url = 'http://www.livejournal.com/interests.bml?int='+key_word
    page_text = urllib2.urlopen(url).read()
    users = re.findall(r'\buser=\w+',page_text)
    users = [user[5:] for user in users]
    #list of all the users whose names appear on the input topic page
    return users

def get_blog_pages_for_user(user_name):
    try:
        url = 'http://' + user_name + '.livejournal.com'
        page_text = urllib2.urlopen(url).read()
        blog_urls = re.findall('('+user_name+'.livejournal.com/[0-9]*.html)',page_text)
        for blog_url in blog_urls:
            print blog_url
    except:
        print "didnt work"

def scrape_user_page(user_name='manon-66'):
    print "user_name: " + str(user_name)
    if True:
    #try:
        url = 'http://' + user_name + '.livejournal.com'
        page_text = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page_text)
        #print soup
        take_1 = scrape_user_page_I(soup,user_name)
        take_2 = scrape_user_page_II(soup,user_name)
        #for elt in take_2:
            #print elt[0]
            #print "\n"
            #print elt[1]
            #print "\n\n\n"
        emotion_blogs = take_1 + take_2
        print len(emotion_blogs)
        return emotion_blogs
    #except:
        print "unable to find user page for: "  + str(user_name)
        return []


def scrape_user_page_I(soup,user_name):
    emotion_blogs = []
    for row in soup('div', attrs={'class' : 'entryHolder'}):
        #print str(row) + "\n\n"
        blog_text = None
        blog_emotion = None
        for entry in row('div', attrs={'class':"entryText"}):
            #print str(entry) + "\n\n"
            blog_text_list= entry.findAll(text=True)
            blog_text = ''.join([text for text in blog_text_list])
        for entry in row('div' , attrs = {'class':"entryMetadata"}):
            text_list = entry.findAll(text=True)
            for i in range(len(text_list)-1):
                if text_list[i] == "Humeur:" or text_list[i] == "Current Mood:":
                    blog_emotion = text_list[i+1]
        if blog_emotion != None and blog_text != None:
            print "user_name: " + unicode(user_name).encode('utf8')
            print "emotion found using user_page_scraper_I: " + unicode(blog_emotion).encode('utf8')
            print "text: "
            print unicode(blog_text).encode('utf8') + "\n\n"
            emotion_blogs.append((blog_emotion,blog_text))
    return emotion_blogs

def scrape_user_page_II(soup,user_name):
    emotion_blogs = []
    for row in soup('td'):
        for entry in row('div'):
            has_mood = False
            for img in entry('img'):
                if img['src'].find("mood") != -1:
                    has_mood = True
                    blog_emotion = row.nextSibling
                    print type(row)
                    print row.nextSibling
                    print blog_emotion
                    break
            if has_mood:
                blog_text_list = row.findAll(text=True)
                blog_emotion = find_emotion(blog_text_list)
                #blog_emotion = blog_text_list[-1]
                blog_text = ''.join([text for text in blog_text_list[:-2]])
                print "user_name: " + unicode(user_name).encode('utf8')
                print "emotion found using user_page_scraper_II: " + unicode(blog_emotion).encode('utf8')
                print "text:"
                print unicode(blog_text).encode('utf8') + "\n\n\n"
                emotion_blogs.append((blog_emotion,blog_text))
    return emotion_blogs




def find_emotion(blog_text_list):
    emotion = None
    for i in range(len(blog_text_list)):
        n = len(blog_text_list)-i-1
        print "next text: " + str(blog_text_list[n])
    if emotion_indicators[blog_text_list] != None:
        emotion = blog_text_list[n+1]
    if emotion == None:
        emotion = blog_text_list[-1]
    if len(emotion) < 2:
        emotion = None
    return emotion
            

def run():
    word_list = get_emotion_list()
    print "obtained word_list"
    usernames = []
    print "word_list: " + str(word_list[:10])
    for word in word_list:
        usernames += scrape_emotion_page(word)
    print ("obtained " +str(len(usernames)) +
    " usernames from: " + str(word) + "page")
    emotion_blogs = []
    for name in usernames:
        blog_pages = get_blog_pages_for_user(name)
        #users_emotion_blogs = scrape_user_page(name)
        #if users_emotion_blogs != []:
            #emotion_blogs.append(users_emotion_blogs)
    """
    print "total number of emotion blogs found: " + str(len(emotion_blogs))
    #print emotion_blogs[:10]
    french_blogs = []
    for blog in emotion_blogs:
        print "blog: " + str(blog)
        emotion = blog[0]
        text = blog[1]
        lang = guess_language.guessLanguage(text)
        if (lang =='fr'):
            french_blogs.append(blog)
    print "number of french blogs: " + str(len(french_blogs))
    print french_blogs[:10]
    """
def make_soup_from_string(s):
    return BeautifulSoup(s)
    
def get_soup(user_name = 'cremlian'):
     url = 'http://' + user_name + '.livejournal.com'
     page_text = urllib2.urlopen(url).read()
     soup = BeautifulSoup(page_text)
     return soup
'''
     print type(soup)
     for row in soup():
         #print type(row)
         if (type(row) == element.NavigableString or
             type(row) == element.Tag):
             for entry in row.children:#():
                 found_mood = False
                 #print type(entry)
                 if (type(entry) == element.NavigableString
                     or type(entry) == element.Tag):
                     for child in entry.children:
                         #print child
                         #print type(child)
                         if type(child) ==element.NavigableString:
                             #print "I have found a string!"
                             if child.find("Current Mood") != -1:
                                 print child
                                 print "I have found Mood"
                                 found_mood = True
                             if found_mood:
                                 print child
'''

def get_children(soup):
    try:
        return soup.children
    except:
        return None



def recursive_scrape(child,found_mood):
    if type(child) == element.NavigableString:
        found_mood,
        if (found_mood and child != " "):
            #print ("the mood is : " +
            #unicode(child).encode('utf8'))
            found_mood = False
        if (child.find("Current Mood:") != -1 or
            child.find("mood") != -1 or 
            child.find("Humeur") !=-1):
            found_mood = True
    elif(type(child) == element.Tag and child.name == 'div' and child.attrs.has_key('class') and child.attrs['class'] == "entryHeader"):
        for c in get_children(child):
            mood = recursive_mood_find(c,False)
            print "mood: " + str(mood)
            if mood != False:
                print c.findAll(text=True)
                print "\n\n"
    else:
        children = get_children(child)
        if children != None:
            for c in children:
                found_mood = recursive_scrape(c,found_mood)

    return found_mood



def recursive_mood_find(child,found_mood):
    if type(child) == element.NavigableString:
        if (found_mood and child != " "):
            print ("the mood is : " +
            unicode(child).encode('utf8'))
            found_mood = False
            #f = open("mood.txt","a")
            #f.write(unicode(child).encode('utf8')+"\n")
            #f.close()
        if (child.find("Current Mood:") != -1 or
            child.find("mood") != -1 or 
            child.find("Humeur") !=-1):
            found_mood = True
    else:
        children = get_children(child)
        if children != None:
            for c in children:
                found_mood = recursive_mood_find(c,found_mood)

    return found_mood

if __name__ == "__main__":
    print "hi"
    run()
    #look at:
    #www.livejournal.com/schools/
    #scrape_user_page('improviste')
    #scrape_user_page('cremlian')
    tags= ['td','tr','b','div']
    #soup = get_soup('improviste')
    #print soup
    #for row in soup():
        #mood = recursive_mood_find(row,False)
        #mood = recursive_scrape(row,False)
        #break

# to do
#1) go to individual post page, grab first emotion, grab all the text.

class FrenchScraper():
    def __init__(self):
        self.blog_url_dict = {}
        #list of dictionaries, each blog with an emotion 
        #is a dict 
        self.emo_blogs = []
        self.run()
        """
        soup = self.get_soup('http://shysexkitten.livejournal.com/')
        for row in soup():
            found_mood,mood = self.recursive_mood_find(row,False,None)
            #print found_mood
            #print mood
            if mood !=None: 
                print mood
                break
        """

    def run(self):
        word_list = self.get_emotion_list()
        print "word_list: "+ str(word_list)
        user_names = []
        for word in word_list:
            user_names += self.scrape_emotion_page(word)
            print ("obtained " +str(len(user_names)) +
                   " usernames from: " + str(word) + "page")
        blog_pages = []
        for name in user_names:
            print name
            blog_pages += self.get_blog_pages_for_user(name)
            print blog_pages[-10:-1]
        #gets rid of duplicates
        for blog in blog_pages:
            self.blog_url_dict[blog] = True
        for blog_url in self.blog_url_dict.keys():
            blog = urllib2.urlopen('http://'+blog_url).read()
            soup = BeautifulSoup(blog)
            emotion = None
            for row in soup():
                found_mood,emotion = self.recursive_mood_find(row,False,emotion)
                if emotion != None:
                    print " I have found the emotion: "+ unicode(emotion).encode('utf8') + "\n For the page: " + unicode(blog_url).encode('utf8')
                    break

            if emotion != None:
                emo_blog = {}
                emo_blog['url'] = blog_url
                emo_blog['mood'] = emotion
                emo_blog['text'] = blog
                self.emo_blogs.append(emo_blog)
            

    def get_soup(self,url):
        page_text = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page_text)
        return soup
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
                #print ("the mood is : " +
                #unicode(child).encode('utf8'))
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




    def get_blog_pages_for_user(self,user_name):
        try:
            url = 'http://' + user_name + '.livejournal.com'
            page_text = urllib2.urlopen(url).read()
            blog_urls = re.findall('('+user_name+'.livejournal.com/[0-9]*.html)',page_text)
            return blog_urls
        except:
            print "didnt work"
            return []

    #looks at a topic page, and returns a list of usernames
    def scrape_emotion_page(self,key_word= 'aimer'):
        url = 'http://www.livejournal.com/interests.bml?int='+key_word
        page_text = urllib2.urlopen(url).read()
        users = re.findall(r'\buser=\w+',page_text)
        users = [user[5:] for user in users]
        #list of all the users whose names appear
        #on the input topic page
        return users


    #grabs list of words to search livejournal 
    #for to get lots of 
    #emo french users
    def get_emotion_list(self):
        f = open('emotion_list.txt','r+')
        text = f.read()
        word_list = text.split()
        return word_list


class FrenchScraper():
    def __init__(self):
        self.blog_url_dict = {}
        #list of dictionaries, each blog with an emotion 
        #is a dict 
        self.emo_blogs = []
        self.run()
        """
        soup = self.get_soup('http://shysexkitten.livejournal.com/')
        for row in soup():
            found_mood,mood = self.recursive_mood_find(row,False,None)
            #print found_mood
            #print mood
            if mood !=None: 
                print mood
                break
        """

    def run(self):
        word_list = self.get_emotion_list()
        print "word_list: "+ str(word_list)
        user_names = []
        for word in word_list:
            user_names += self.scrape_emotion_page(word)
            print ("obtained " +str(len(user_names)) +
                   " usernames from: " + str(word) + "page")
        blog_pages = []
        for name in user_names:
            print name
            blog_pages += self.get_blog_pages_for_user(name)
            print blog_pages[-10:-1]
        #gets rid of duplicates
        for blog in blog_pages:
            self.blog_url_dict[blog] = True
        for blog_url in self.blog_url_dict.keys():
            blog = urllib2.urlopen('http://'+blog_url).read()
            soup = BeautifulSoup(blog)
            emotion = None
            for row in soup():
                found_mood,emotion = self.recursive_mood_find(row,False,emotion)
                if emotion != None:
                    print " I have found the emotion: "+ unicode(emotion).encode('utf8') + "\n For the page: " + unicode(blog_url).encode('utf8')
                    break

            if emotion != None:
                emo_blog = {}
                emo_blog['url'] = blog_url
                emo_blog['mood'] = emotion
                emo_blog['text'] = blog
                self.emo_blogs.append(emo_blog)
            

    def get_soup(self,url):
        page_text = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page_text)
        return soup
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
                #print ("the mood is : " +
                #unicode(child).encode('utf8'))
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




    def get_blog_pages_for_user(self,user_name):
        try:
            url = 'http://' + user_name + '.livejournal.com'
            page_text = urllib2.urlopen(url).read()
            blog_urls = re.findall('('+user_name+'.livejournal.com/[0-9]*.html)',page_text)
            return blog_urls
        except:
            print "didnt work"
            return []

    #looks at a topic page, and returns a list of usernames
    def scrape_emotion_page(self,key_word= 'aimer'):
        url = 'http://www.livejournal.com/interests.bml?int='+key_word
        page_text = urllib2.urlopen(url).read()
        users = re.findall(r'\buser=\w+',page_text)
        users = [user[5:] for user in users]
        #list of all the users whose names appear
        #on the input topic page
        return users


    #grabs list of words to search livejournal 
    #for to get lots of 
    #emo french users
    def get_emotion_list(self):
        f = open('emotion_list.txt','r+')
        text = f.read()
        word_list = text.split()
        return word_list

class FrenchScraper():
    def __init__(self):
        self.blog_url_dict = {}
        self.emo_blogs = []
        self.run()

    def run(self):
        word_list = self.get_emotion_list()
        print "word_list: "+ str(word_list)
        user_names = []
        for word in word_list:
            user_names += self.scrape_emotion_page(word)
            print ("obtained " +str(len(user_names)) +
                   " usernames from: " + str(word) + "page")
        blog_pages = []
        for name in user_names:
            print name
            blog_pages += self.get_blog_pages_for_user(name)
            print blog_pages[-10:-1]
        #gets rid of duplicates
        for blog in blog_pages:
            self.blog_url_dict[blog] = True
        for blog_url in self.blog_url_dict.keys():
            blog = urllib2.urlopen('http://'+blog_url).read()
            soup = BeautifulSoup(blog)
            emotion = None
            for row in soup():
                found_mood,emotion = self.recursive_mood_find(row,False,emotion)
                if emotion != None:
                    print " I have found the emotion: "+ unicode(emotion).encode('utf8') + "\n For the page: " + unicode(blog_url).encode('utf8')
                    break

            if emotion != None:
                emo_blog = {}
                emo_blog['url'] = blog_url
                emo_blog['mood'] = emotion
                emo_blog['text'] = blog
                self.emo_blogs.append(emo_blog)
            

    def get_soup(self,url):
        page_text = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page_text)
        return soup
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
                #print ("the mood is : " +
                #unicode(child).encode('utf8'))
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




    def get_blog_pages_for_user(self,user_name):
        try:
            url = 'http://' + user_name + '.livejournal.com'
            page_text = urllib2.urlopen(url).read()
            blog_urls = re.findall('('+user_name+'.livejournal.com/[0-9]*.html)',page_text)
            return blog_urls
        except:
            print "didnt work"
            return []

    #looks at a topic page, and returns a list of usernames
    def scrape_emotion_page(self,key_word= 'aimer'):
        url = 'http://www.livejournal.com/interests.bml?int='+key_word
        page_text = urllib2.urlopen(url).read()
        users = re.findall(r'\buser=\w+',page_text)
        users = [user[5:] for user in users]
        #list of all the users whose names appear
        #on the input topic page
        return users


    #grabs list of words to search livejournal 
    #for to get lots of 
    #emo french users
    def get_emotion_list(self):
        f = open('emotion_list.txt','r+')
        text = f.read()
        word_list = text.split()
        return word_list
