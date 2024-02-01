import json
# GBC(group by Class) Model by David Charles
# words in a doc are related, and the strength of the relation increases across multiple documents 
# as the co-occurence between words across the documents increase.
# from collections import Counter

class GBC:
    
    def __init__(self):
        self.model = {}
        self.keycount = {}
        self.name = "gbc"
        self.doctotal = 0
        self.matchminimum = 1
        self.prediction = {}
        self.termVectors = {}
        self.penalty = {}
        self.topics = {}
        self.keys = {}
    def init(self,topics,keys):
        self.doctotal = 0
        self.matchminimum = 1
        self.prediction = {}
        self.termVectors = {}
        self.penalty = {}
        self.topics = topics
        self.keys = keys
        for topic,topiclist in topics.items():
             self.model[topic] = {}
             self.keycount[topic]  = {}
             for i in range(0,len(topiclist)):
                keyword = topiclist[i]
                self.model[topic][keyword]={}
                self.model[topic][keyword]['DocumentCount'] = 0
                self.model[topic][keyword]['TermVectorAverage'] = 0
                self.model[topic][keyword]['features'] = {}
                self.keycount[topic][keyword] = 0
        return self
    def MinKey(self,amt):
        self.matchminimum = amt
    def PenaltyScores(self):
        return self.penalty
    def TermVectors(self):
        return self.termVectors
    def build(self,articlecontent): #check and see if key word exists for each topic
        articlecontent = articlecontent.lower()
        self.doctotal += 1
        for topic,topiclist in self.topics.items():
            for i in range(0,len(topiclist)):
                keyword = topiclist[i]
                # print(self.keys)
                # print(keyword)
                if self.goodtopicscore(self.keys[keyword],articlecontent):#keyword.lower() in articlecontent:
                    visited = {}
                    result = articlecontent.split()
                    for j in range(0,len(result)):
                            if result[j] in self.model[topic][keyword]['features'] :
                                if result[j] not in visited:
                                    self.model[topic][keyword]['features'][result[j]] += 1
                                    visited[result[j]] = 1
                            else:
                                self.model[topic][keyword]['features'][result[j]] = 1
                                visited[result[j]] = 1
                                
                    self.keycount[topic][keyword] += 1
                    self.model[topic][keyword]['features'][keyword] = self.keycount[topic][keyword]#*(self.model[topic][keyword]['docamt']/self.doctotal) # Ensures Keyword is always 100 %
                    self.model[topic][keyword]['DocumentCount'] = self.keycount[topic][keyword]
                    # print("word={} Occurence={}\n".format(keyword,self.model[topic][keyword]['docamt']))
    def setweights(self):
       
            for topic,topiclist in self.topics.items():
                for i in range(0,len(topiclist)):
                    largestkey = 0 #each key word has its own feturevector, and hence its own average weighting value
                    total = 0
                    sumofweights = 0
                    numberofweights = 0
                    averageweight = 0
                    keyword = topiclist[i]
                    result =self.model[topic][keyword]['TermVectorAverage']
                    # print(result)
                    if(result<=0):
                        # print('setweights test')
                        # print(self.topics.items())
                        features = self.model[topic][keyword]['features']
                        sortedweights = sorted(features.items(),key=lambda p:p[1])
                        for k,v in sortedweights:
                            if largestkey < v:
                                largestkey = v # prevents counting duplicated weights
                                sumofweights += v
                                numberofweights += 1
                        if(sumofweights > 0 and numberofweights>0):
                            averageweight = sumofweights/numberofweights
                            self.model[topic][keyword]['TermVectorAverage'] = averageweight
                            for k,v in sortedweights:
                                averageweightofvalue = round(v/averageweight,6)
                                self.model[topic][keyword]['features'][k] = round((averageweightofvalue),6) 
                        
    def removeweights(self):
        for key, value in self.model["model"].items():
            features = self.model["model"][key]["features"]
            termcount = 0
            if(self.model["model"][key]['TermVectorAverage']>0):
                for k,v in features.items():
                     termcount = features[k] *  self.model["model"][key]['TermVectorAverage']
                     self.model["model"][key]["features"][k] = round(termcount,1)
                # print('removeweights test')
            self.model["model"][key]['TermVectorAverage'] = 0
        
    def goodtopicscore(self,keys,content):
        matchedkeysize = 0
        content = content.lower()
        for i in range(0,len(keys)):
            if keys[i].lower() in content:
                matchedkeysize += content.count(keys[i].lower())
        if matchedkeysize < self.matchminimum:
            return 0
        return matchedkeysize
    def tojson(self,path):
        self.name = path
        with open(self.name+'.json', 'w') as modelobj:
            json.dump(self.model, modelobj,sort_keys=True, indent=4)
    def load(self,path):
        with open(path, 'r') as fp:
            self.model = json.load(fp)
            self.topics['model'] = list(self.model["model"].keys())
        return self.model
        
    def getTopic(self):
        largest = 0
        key = ""
        for k,v in self.prediction.items():
            if v > largest:
                largest = v
                key = k
        return key, largest

    def getTopics(self):
        return self.prediction
    
    def predict(self,modeloption,doc):
        docset = set(doc.lower().split())
        topic = {}
        penalty = {}
        
        # penaltyCNT = {}
        numberOftopics = len(self.model[modeloption].items())
        for row,col in self.model[modeloption].items():
            result = col['features'].keys() & docset
            
            if(len(result)>0):
                for val in result:
                    if val in penalty:
                        penalty[val] += col['features'][val]
                        # penaltyCNT[val] +=1
                    else:
                        penalty[val] = col['features'][val]
                    # penaltyCNT[val] = 1
        # print("==================================")
        for row,col in self.model[modeloption].items():
            result = col['features'].keys() & docset
            if(len(result)>0):
                self.termVectors[row] = result
                # print(row)
                # print (result)
                # marker=1
                numberofterms = len(doc.lower().split())
                numtopics = len(self.model[modeloption])
                # print("{} {}".format(row,result))
                for val in result:
                    scale = 1#doc.lower().count(val)
                    # print("Scale:{} Word:{} ScaleValue:{}".format(scale,val,(col['features'][val] * scale)))
                    
                    # if (penalty[val] == col['features'][val]):
                    #     # print("ImportantWord {} = {}".format(val,col['features'][val]))
                    #     penalty[val]  = 1
                    # averagepenalty =  self.getAvergaePenalty(penalty)
                    # penaltyoutcome = penalty[val]/averagepenalty
                    # # if(penaltyCNT[val]<numtopics):
                    # if penaltyoutcome <=self.penaltyborder:
                        # print("{} {}".format(val,penaltyoutcome))
                    if  row not in topic:
                        topic[row] = (col['features'][val] * scale)/penalty[val]
                        # marker=0
                    else:
                        topic[row] +=  (col['features'][val] * scale)/penalty[val]
                    # else:
                    #     print("{} {}".format(val,penaltyoutcome))
                    #     if marker:
                    #         topic[row] = (col['features'][val])/penalty[val]  
                    #         marker=0
                    #     else:
                    #         topic[row] +=  (col['features'][val])/penalty[val]  
        
        self.prediction = topic
        self.penalty['Penalty'] = penalty
        # print("\nPenalty: {}".format(penalty))
        # print(topic)
        return self#(topic)
            
    def showfeatures(self):        
        for model,modelvalue in self.model.items():
            for row,col in modelvalue.items():
                sortedweights = sorted(col['features'].items(),key=lambda p:p[1],reverse=True)
                print("{}[{} : {}]".format(model,row,sortedweights))
                
    def showmodels(self):
        for model,modelvalue in self.model.items():
            print(model)
            
            
class Merger:
    
    def merge(self,models):
        model = GBC()
        model = models[0]
        model.removeweights()
        for i in range(1,len(models)):
            models[i].removeweights()
            topics = models[i].topics['model']
            # print(topics)
            for j in range(0,len(topics)):
                # print(topics[j])
                jtopic = models[i].model["model"][topics[j]]
                jfeatures = models[i].model["model"][topics[j]]["features"]
                if topics[j] in model.topics['model']:  #merge with existing model is class already exist
                    x = model.model['model'][topics[j]]['features']
                    y = jfeatures
                    z = { k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) }
                    model.model['model'][topics[j]]['features'] = z 
                    model.model['model'][topics[j]]['DocumentCount'] += jtopic['DocumentCount']
                    # print(z)
                else:
                    model.topics['model'].append(topics[j]) # otherwise append new class to existing model
                    # print(model.topics['model'])
                    model.model["model"][topics[j]] = {}
                    model.model['model'][topics[j]]['DocumentCount'] = jtopic['DocumentCount']
                    model.model['model'][topics[j]]['TermVectorAverage'] = jtopic['TermVectorAverage']
                    model.model["model"][topics[j]]["features"] = jfeatures
        
        model.setweights()
        # print(model.model["model"])
        # model.tojson("merged")   
        return model
        # print ( model.model["model"])
        # print("\n")
        # x = {'both1':1, 'both2':2, 'only_x': 100 }
        # y = {'both1':10, 'both2': 20, 'only_y':200 }
        
        # print ({ k: x.get(k, 0) + y.get(k, 0) for k in set(x) })
        # print({ k: x.get(k, 0) + y.get(k, 0) for k in set(x) & set(y) })
        # print({ k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) })