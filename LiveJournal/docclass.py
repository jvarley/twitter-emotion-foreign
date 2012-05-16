#from pysqlite2 import dbapi2 as sqlite
import psycopg2
import re
import math
import datetime

def getwords(doc):
  splitter=re.compile('\\W*')
  #print doc
  # Split the words by non-alpha characters
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
  # Return the unique set of words only
  return dict([(w,1) for w in words])

class classifier:
  def __init__(self,getfeatures,filename=None):
    # Counts of feature/category combinations
    self.fc={}
    # Counts of documents in each category
    self.cc={}
    self.getfeatures=getfeatures
    self.con = psycopg2.connect("dbname='nlptweets' host='localhost' user='jvarley' password='password'")
    self.cur = self.con.cursor()
    self.doc_count = 0
    self.Cache = {}
    self.Cache["cat_list"] = None
    self.Cache["total_count"] =None
    self.Cache["category_count"] = {}
    
  def setdb(self):
    self.cur.execute("CREATE TABLE bayes_classifier(feature VARCHAR(64), category VARCHAR(64), count int8);")
    self.cur.execute("CREATE TABLE bayes_category_counter(category VARCHAR(64), count int8);")
    self.con.commit()

  def incf(self,f,cat):
    count=self.fcount(f,cat)
    if count==0:
      self.cur.execute("INSERT INTO bayes_classifier(feature, category, count) VALUES ('%s','%s',1);" 
                       % (f,cat))
    else:
      self.cur.execute(
        "UPDATE bayes_classifier SET count=%d WHERE feature='%s' AND category='%s';" 
        % (count+1,f,cat)) 
  
  def fcount(self,f,cat):
    self.cur.execute("SELECT * FROM bayes_classifier WHERE feature='%s' AND category='%s';" %(f,cat))
    res = self.cur.fetchone()
    if res==None: return 0
    else: return float(res[2])

  def incc(self,cat):
    count=self.catcount(cat)
    if count==0:
      self.cur.execute("INSERT INTO bayes_category_counter(category,count) VALUES ('%s',1);" % (cat))
    else:
      self.cur.execute("UPDATE bayes_category_counter SET count=%d WHERE category='%s';" 
                       % (count+1,cat))    

  def catcount(self,cat):
    if not self.Cache["category_count"].has_key(cat):
      self.cur.execute("SELECT COUNT FROM bayes_category_counter WHERE category='%s';"
                         %(cat))
      res = self.cur.fetchone()
      if res != None:
        self.Cache["category_count"][cat] = float(res[0])
      else:
        self.Cache["category_count"][cat] = float(0)

    return self.Cache["category_count"][cat]

  def categories(self):
    if self.Cache["cat_list"] == None:
      self.cur.execute('SELECT category FROM bayes_category_counter;');
      res = self.cur.fetchmany(125)
      ret= [d[0] for d in res]
      self.Cache["cat_list"] = ret
    return self.Cache["cat_list"]

  def totalcount(self):
    if self.Cache["total_count"] == None:
      self.cur.execute('SELECT SUM(COUNT) FROM bayes_category_counter;');
      res = self.cur.fetchone()
      if res != None:
        self.Cache["total_count"] = res[0]
      else:
        self.Cache["total_count"] = 0
    return self.Cache["total_count"]


  def train(self,item,cat):
    self.doc_count +=1
    print "I am training on document: " + str(self.doc_count)
    features=self.getfeatures(item)
    # Increment the count for every feature with this category
    for f in features:
      self.incf(f,cat)

    # Increment the count for this category
    self.incc(cat)
    self.con.commit()

  def fprob(self,f,cat):
    if self.catcount(cat)==0: return 0

    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return self.fcount(f,cat)/self.catcount(cat)

  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    # Calculate current probability
    basicprob=prf(f,cat)

    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([self.fcount(f,c) for c in self.categories()])

    # Calculate the weighted average
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp




class naivebayes(classifier):
  
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)  
    #print "features: " + str(features)

    # Multiply the probabilities of all the features together
    p=1
    #for f in features: p*=self.weightedprob(f,cat,self.fprob)
    for f in features: 
      p*=self.weightedprob(f,cat,self.fprob)
      #print f
      
      
    print "probability that: " + str(item)+ " is in category: " + str(cat) + " is: " + str(p)
    return p

  def prob(self,item,cat):
    catprob=float(self.catcount(cat))#/float(self.totalcount()) # can remove this because it is all normalized 
    docprob=self.docprob(item,cat)
    return docprob*catprob
  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    if cat not in self.thresholds: return 1.0
    return self.thresholds[cat]
  
  def classify(self,item,default=None):
    probs={}
    # Find the category with the highest probability
    max=0.0
    starttime = datetime.datetime.now()
    for cat in self.categories():
      probs[cat]=self.prob(item,cat)
      if probs[cat]>max: 
        max=probs[cat]
        best=cat
    
    # Make sure the probability exceeds threshold*next best
    for cat in probs:
      if cat==best: continue
      if probs[cat]*self.getthreshold(best)>probs[best]: return default
    print "start: " + str(starttime) + " endtime: " + str(datetime.datetime.now())
    return best





class fisherclassifier(classifier):
  def cprob(self,f,cat):
    # The frequency of this feature in this category    
    clf=self.fprob(f,cat)
    if clf==0: return 0

    # The frequency of this feature in all the categories
    freqsum=sum([self.fprob(f,c) for c in self.categories()])

    # The probability is the frequency in this category divided by
    # the overall frequency
    p=clf/(freqsum)
    
    return p
  def fisherprob(self,item,cat):
    # Multiply all the probabilities together
    p=1
    features=self.getfeatures(item)
    for f in features:
      p*=(self.weightedprob(f,cat,self.cprob))

    # Take the natural log and multiply by -2
    fscore=-2*math.log(p)

    # Use the inverse chi2 function to get a probability
    return self.invchi2(fscore,len(features)*2)
  def invchi2(self,chi, df):
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df//2):
        term *= m / i
        sum += term
    return min(sum, 1.0)
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.minimums={}

  def setminimum(self,cat,min):
    self.minimums[cat]=min
  
  def getminimum(self,cat):
    if cat not in self.minimums: return 0
    return self.minimums[cat]
  def classify(self,item,default=None):
    # Loop through looking for the best result
    best=default
    max=0.0
    for c in self.categories():
      p=self.fisherprob(item,c)
      # Make sure it exceeds its minimum
      if p>self.getminimum(c) and p>max:
        best=c
        max=p
    return best


def sampletrain(cl):
  cl.train('Nobody owns the water.','good')
  cl.train('the quick rabbit jumps fences','good')
  cl.train('buy pharmaceuticals now','bad')
  cl.train('make quick money at the online casino','bad')
  cl.train('the quick brown fox jumps','good')
