from modules import *

class Categorie(object):
    def createcategorie(self, request):
        data = json.dumps(request.get_json())
        return requests.post(apidomain + 'categorie', data, headers=headers).content

    def updatecategorie(self, request):
        data = json.dumps(request.get_json())
        return requests.patch(apidomain + 'categorie', data, headers=headers).content

    def deletecategorie(self, id):
        return requests.delete(apidomain + 'categorie/'+id, headers=headers).content
         
    def getallcategories(self):
        return requests.get(apidomain + 'categorie', headers=headers).content
        
    def getbyidcategorie(self, id):
        return requests.get(apidomain + 'categorie/'+id, headers=headers).content
        
    def getcategorybyquery(self,query):
        q = '?q={"filters":[{"name":"name","op":"eq","val":"'+query+'"}]}'
        result = requests.get(apidomain+"categorie"+q, headers=headers).content
        return result
        
class Topicmodel(object):
    
    def getclassificationmodel(self):
        classifier = Classifier()
        result = json.dumps(classifier.load("classvectors.json"))
        return result
    
    def createtopicmodel(self, request):
        data = json.dumps(request.get_json())
        return requests.post(apidomain + 'topicmodel', data, headers=headers).content

    def updatetopicmodel(self, request):
        data = json.dumps(request.get_json())
        return requests.patch(apidomain + 'topicmodel', data, headers=headers).content

    def deletetopicmodel(self, id):
        return requests.delete(apidomain + 'topicmodel/'+id, headers=headers).content
         
    def getalltopicmodels(self):
        return requests.get(apidomain + 'topicmodel', headers=headers).content
        
    def getbyidtopicmodel(self, id):
        return requests.get(apidomain + 'topicmodel/'+id, headers=headers).content
    
    def getcategorykeysbypage(self):
        page=1
        result = requests.get(apidomain + 'topicmodel?page='+str(page), headers=headers)
        numpages = result.json()['total_pages']
        data = (result.json()['objects'])
        for i in range(2,numpages):
            result = requests.get(apidomain + 'topicmodel?page='+str(page), headers=headers)
            data += (result.json()['objects'])
        return json.dumps(data)    
        
class Article(Modules):
    
    def createarticle(self, request):
        data = json.dumps(request.get_json())
        return requests.post(apidomain + 'article', data, headers=headers).content

    def updatearticle(self, request):
        data = json.dumps(request.get_json())
        return requests.patch(apidomain + 'article', data, headers=headers).content

    def deletearticle(self, id):
        return requests.delete(apidomain + 'article/'+id, headers=headers).content
         
    def getallarticles(self):
        return requests.get(apidomain + 'article', headers=headers).content
        
    def getbyidarticle(self, id):
        return requests.get(apidomain + 'article/'+id, headers=headers).content
    
    def get_articlebypage(self,page):
        result = requests.get(apidomain + 'article?page='+str(page), headers=headers)
        # resultamt = (result.json()['total_pages'])
        # val =int(resultamt)- int(page-1)
        # result = requests.get(apidomain + 'article?page='+str(val), headers=headers)
        articles={}
        articles['data']=result.json()['objects']
        alltopicsandkeys=self.traversePages("setTopicandTerms",'topicmodel')
        categories=''
        for i in range(0,len(articles['data'])):
            categories = self.getCategory(articles['data'][i]['CONTENT'],2,alltopicsandkeys)
            categories = json.loads(categories)
            articles['data'][i]['articlecategories'] = categories['categoriestop3']
            
        # print(articles['data'][0]['articlecategories'])
        articles['total_pages'] = (result.json()['total_pages'])
        return json.dumps(articles)
        
   
    def get_classofdata(self,request):
        # print(request.form['url'])
        # data = request.data
        
        '''
        Filter to see if the domain exists in domain table if it does then, get the id, if it does not then, 
        domain is unsupported and wont be added to the db, however best attempt classigication, would still be done.
        On submission of the url to the article table, if integrigity violated then just return the article with its categoriese
        '''
        
        #  q = '?q={"filters":[{"name":"domainname","op":"like","val":"%'+query+'%"}]}'
        # qresult = requests.get("http://0.0.0.0:8085/api/domain"+q).content
        alltopicsandkeys=self.traversePages("setTopicandTerms",'topicmodel')
        data =request.get_json()
       
        
        supportedonlinearticle = 0
        # print(data['url'])
        if("trinidadexpress.com" in data['url']):
            spider = Crawler('https://www.trinidadexpress.com',"",['p'],['time'],['h1','headline'])
            supportedonlinearticle=1
            # print("RESULT1: ")
            # print(supportedonlinearticle)
        elif("guardian.co.tt" in data['url']):
            spider = Crawler('https://www.guardian.co.tt',"",['p','bodytext'],['span','textelement-publishing date'],['h1','headline'])
            supportedonlinearticle=1
        elif("newsday.co.tt" in data['url']):
            spider = Crawler('http://newsday.co.tt',"",['p'],['time'],['h1'])
            supportedonlinearticle=1
        elif("looptt.com" in data['url']):
            spider = Crawler('http://www.looptt.com',"",['p'],['span','date-tp-4 border-left'],['span','field field--name-title field--type-string field--label-hidden'])
            supportedonlinearticle=1
     
        if supportedonlinearticle:
            result = spider.get_article_data(data['url'])
            # print("RESULT2: ")
            # print(result)
            r = requests.post(apidomain + 'article', result, headers=headers)#use db api to post the data to database
            result = self.getCategory(spider.acorpus["CONTENT"],1,alltopicsandkeys)
            addsource = json.loads(result)
            addsource['asource'] = data['url']
            result =json.dumps(addsource)
            # print(result)
        else:
            if self.uri_validator(data['url']): # if normal valid url then just try to the content
                spider = Crawler(data['url'],"",['p'],"",['h1'])
                spider.getAllPageContent(data['url'])
                result = self.getCategory(spider.acorpus["CONTENT"],1,alltopicsandkeys)
                addsource = json.loads(result)
                addsource['asource'] = data['url']
                result =json.dumps(addsource)
                # result = self.getCategory(result)
            else:
                result = data['url']       
                result = self.getCategory(result,1,alltopicsandkeys)
                addsource = json.loads(result)
                addsource['asource'] = "UserInput"
                result =json.dumps(addsource)
        return result

# class Keyword(object):
    
#     def createkeyword(self, request):
#         data = json.dumps(request.get_json())
#         return requests.post(apidomain + 'keyword', data, headers=headers).content

#     def updatekeyword(self, request):
#         data = json.dumps(request.get_json())
#         return requests.patch(apidomain + 'keyword', data, headers=headers).content

#     def deletekeyword(self, id):
#         return requests.delete(apidomain + 'keyword/'+id, headers=headers).content
         
#     def getallkeywords(self):
#         return requests.get(apidomain + 'keyword', headers=headers).content
        
#     def getbyidkeyword(self, id):
#         return requests.get(apidomain + 'keyword/'+id, headers=headers).content
        
#     def getKeyword(self,query):
#         q = '?q={"filters":[{"name":"word","op":"eq","val":"'+query+'"}]}'
#         result = requests.get(apidomain+'keyword'+q).content
#         return result
    
#     def getKeywordByPage(self,page):
#         # q = '?q={"filters":[{"name":"word","op":"eq","val":"'+query+'"}]}'
#         # result = requests.get(apidomain+'keyword'+q).content
#         result = requests.get(apidomain + 'keyword?page='+str(page), headers=headers).content
#         return result