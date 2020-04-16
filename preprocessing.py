# constructs the network
import time
import csv
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os

class Network:

    def __init__(self):

        self.questions = [
            "Network Science Measures that Reflect Prestige of Venues/Authors",
            "Location of Scientist's Institute vs Success of Scientist",
            'Correlation of Prestige of Institutes and Authors who Publish in Premium Venues',
            'Reputation of Venues vs Career of Scientist'
        ]

        self.publications_api = PublicationsAPI()
        self.network_graph = self.drawDiWeightedNetwork()


    def getConferences(self):
        f = open('config.txt', 'r')
        if f.mode == 'r':
            contents = f.read()
            # conferences is a list of lists each being [conf_name, tier]
            conferences = [i.strip().split(',') for i in contents.split('\n') if i != '']
        f.close()
        return conferences

    def addConference(self, new_conf):
        conferences = self.getConferences()
        conferences.append(new_conf)
        conferences.sort(key=lambda x: x[1])
        with open('config.txt', 'w') as f:
            for c in conferences:
                f.write(f'{c[0]},{c[1]}\n')


    def removeConference(self, to_rem):
        conferences = self.getConferences()
        conf_to_rem = next(x for x in conferences if x[0] == to_rem)
        new_conf = conferences.remove(conf_to_rem)
        with open('config.txt', 'w') as f:
            for c in conferences:
                f.write(f'{c[0]},{c[1]}\n')

    
    def getQuestions(self):
        return self.questions

    def setQuestions(self, new_quest):
        self.questions = new_quest

    def drawDiWeightedNetwork(self):
        conf = pd.read_csv ('authors.csv')
        G=nx.MultiDiGraph()

        conf2 = conf.drop_duplicates()
        conf2 = conf2.sort_values(by=['pid','year'])
        
        # getting list of conferences
        conftierlist = self.getConferences()
        conferences = []
        for i in range(len(conftierlist)):
                conferences.append(conftierlist[i][0])
        
        # adding nodes:
        G.add_nodes_from(conferences)

        for i in range(len(conf2.index)-1):
                if (conf2['pid'].iloc[i] == conf2['pid'].iloc[i+1]) and (conf2['conf'].iloc[i] != conf2['conf'].iloc[i+1]):
                        G.add_edge(conf2['conf'].iloc[i+1], conf2['conf'].iloc[i])
                        
        G2 = nx.DiGraph()
        G2.add_nodes_from(conferences)
        
        for i in range(len(conferences)):
                for j in range(len(conferences)):
                        if G.number_of_edges(conferences[i],conferences[j])>0:
                                G2.add_edge(conferences[i],conferences[j],weight=G.number_of_edges(conferences[i],conferences[j]))
        
        return G2
    
    # Returns a dict of {"sigmod":0.4, ...}
    def getVenuePrestigefromNetwork(self):
        prestige = nx.eigenvector_centrality(self.network_graph, weight= 'weight')
        
        return prestige
                                
    
    def getPublications(self,conf_list):
        print('getting publications')
        self.publications_api.create_csv(conf_list)

 

class PublicationsAPI:
     ### Fetch the authors.csv which contains all the publications in the listed conferences

    BASE_URL = "https://dblp.uni-trier.de/search/publ/api"
    def query_string_builder(self, conf_string):

        query_string = "stream:streams/conf/{}:".format(conf_string)

        return query_string


    def send_request(self, q, h, f, format="json"):
            http = urllib3.PoolManager()
            response = http.request('GET', self.BASE_URL, fields={
                    'q': q,
                    'h': h,
                    'f': f,
                    'format': format
            })

            return response.data


    def num_hits_in_conf(self, conf):
            query_string = self.query_string_builder(conf)
            json_data = json.loads(self.send_request(query_string, 0, 0).decode('utf-8'))

            return int(json_data['result']['hits']['@total'])


    # list of dict
    def add_entry_to_list(self, authors_list, pid, name, year, conf):
            authors_list.append({
                    'pid': pid,
                    'name': name,
                    'year': year,
                    'conf': conf
            })


    def add_conf_to_csv(self, conf):

        
            authors_list = []
            query_string = self.query_string_builder(conf)
            h = 1000
            f = 0
            # load 1000 each time
            for i in range(int(self.num_hits_in_conf(conf) / 1000) + 1):
                    print(conf, f)
                    # Send request
                    json_data = json.loads(self.send_request(query_string, h, f).decode('utf-8'))

                    # Iterate through each publication
                    for publication in json_data['result']['hits']['hit']:
                            # BASICALLY, some publications don't have a single fucking author.
                            if not 'authors' in publication['info'].keys():
                                    continue

                            authors = publication['info']['authors']['author']
                            year = publication['info']['year']

                            # Check if object is a list, they do not hold list of length 1 hence the extra check.
                            if type(authors) is list:
                                    for author in authors:
                                            self.add_entry_to_list(authors_list, author['@pid'], author['text'], year, conf)
                            else:
                                    self.add_entry_to_list(authors_list, authors['@pid'], authors['text'], year, conf)



                    # Increase f
                    f += 1000

            # Check file exists
            file_exists = True
            if not os.path.isfile('authors.csv'):
                    file_exists = False
            # Append CSV
            with open('authors.csv', 'a', encoding='utf8', newline='') as output_file:
                    fc = csv.DictWriter(output_file, fieldnames=authors_list[0].keys())

                    if not file_exists:
                            fc.writeheader()

                    fc.writerows(authors_list)


    def create_csv(self, conf_list):
            beginning = time.time()
            for conf in conf_list:
                    start = time.time()
                    print("===============================================")
                    print("starting {}".format(conf))
                    self.add_conf_to_csv(conf)
                    print("completed {}".format(conf))
                    print("time elapsed: {:.3f}s\n".format(time.time()-start))

            print("total time elapsed: {:.3f}s\n".format(time.time()-beginning))
