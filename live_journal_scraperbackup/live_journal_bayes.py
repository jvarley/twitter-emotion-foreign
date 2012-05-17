import nltk
import codecs


#Jake Varley
from nltk.classify import NaiveBayesClassifier 
import re

def fetchBasicFeatureSet():
    f = open('output4/final_output_fr')
    text_list = []
    text_str = ""
    emotion = ""
    emotion_set = []
    count = 0
    for line in f.readlines():

        if line.find("#!#Emotion#!#") != -1:   
            emotion = line[13:-8].split()[0]
            text_list = []

        elif line.find("###BLOG_URL####") != -1:
             if count  > 0:
                text_str = "".join(text_list)
                """
                print url
                print emotion
                print text_str[0:100]
                print "\n\n"
                """
                emotion_set.append(({},url,text_str,emotion))
                
             #print "url: " + line[15:-6]
             url = line[15:-6]
             count += 1

        else:
            text_list.append(line)
    
    print "blog count: " + str(count)
    return emotion_set

def buildFeatureSet(simple_fs,text):
    """
    for word in text.split():
        
        if simple_fs.has_key(word):
            simple_fs[word] = simple_fs[word] + 1
        else:
            simple_fs[word] = 0

        if text.find("!") != -1:
            simple_fs["has !"] = True
        if text.find("?") != -1:
            simple_fs["has ?"] = True
    """
    simple_fs = get_freq_letters(text.split())

def get_freq_letters(words):
    fdist = nltk.FreqDist([char.lower() for word in words for char in word if char.isalpha()])
    freq_letters = {}
    for key,value in fdist.iteritems():
        freq_letters[key] = value
        #print "key: " + str(key) + " value: " + str(value) 
    return freq_letters
    
def get_freq_words(text):
    freq_words = {}
    fdist = nltk.FreqDist([word for word in text])
    for key,value in fdist.iteritems():
        if freq_words.has_key(key):
            freq_words[key] += value
        else:
            freq_words[key] = value
    return freq_words

def get_100_most_popular_words(list_of_pages):
    emotion_dict = {}
    ### collect all emotions
    for page in list_of_pages:
        if not emotion_dict.has_key(page[3]):
            emotion_dict[page[3]] = page[2]
        else:
            emotion_dict[page[3]] += page[2]

    top100_dict = {}
    for key in emotion_dict.keys():
        freq = nltk.FreqDist([word for word in emotion_dict[key].split()])
        top100 = freq.items()
        top100_dict[key] = top100
        print "top 10 for: " + key
        print len(top100)
        print top100[-40:-30]
        


if __name__ == "__main__":

    print "obtaining simple feature set"
    list_of_pages = fetchBasicFeatureSet()
    training_data = []
    print "building feature sets"
    #get_100_most_popular_words(list_of_pages)
    
    for page in list_of_pages:
        text = page[2]
        emotion = page[3]
        fs = get_freq_words(text.split())
        url = page[1]

        #buildFeatureSet(fs,text)
        training_data.append((fs,emotion))
    print "training classifier"
    classifier = NaiveBayesClassifier.train(training_data)
    print classifier.show_most_informative_features(n=20)
    print "Labels:"
    print classifier.labels()

    string = "hello world I am so happy today"
    print classifier.prob_classify(get_freq_letters(string.split()))

    
    
