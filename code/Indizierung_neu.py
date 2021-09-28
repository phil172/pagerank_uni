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
            
        #print(i)
        return x
    
    
    def rank(self,x):
        l=[]
        for i in range(x.shape[0]):
            l.append((i+1,x[i]))       #Liste mit Tupeln (url,x-Wert)
                  
        l.sort(key=self.g,reverse=True)
        
        d={}
        for k in range(len(l)):
            d[l[k][0]]=l[k][1]
        
        return d
        
    
        #for j in range(len(l)):
         #   l[j]=l[j][0]
        
        #return list(map(self.url_to_number,l))
        
    
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


with open("id_graph.json", "r") as f:
    graph = json.load(f)

#print(d2)    
i=Rank(id_dict)
#print(i.idliste)
#g2=i.graph_1_to_graph_0(f)
#print(g2)
#m=i.graph_to_matrix(g2)  
#print(m)
#x=i.fixpunktiteration(m)
#print(x)
#print(i.rank(x))
#print
rank_dict = i.graph_to_rank(graph)

with open("pageranks.json", "w") as outfile:
    json.dump(rank_dict, outfile)   

