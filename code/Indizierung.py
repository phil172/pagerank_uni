# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 20:13:01 2021

@author: Xander
"""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.linalg import norm
import json



def decrement(n):
    return n-1


class Rank:
    
        
    def __init__(self,idliste_1):
        
         d={}
         i=1
         for element in idliste_1.keys():
             
             d[element]=i-1
             i=i+1
                
         self.idliste=d
         
         
    def url_to_number(self,url,version_1=True):
        if url in self.idliste.keys():
            if version_1==False:
                return self.idliste[url]
            if version_1==True:
                return self.idliste[url]+1
        
        
        else:
            print("url nicht in der Liste vorhanden")
            
            
            
            
    def number_to_url (self,number):
        if number in self.idliste.values():
            for n in self.idliste.keys():
                if number==self.idliste[n]: 
                    return n
        else:
            print("Nummer ist nicht einer Zahl zugeordnet")
        
            
    '''       
    def url_to_graph(self,linkstruktur):        #Graph in Dictionary-Form
        d={}
        for k in linkstruktur.keys():
            d[self.url_to_number(k)]=list(map(self.url_to_number,linkstruktur[k]))
        
        return d
     '''   
    
    ### Philipp's Graph mit startID = 1 zu Xanders Graph StartID = 0
    def graph_1_to_graph_0 (self,graph_1):
        d2={}
        for k in graph_1.keys():
            d2[int(k)-1]=list(map(decrement,graph_1[k]))
        return d2
    
                                  
    def graph_to_matrix(self,graph):
        dim=len(self.idliste)
        A=np.zeros((dim,dim))
        for k in graph.keys():
            l=len(graph[k])
            for v in graph[k]:
                A[k,v]=1/l
        
        
        A=A.transpose()
        As=csr_matrix(A)
        
        return As
        
    
    
    def fixpunktiteration(self,A,epsilon=0.001,m=0.15):           
        B=np.empty(A.shape)
        B.fill(1)
        M=(1-m)*A+(m/A.shape[0])*B
        M=csr_matrix(M)
        x=np.array([1]*A.shape[0])
        xalt=x*3
        differenz=norm((xalt-x))        #2-Norm
        i=1
        
        while differenz > epsilon:
            i=i+1
            xalt=x
            x=M.dot(x)
            differenz=norm(xalt-x)
            
        print(i)
        return x
    
    
    def rank(self,x):
        l=[]
        for i in range(x.shape[0]):
            l.append((self.number_to_url(i),x[i]))       #Liste mit Tupeln (url,x-Wert(Pagerank))
                  
        l.sort(key=self.g,reverse=True)
        
        # for j in range(len(l)):
        #     l[j]=l[j][0]
        return l #list(map(self.url_to_number,l))
        
    
    def g (self,tupel):
        return tupel[1]

    
    
    def graph_to_rank (self,graph,epsilon=0.001,m=0.15):
        
        if int(list(graph.keys())[0])==1:
            g=self.graph_1_to_graph_0(graph)
        else: g=graph
        A=self.graph_to_matrix(g)
        x=self.fixpunktiteration(A,epsilon,m)
        rank=self.rank(x)
        return rank
    
    
    
    
    

with open("id_dict.json", "r") as id:
    id_dict = json.load(id)
#print(d)

    



#d={'https://www.math.kit.edu/': 0, 'https://www.math.kit.edu/lehre/seite/spos/de': 1, 'https://www.math.kit.edu/seite/absolventen/': 2, 'https://www.math.kit.edu/dekanat/seite/dekan/de': 3, 'https://www.math.kit.edu/fakmath/seite/aemter/de': 4, 'https://www.math.kit.edu/iag3/de': 5, 'https://www.math.kit.edu/lehre/seite/studium-im-sommer-2021/de': 6, 'https://www.math.kit.edu/fakmath/seite/online_lehre/de': 7, 'https://www.math.kit.edu/grk1294/seite/eventsn/de': 8, 'https://www.math.kit.edu/fakmath/seite/seminarverbuchung/de': 9, 'https://www.math.kit.edu/lehre/seite/infostud/': 10, 'https://www.math.kit.edu/lehre/seite/ma-tema/de': 11, 'https://www.math.kit.edu/fakmath/seite/planung_sose_21/de': 12, 'https://www.math.kit.edu/stoch/seite/statrat-informationen/de': 13, 'https://www.math.kit.edu/ianm1/de': 14, 'https://www.math.kit.edu/dekanat/seite/geschfuehrung/de': 15, 'https://www.math.kit.edu/fakmath/de': 16, 'https://www.math.kit.edu/bibliothek/de': 17, 'https://www.math.kit.edu/iana3/de': 18, 'https://www.math.kit.edu/lehre/seite/lehramt/de': 19, 'https://www.math.kit.edu/grk1294/seite/open_positions/de': 20}
with open("id_graph.json", "r") as f:
    graph = json.load(f)

# f={"1": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "2": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "3": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "4": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "5": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "6": [2, 4, 5, 6, 7, 8, 10, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "7": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "8": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "9": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "10": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "11": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "12": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "13": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "14": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "15": [2, 4, 10, 12, 13, 14, 21, 5, 7, 9, 15, 20, 8, 17, 1, 6, 16, 18, 19], "16": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "17": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "18": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "19": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "20": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1], "21": [2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 1]}
# d2={}




#print(d2)    
i=Rank(id_dict)
print(i.idliste)
g2=i.graph_1_to_graph_0(graph)
x = i.fixpunktiteration(i.graph_to_matrix(g2), epsilon=0.001, m=0.15)

#l = i.rank(g2)
#print(l)
# page_rank_dict = dict()
# for i in range(len(list(id_dict.keys()))):
#     page_rank_dict[i+1] =    
    
#print(g2)
#m=i.graph_to_matrix(g2)  
#print(m)
#x=i.fixpunktiteration(m)
#print(x)
#print(i.rank(x))
#print
tup = i.graph_to_rank(graph)

    
