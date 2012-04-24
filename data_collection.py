#this file runs to collect data and store in a file
import tweetstream
import guess_language
def collect(fileName):
    f = open(fileName,'a')
    stream = tweetstream.SampleStream("varley_jake", "mypassword")
    for tweet in stream:
        text = tweet.get('text')
        date = tweet.get('created_at')
        geo = tweet.get('geo')
        
        if (text != None):
            lang = guess_language.guessLanguage(text)
            if (lang == 'fr'):
                print  text.encode('utf8') + "\n\n"
                print date
                f.write("\n\n" + str(tweet).encode('utf8'))
        #print "new tweet: \n\n"+str(tweet) + "\n\n"

if __name__ == "__main__":
#    collect("samples")
    print "run collection with \n>>> collect filename.txt"
    
