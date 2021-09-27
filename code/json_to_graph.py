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

    def to_json(self, file):
        with open(file, "w") as outfile:
            json.dump(self.graph, outfile)

    def get_graphs(self):
        ids: dict = self.ids
        data: dict = self.data
        print(len(list(data.keys())))
        for i in range(0, len(list(data.keys()))):
            lst = list(data[list(data.keys())[i]])
            new_lst = []
            A = (pd.Series(lst)).map(ids) #convert the list to a pandas series temporarily before mapping
            B = list(A.dropna())
            for el in B:
                new_lst.append(int(el))
            self.graph[i+1] = new_lst
        return self.graph



gr = Graph(idpath, datapath)
graph = gr.get_graphs()
gr.to_json("id_gaph.json")



