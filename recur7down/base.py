# coding: utf-8



import sys
try:
    reload(sys)
    sys.setdefaultencoding("utf-8")
except:
    print('python3')
    
import pandas as pd
import json
import requests
import os
from time import time







class Collect(object):
    
    def __init__(self, link, place_id, cat_id):
        
        
        self.link =  link.format(place_id, cat_id, '{}')

        self.place_id = place_id
        self.cat_id = cat_id
        self.collect = []
        self.df = None
        self.flag = 0 
        
        
    def __scrape(self, index):
        
        try:
            products = json.loads(requests.get(self.link.format(index), timeout=3).text)['responseData']['product_info']
            print 'O',
            
            if len(products)==0:
                try: 
                    if 0==len(json.loads(requests.get(self.link.format(index), timeout=3).text)['responseData']['product_info']):
                        print 'E',
                        self.flag = 1
                        return
                except:
                    print '?',
                    self.__scrape(index)
            

            for product in products:
                self.collect.append(product)
                
        except Exception as e:
            print e
            print 'X',
            self.__scrape(index)  
            
    def main(self):
        
            
        for i in range(180):
            if not self.flag:
                self.__scrape(i)
                    
                                    
        print(len(self.collect))

        self.df = pd.DataFrame(self.collect) 
        
        try:
            col = list(test.df.columns)
            col = [col.pop(col.index('pid')), col.pop(col.index('title'))]+col
            self.df = self.df[col]
        except:
            print 'U'
        
        return self.df     
    def save(self):
        try:
            name = "{}_{}.xlsx".format(self.place_id, self.cat_id)
            self.df.to_excel(name, encoding="utf-8", index=False)
            print "Save Success! for "+name
        except:
            print "Save Error"
    def __repr__(self):
        return "place: "+ str(self.place_id)+ " category: "+ str(self.cat_id)+ " scraped: "+ str(self.flag==1)
        

