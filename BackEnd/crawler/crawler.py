import asyncio, aiohttp , bs4 , re , json
from urllib.parse import urlparse
import requests
# pip3 install html5lib 
#html5lib needed for crawler to work

# import datefinder
# import time
# from datetime import datetime, date, time, timedelta #https://stackoverflow.com/questions/37980655/why-is-python-datetime-time-delta-not-found
# import socket
# from urllib.parse import urlparse
# # from htmlparser import HTMLPARSER
# import asyncio
# import aiohttp
# import bs4
# import tqdm
# import re
# import json

class Crawler: 
   
    def __init__(self,domainname,pagesource,contentparameters,dateparameters,titleparameters):
        '''
        domainname => name of the domainname
        pagesource => html syntax of the web page having the links to be traversed
        contentparameters => an array containng one or more of the following: tag,class,id for the purpose of extracting article content
        dateparameters = > an array containng one or more of the following: tag,class,id for the purpose of extracting article date
        titleparameters = > an array containng one or more of the following: tag,class,id for the purpose of extracting article title
        '''
        self.domainname =  '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(domainname)).rstrip("/")
        self.contentinfo = contentparameters
        self.dateinfo = dateparameters
        self.titleinfo = titleparameters
        self.pagesource = pagesource
        self.acorpus = {} 
        self.linkpool = {}
        self.artpool = []
       
    
   
    def crawl(self):
       self.pagesourcetolinkpool()
       self.setartpoolforlinkpool()
    #   print(self.linkpool)
       self.dowload_data()
   
    def get_article_data(self,url):
       self.linkpool[url]=1
       self.setartpool()
       return json.dumps(self.artpool[0])
   
    def pagesourcetolinkpool(self):
        '''
        add all urls on an html page/pages stored at self.pagesource to the link pool,
        currently would work only with trinidad express and not news day
        todo: strip domainname then add it back for more generic behaviour [self.domainname+result]
        '''
        ps = open(self.pagesource, "r")
        page = bs4.BeautifulSoup(ps.read(),features="html5lib")
        for link in page.find_all('a'):
            result = link.get('href')
            try:
                if result[0] == '/':
                    if result in self.linkpool:
                        self.linkpool[self.domainname+result] += 1 # Express
                    else:
                        self.linkpool[self.domainname+result] = 1 # Express
            except Exception as e:
                pass
            
    def getAllPageContent(self,url):
        html = requests.get(url).text
        page = bs4.BeautifulSoup(html,features="html5lib")
        self.acorpus["CONTENT"]=""
        for pharase in page.find_all(self.contentinfo[0]):
            self.acorpus["CONTENT"] += pharase.text+ "\n"
        return self.acorpus["CONTENT"]
     
                
    
    def setartpool(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        f = asyncio.wait([self.main(link) for link in self.linkpool])
        loop.run_until_complete(f)
        
        
    def setartpoolforlinkpool(self):
        loop = asyncio.get_event_loop()
        f = asyncio.wait([self.main(link) for link in self.linkpool])
        loop.run_until_complete(f)
    
    def dowload_data(self):
        # print(self.artpool)
        corpusname = self.pagesource.split('.')
        with open(corpusname[0]+'.json', 'w') as corpobj:
            json.dump(self.artpool, corpobj,sort_keys=True, indent=4)
        
    async def fetch(self,session, url):
        async with session.get(url) as response:
            return await response.text()
    
    async def main(self,url):
        async with aiohttp.ClientSession() as session:
            try:
                html = await self.fetch(session, url)
                # print(html)
                page = bs4.BeautifulSoup(html,features="html5lib")
                articledate = ""
                articlecontent = ""
                articletitle = ""
                authorname = ""
                if len(self.dateinfo)>1:
                    for pharase in page.find_all(self.dateinfo[0],class_=self.dateinfo[1]):
                        articledate = pharase.text+ "\n"
                        break
                elif len(self.dateinfo)>0:
                    for pharase in page.find_all(self.dateinfo[0]):
                        articledate = pharase.text+ "\n"
                        break
                
                if len(self.titleinfo)>1:    
                    for pharase in page.find_all(self.titleinfo[0],class_=self.titleinfo[1]):
                        articletitle += pharase.text
                elif len(self.titleinfo)>0:
                    for pharase in page.find_all(self.titleinfo[0]):
                        articletitle += pharase.text
                    
                if articledate and articletitle:
                    is_safe = 0
                    if len(self.contentinfo)>1:
                        for pharase in page.find_all(self.contentinfo[0],class_=self.contentinfo[1]):
                            articlecontent += pharase.text+ "\n"
                        is_safe = 1
                    elif len(self.contentinfo)>0:
                        for pharase in page.find_all(self.contentinfo[0]):
                            articlecontent += pharase.text+ "\n"
                        is_safe = 1
                    if is_safe:
                        self.acorpus["SOURCE"] = str(url)
                        self.acorpus["TITLE"] = re.sub('\s+',' ',articletitle)
                        dresult = re.sub('\s+',' ',articledate)
                        self.acorpus["DATE"] = dresult
                        self.acorpus["CONTENT"] =  re.sub('\s+',' ',articlecontent)
                        if("trinidadexpress.com" in url):
                            self.acorpus["domain_id"] =1
                        if("http://www.looptt.com" in url):
                            self.acorpus["domain_id"] =2
                        if("newsday.co.tt" in url):
                            self.acorpus["domain_id"] =3   
                        if("guardian.co.tt" in url):
                            self.acorpus["domain_id"] =4
                        
                        r = self.acorpus
                        # print(r)
                        # https://stackoverflow.com/questions/5244810/python-appending-a-dictionary-to-a-list-i-see-a-pointer-like-behavior
                        # https://stackoverflow.com/questions/184710/what-is-the-difference-between-a-deep-copy-and-a-shallow-copy
                        # https://docs.python.org/3/library/copy.html
                        self.artpool.append(r.copy())
                        # print(self.artpool)
                        # print(articletitle)
            except Exception as e:
                print (e)
                

# ^Cubuntu:~/environment/GBK-Topic-Modeler/BackEnd/app (master) $ pip3 install html5lib