import json
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
idpath = 'id_dict.json'
datapath = 'links_to_pages.json'

class Graph():
    def __init__(self, idpath, datapath):
        self.datapath = datapath
        self.idpath = idpath
        self.data: dict = self.open(self.datapath)
        self.ids: dict  = self.open(self.idpath)
        self.graph = dict()

    def open(self, path):
        with open(path) as json_file:
            data = json.load(json_file)
        return data

# with open('id_dict.json') as json_file:
#     id_dict = json.load(json_file)

    def get_graphs(self):
        ids: dict = self.ids
        data: dict = self.data
        for i in range(1, len(list(data.keys()))):
            lst = list(data[list(data.keys())[i]])
            new_lst = []
            A = (pd.Series(lst)).map(ids) #convert the list to a pandas series temporarily before mapping
            B = list(A.dropna())
            for el in B:
                new_lst.append(int(el))
            self.graph[i] = new_lst
        return self.graph



    def test(self):
        ids: dict = self.ids
        data: dict = self.data
        print(ids)
        lst = list(data[list(data.keys())[0]])

gr = Graph(idpath, datapath)
#gr.test()
# gr.get_graph()
graph = gr.get_graphs()
print(graph)



