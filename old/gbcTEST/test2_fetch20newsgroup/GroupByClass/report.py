import csv
from gbk2 import GBK as Model
from sklearn.datasets import fetch_20newsgroups
# from gbk.gbk import GBK as Model2
from classifier.gbc import GBC as Model2
from sklearn.metrics import confusion_matrix , classification_report
# from testdocs import *

# https://github.com/DavidDexterCharles/bit-of-data-science-and-scikit-learn/blob/master/notebooks/FeatureExtraction.ipynb
# categories = ['alt.atheism', 'talk.religion.misc','comp.graphics', 'sci.space']#https://github.com/gokriznastic/20-newsgroups_text-classification/blob/master/Multinomial%20Naive%20Bayes-%20BOW%20with%20TF.ipynb
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

keys = {}
keys ['alt.atheism'] =['alt.atheism']
keys ['comp.graphics'] =['comp.graphics']
keys ['talk.religion.misc'] =['talk.religion.misc']
keys ['sci.space'] =['sci.space']

keys ['comp.os.ms-windows.misc'] =['comp.os.ms-windows.misc']
keys ['comp.sys.ibm.pc.hardware'] =['comp.sys.ibm.pc.hardware']
keys ['comp.sys.mac.hardware'] =['comp.sys.mac.hardware']
keys ['comp.windows.x'] =['comp.windows.x']
keys ['misc.forsale'] =['misc.forsale']
keys ['rec.autos'] =['rec.autos']
keys ['rec.motorcycles'] =['rec.motorcycles']
keys ['rec.sport.baseball'] =['rec.sport.baseball']


keys ['rec.sport.hockey'] =['rec.sport.hockey']
keys ['sci.crypt'] =['sci.crypt']
keys ['sci.electronics'] =['sci.electronics']
keys ['sci.med'] =['sci.med']
keys ['soc.religion.christian'] =['soc.religion.christian']
keys ['talk.politics.guns'] =['talk.politics.guns']
keys ['talk.politics.mideast'] =['talk.politics.mideast']
keys ['talk.politics.misc'] =['talk.politics.misc']

testdata  = fetch_20newsgroups(subset='test', categories=categories)
traindata = fetch_20newsgroups(subset='train', categories=categories)
# remove=('headers', 'footers', 'quotes'),


# def getTopic(topic):
#     largest = 0
#     key = ""
#     for k,v in topic.items():
#         if v > largest:
#             largest = v
#             key = k
#     # print (key)
#     # print (largest)
#     return key, largest
    
# def predict(i,name):
#     model = Model2()
#     model.load(name)
#     result = model.predict('model',(testdata.data[i].lower())).getTopic()
#     key,value = result#getTopic(result)
#     print("\nTAG_RETURNED: {} {}".format(key,value))
#     print ("RESULT:{}".format(result))
#     print("TAG_EXPECTED {}: {}\n\n{}".format(i,list(testdata.filenames)[i],testdata.data[i]))
    
    
    # return result
    
# def ReportForModel(name):
#     model = Model()
#     model.load(name)
#     dataset = list(testdata.data)
#     testdata2  = fetch_20newsgroups(subset='test',remove=('headers', 'footers', 'quotes'),categories=categories)#remove=('headers', 'footers', 'quotes'), 
#     datasetHFQ =  list(testdata2.data) #removed header footer and quotes
#     numFalse = 0
#     numTrue = 0
#     with open('report.csv', mode='w') as report_file:
#         report_writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         report_writer.writerow(['ID','TAG_WEIGHT','TAG_RETURNED', 'TAG_EXPECTED', 'OUTCOME','OUTCOME_HFQ_REMOVED','TAG_RETURNED_HFQ_REMOVED','TAG_WEIGHT_HFQ_REMOVED'])
#         for i in range(0,len(dataset)):
#             result = model.predict('model',(dataset[i].lower()))
#             tag,weight = getTopic(result)
#             result2 = model.predict('model',(datasetHFQ[i].lower()))
#             tag2,weight2 = getTopic(result2)
            
#             for j in range(0,len(categories)):
#                 if categories[j] in testdata.filenames[i]:
#                     report_writer.writerow([i, weight,tag,categories[j],categories[j]==tag,categories[j]==tag2,tag2,weight2])                                                           #the number of occurence of the word in the query string{WAS WRONG], weighting was the problem
#                     if categories[j]!= tag:
#                         numFalse += 1
#                     else:
#                         numTrue += 1
#     print("\n")
#     print("Total: {} \n True: {} \n False: {}".format(len(dataset),numTrue,numFalse))

def printAccuracy(name):   
    f = open("GBC20newsgroup.txt", "w")
    model = Model2()
    model.load(name)
    dataset = list(testdata.data)
    numFalse = 0
    numTrue = 0
    y_true =[]
    y_pred = []
    for i in range(0,len(dataset)):
        result = model.predict('model',(dataset[i].lower())).getTopic()
        tag,weight = result# getTopic(result)
        y_true.append(testdata.target_names[testdata.target[i]])
        y_pred.append(tag)
        if testdata.target_names[testdata.target[i]]!= tag:
            numFalse += 1
            print(numFalse)
        else:
            # print("{} {}".format(testdata.target_names[testdata.target[i]],tag))
            numTrue += 1
        
       
    print(confusion_matrix(y_true, y_pred, labels=categories))
    print(classification_report(y_true, y_pred, labels=categories))
    
    print("\n")
    print("Total: {} \n True: {} \n False: {}".format(len(dataset),numTrue,numFalse))
    
    f.write(str(confusion_matrix(y_true, y_pred,labels=categories)))
    f.write("\n")
    f.write(classification_report(y_true, y_pred,labels=categories))
    f.write("\n")
    f.write(str(numTrue)+"\n")
    f.write(str(len(dataset))+"\n")
    f.write(str(numTrue/len(dataset))+"\n")


def RebuildNewsGroupModel(name,keywords):
    model = Model2()
    topics = {}
    topics['model'] =categories# ['alt.atheism', 'talk.religion.misc','comp.graphics', 'sci.space']#keywords

    model.init(topics,keys)
    model.matchminimum = 1 # because we are training on tagged data 
    
    # categories = topics['model']
    newsgroups_train =traindata# fetch_20newsgroups(subset='train', categories=categories)
    doclist = list(newsgroups_train.data)   
    
    for i, doc in enumerate(list(newsgroups_train.data)):
        tags = ""
        for j in range(0,len(categories)):
            if categories[j] in newsgroups_train.filenames[i]:
                tags += categories[j] + " "
        model.build((doc)+" "+tags+" ")
                    
    
    model.setweights()
    
    model.tojson(name)
    

if __name__ == '__main__':
    
    # https://textblob.readthedocs.io/en/dev/classifiers.html
    RebuildNewsGroupModel("modeltest",categories)
    
    print("test")
    
    
    printAccuracy("modeltest.json")
    # ReportForModel("model5.json")
    # ReportForModel("model11.json")
    # print("{} {}".format(testdata.filenames[7], testdata.target[:10]),list(testdata.data)[7])
    
    # Fail=[63,679,682,684,685,19,93,97,98,405,406,414,416]# known fails
    
    # predict(114,"TrainData3model.json")
    
   
    # print(testdoc)
    # model.load("TrainData3model.json")
    # result = getTopic(model.predict("model1",testdoc[1]))
    # print("{}".format(result))