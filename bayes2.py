from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.metrics import confusion_matrix , classification_report

newsgroups_train = fetch_20newsgroups(subset='train')
# categories = ['alt.atheism', 'talk.religion.misc',
#               'comp.graphics', 'sci.space']
# categories=['alt.atheism','soc.religion.christian','comp.graphics','sci.med']

categories =[
 'alt.atheism',
 'sci.space',
  'comp.graphics',
 'talk.religion.misc',
 
 'comp.os.ms-windows.misc',
 'comp.sys.ibm.pc.hardware',
 'comp.sys.mac.hardware',
 'comp.windows.x',
 'misc.forsale',
 'rec.autos',
 'rec.motorcycles',
 'rec.sport.baseball',
 
 
 'rec.sport.hockey',
 'sci.crypt',
 'sci.electronics',
 'sci.med',
 'soc.religion.christian',
 'talk.politics.guns',
 'talk.politics.mideast',
 'talk.politics.misc'
 
 
 ]


newsgroups_train = fetch_20newsgroups(subset='train',
                                      categories=categories)
                                      
                                      
newsgroups_test = fetch_20newsgroups(subset='test',
                                     categories=categories)                                      
                                      
                                      
vectorizer =TfidfVectorizer()# TfidfVectorizer()#CountVectorizer()
# the following will be the training data
vectors = vectorizer.fit_transform(newsgroups_train.data)
vectors.shape


# this is the test data
vectors_test = vectorizer.transform(newsgroups_test.data)

clf = MultinomialNB(alpha=.02)

# the fitting is done using the TRAINING data
# Check the shapes before fitting
vectors.shape
#(2034, 34118)
newsgroups_train.target.shape
#(2034,)

# fit the model using the TRAINING data
clf.fit(vectors, newsgroups_train.target)

# the PREDICTION is done using the TEST data
pred = clf.predict(vectors_test)

# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html

print(len(pred))
count = 0
y_true =[]
y_pred = []

for i in range (len(pred)):
    y_true.append(newsgroups_test.target_names[newsgroups_test.target[i]])
    y_pred.append(newsgroups_test.target_names[pred[i]])
    if pred[i]==newsgroups_test.target[i]:
        count=count+1

# print(y_pred)
print(confusion_matrix(y_true, y_pred, labels=categories))
print(classification_report(y_true, y_pred, labels=categories))
print("\n")
print("Total: {} \n True: {} \n False: {}".format(len(pred),count,len(pred)-count))

f = open("MNB20newsgroup.txt", "w")
f.write(str(confusion_matrix(y_true, y_pred,labels=categories)))
f.write("\n")
f.write(classification_report(y_true, y_pred,labels=categories))
f.write("\n")
f.write(str(count)+"\n")
f.write(str(len(pred))+"\n")
f.write(str(count/len(pred))+"\n")    