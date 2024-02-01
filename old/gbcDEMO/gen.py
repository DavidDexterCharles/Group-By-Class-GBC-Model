from gbc import GBC as Classifier
from iptc import IPTC_topics,IPTC_topictags #Import IPTC Topics And Tags
import json

from sklearn.datasets import fetch_20newsgroups


# Read in the articles
with open('data.json') as trainingdata:
  articles = json.load(trainingdata)
# Instantiate Classifier Object
classifier = Classifier()


# STEP 1 - Initialize The Class Vectors
classifier.init(IPTC_topics,IPTC_topictags).MinKey(2)
classifier.tojson('initializedclassvectors')


# STEP 2 - Populate The Class Vectors
for i in range(0,len(articles)):
           classifier.build(articles[i]['CONTENT'])
classifier.tojson('populatedclassvectors')


# STEP 3 - Standardize The Class Vectors
classifier.setweights()
classifier.tojson('standardizedclassvectors')



classifier2 = Classifier()

classifier2.MinKey(2)
classifier2.addtopic('Religion and Belief',['religion', 'christian', 'Mosk', 'Hindu', 'church'])
classifier2.addtopic(   'Art and Culture',
                        ['art', 'culture', 'entertainment', 'music', 'history', 'film', 'media', 'book', 'fashion', 'festival', 'comedy','museums', 
                                          'opera', 'drama', 'poetry','documentary', 'painting', 'theatre', 'sculpture', 'carnival' ]
                    )
for i in range(0,len(articles)):
           classifier2.build(articles[i]['CONTENT'])

classifier2.setweights()
classifier2.tojson('Testclassifier2classvectors')







'''
from modules import Modules,headers,apidomain,requests,json
m = Modules()
# result=m.traversePages("setTopicandTerms",'topicmodel')
# print(result.terms)
article = requests.get(apidomain + 'article', headers=headers).json()
numberofpages = article["total_pages"]
doclist =[]
nextpage = 1
while nextpage <= numberofpages:
    for i in range(0,len(article["objects"])):
        ob = {}
        ob['CONTENT'] = article["objects"][i]["CONTENT"]
        ob['DATE'] = article["objects"][i]["DATE"]
        ob['SOURCE'] = article["objects"][i]["SOURCE"]
        ob['domain_id'] = article["objects"][i]["domain_id"]
        doclist.append(ob)
    nextpage += 1
    article = requests.get(apidomain + 'article?page='+str(nextpage), headers=headers).json()

with open('data.json', 'w') as modelobj:
            json.dump(doclist, modelobj,sort_keys=True, indent=4)
'''

