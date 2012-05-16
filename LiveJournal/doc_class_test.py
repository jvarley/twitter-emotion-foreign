import docclass as dc

classifier = dc.naivebayes(dc.getwords)
#classifier.setdb() #works!
#classifier.train("hello world","test_category")
