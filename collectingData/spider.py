# https://ieeexplore.ieee.org/abstract/document/6706853
import time
from crawler import Crawler
if __name__ == '__main__':
    pagesource = []
    pagesource.append("pagesource/artscultureentertainment.txt")#https://www.trinidadexpress.com/search/?f=html&q=crime&d1=2018-01-01&d2=2019-02-05&sd=desc&l=100&t=article&nsa=eedition&app%5B0%5D=editorial&o=800
    pagesource.append("pagesource/conflictswarpeace.txt")
    pagesource.append("pagesource/crimelawjustice.txt")
    pagesource.append("pagesource/disasteraccidentemergencyincident.txt")
    pagesource.append("pagesource/economybusinessfinance.txt")
    pagesource.append("pagesource/education.txt")
    pagesource.append("pagesource/environment.txt")
    pagesource.append("pagesource/health.txt")
    pagesource.append("pagesource/humaninterest.txt")
    pagesource.append("pagesource/lifestyleleisure.txt")
    pagesource.append("pagesource/politics.txt")
    pagesource.append("pagesource/religionbelief.txt")
    pagesource.append("pagesource/sciencetechnology.txt")
    pagesource.append("pagesource/society.txt")
    pagesource.append("pagesource/sport.txt")
    pagesource.append("pagesource/weather.txt")
    for i in range(0,len(pagesource)):
        spider = Crawler('https://www.trinidadexpress.com',pagesource[i],['p'],['time'],['h1','headline'])
        spider.crawl()
        # time.sleep(1)
        print(i,pagesource[i])


# Data date range
# 2018-01-01 TO
# 2019-02-05
# Articles
# countercheck = 