import asyncio, aiohttp , bs4 , re , json
from urllib.parse import urlparse

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
       self.initiate_linkpool()
    #   print(self.linkpool)
       self.dowload_data()
   
    def initiate_linkpool(self):
        '''
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
    
    def dowload_data(self):
        loop = asyncio.get_event_loop()
        f = asyncio.wait([self.main(link) for link in self.linkpool])
        loop.run_until_complete(f)
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
                for pharase in page.find_all(self.dateinfo[0]):
                    articledate = pharase.text+ "\n"
                for pharase in page.find_all(self.titleinfo[0],class_=self.titleinfo[1]):
                    articletitle += pharase.text
                if articledate and articletitle:    
                    for pharase in page.find_all(self.contentinfo[0]):
                        articlecontent += pharase.text+ "\n"
                    self.acorpus["SOURCE"] = str(url)
                    self.acorpus["TITLE"] = re.sub('\s+',' ',articletitle)
                    dresult = re.sub('\s+',' ',articledate)
                    self.acorpus["DATE"] = dresult
                    self.acorpus["CONTENT"] =  re.sub('\s+',' ',articlecontent)
                    r = json.dumps(self.acorpus)
                    self.artpool.append(r)
                    # print(self.artpool)
            except Exception as e:
                pass