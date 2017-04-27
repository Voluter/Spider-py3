import json
import requests
import re
import os
from multiprocessing import Pool
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
import csv
import random
import time


class Crawer(object):
    def __init__(self, _url):
        self.url = _url
    
    def get_one_page(self, url):
        print('Crawling ' + url)
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"}
        
        response = requests.get(url,headers=headers)
        time.sleep(random.random()*4)#休眠，防止访问频率过高
        if response.status_code == 200:
            return response.text.encode('utf-8')
        return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = {}

        a0=soup.select('h3.name')
        a1=soup.select('.ename')
        a2=soup.select('li.ellipsis')
        if a0==[]:
            return None
        items['name'] =a0[0].string
        items['enName']=a1[0].string 
        items['type'] = a2[0].string
        items['country'] = a2[1].string.strip()
        items['showTime'] =a2[2].string
        star = soup.select('.star-on')
        if star:
            star = star[0]['style'][6:9]
        else:
            star = 'NotAiailable'
        items['rate'] = star
        return items

    def create_dataFile(self):
        if not os.path.exists('E:/test1.csv'):
            with open('E:/test1.csv', 'w') as csvfile:
                fieldnames = ['name', 'enName', 'type', 'country', 'showTime', 'rate']
                writer = csv.writer(csvfile)
                writer.writerow(('name', 'enName', 'type', 'country', 'showTime', 'rate'))
                csvfile.close()

    def save_data(self, data):
        if data is not None:
            with open('E:/test1.csv', 'a') as csvfile:
                fieldnames = ['name', 'enName', 'type', 'country', 'showTime', 'rate']
                writer = csv.writer(csvfile)
                writer.writerow(
                    (data['name'], data['enName'], data['type'], data['country'], data['showTime'], data['rate']))
                csvfile.close()

    def one_inf(self, n):
        url = self.url + str(n)
        html = self.get_one_page(url)
        data = self.parse_html(html)
        self.save_data(data)


Spider = Crawer('http://maoyan.com/films/')
Spider.create_dataFile()
pool = ThreadPool(4)
results = pool.map(Spider.one_inf, [i for i in range(100)])
pool.close()
pool.join()















