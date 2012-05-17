import urllib2
from bs4 import BeautifulSoup


def scrape_page(url ="http://b0st0n.livejournal.com/" ,
                mood_corpus = {}):
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    mood_corpus = {}
    texts = soup.findAll(text=True)
    for i in range(len(texts)):
        if texts[i] == '[' and texts[i+1] == 'mood':
            mood_text = ""
            mood = texts[i+4]
            print mood
            y = i+6
            while texts[y] != 'link':
                mood_text +=texts[y]
                y+=1
            print mood_text
            if mood_corpus.has_key(mood):
                mood_corpus[mood].append(mood_text)
            else:
                mood_corpus[mood] = [mood_text]
    return mood_corpus
    
scrape_page()
