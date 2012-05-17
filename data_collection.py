#this file runs to collect data and store in a file
import tweetstream
import guess_language
def collect(fileName):
    f = open(fileName,'a')
    stream = tweetstream.SampleStream("varley_jake", "mypassword")
    for tweet in stream:
        #print tweet.keys()
        text = tweet.get('text')
        date = tweet.get('created_at')
        geo = tweet.get('geo')
        language = tweet.get('lang')
        location = tweet.get('location')
        
        if (text != None):
            lang = guess_language.guessLanguage(text)
            if (lang == 'fr'):
                print  text.encode('utf8') + "\n\n"
                print "date: " + str(date)
                print "geo: " + str(geo)
                print "location: " + str(location)
                print "language: " + str(language)
                f.write("\n\n" + str(tweet).encode('utf8'))

if __name__ == "__main__":
    collect("samples2.txt")
    
