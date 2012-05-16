import nltk
import codecs
import docclass as nbc
#from set import Set

#Jake Varley
from nltk.classify import NaiveBayesClassifier 
#from nltk.corpus import stopwords
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
    
    #print "blog count: " + str(count)
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
        


def run():
    #stop_words = stopwords.words("french")
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
    return classifier
    

def run3():
    classifier = nbc.naivebayes(nbc.getwords)
    list_of_pages = fetchBasicFeatureSet()
    for page in list_of_pages:
        text =page[2]
        emotion= page[3]
        index = emotion.find("\'")
        if index != None:
            emotion = emotion[:index] + emotion[index+1:]
        classifier.train(text,emotion)
 

emotion_groups = {}   
emotion_groups["happy"] = {'happy':1,'cheerful':1,'bouncy':1,'good':1,'excited':1, 'jubilant':1,'ecstatic':1,'silly':1, 'sunny':1}
emotion_groups["calm"] = { 'calm' :1,'content':1, 'okay':1, 'satisfied':1, 'peaceful':1,'relaxed':1}
emotion_groups["contemplative"] = {"contemplative":1, "pensive":1}
emotion_groups["drunk"] = {"drunk":1,'just a little drunk':1}
emotion_groups["sad"] = {'sad':1, 'disappointed':1, 'crappy':1, 'depressed':1, 'crushed':1, 'drained':1,  'blah':1,'gloomy':1, 'discontent':1, 'home sick':1, 'melancholy':1}
emotion_groups["annoyed"] = {'annoyed':1,'irritated':1,'uncomfortable':1,'stressed':1,'frustrated':1,'cranky':1}
emotion_groups["angry"] = {'angry':1, 'pissed off':1, 'irate':1,'infuriated':1}
emotion_groups["tired"] = {'tired':1,'exhausted':1,'sleepy':1,' drained':1}
emotion_groups["bored"] = {'bored':1,'listless':1,'lazy':1,'indifferent':1,'lethargic':1}
emotion_groups["anxious"]  ={'anxious':1,'scared':1,'nervous':1,'worried':1}
emotion_groups["busy"] = {'busy':1,'working':1,'productive':1}
emotion_groups["grateful"] = {'grateful':1, 'touched':1, 'thankful':1}
emotion_groups["cold"] = {'cold':1, 'Il fait froid...!!!':1}
emotion_groups["sick"] = {'sick':1,'in pain':1}
emotion_groups["remove"] = {'souffrante..':1,'rushed':1, 'glouton':1,'embarrassed':1,'devious':1,'broke':1,'blank':1,'artistic':1,'Calme':1,'traumatized':1,'tanning':1,'so damn lucky':1,'sereine':1,'riche':1,'pleased':1,'older':1,'nerdy':1,'giggly':1, 'flirty':1,'everything':1,'envious':1,'distressed':1,'determined':1, 'chipper':1,'careless':1,'bitchy':1, 'better':1,'Oups':1,'Miam miam':1,'Miam':1,"J'adore":1,'Hum hum':1,'Cheburashka':1,'Berk berk':1,'.':1,"-Sens de l'humour 5/10":1}

def processed_fs(fs):
    emotion_list = []
    for page in fs:
        text = page[2]
        emotion = page[3]
        index = emotion.find("\'")
        if index != -1:
            emotion = emotion[:index] + emotion[index+1:]
        grouped_emotion = emotion
        print "original: " + str(emotion)
        for emotion_group in emotion_groups.keys():
            if emotion_groups[emotion_group].has_key(emotion):
                grouped_emotion = emotion_group
        print "updated: " + grouped_emotion
        print "get rid of removed!!!"
        if grouped_emotion != 'remove':
            emotion_list.append([text, emotion, grouped_emotion])
    return emotion_list
        
if __name__ == "__main__":
    #run3()
    fs = fetchBasicFeatureSet()
    processed_fs = processed_fs(fs)
    classifier = nbc.naivebayes(nbc.getwords)
    classifier.setdb()
    for item in processed_fs:
        text = item[0]
        emotion = item[1]
        grouped_emotion = item[2]
        classifier.train(text, grouped_emotion)

    #print classifier.classify("L'amour s'en va comme cette eau courante L'amour s'en va")
   
