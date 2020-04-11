# constructs the network
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

class Network:
  conferences = [
      'SIGMOD',
      'VLDB',
      'KDD',
      'EDBT',
      'ICDE',
      'ICDM',
      'SDM',
      'CIKM',
      'DASFAA',
      'PAKDD',
      'PKDD',
      'DEXA'
  ]

  questions = [
    "Location of Scientist's Institute vs Success of Scientist",
    'Correlation of Prestige of Institutes and Authors who Publish in Premium Venues',
    'Impact of Network Effect on Reputation & Success of Scientist',
    'Reputation of Publications vs Career of Scientist'
  ]

  def getConferences(self):
    return self.conferences

  def setConferences(self,new_conf):
    self.conferences = new_conf

  def getQuestions(self):
    return self.questions

  def setQuestions(self, new_quest):
    self.questions = new_quest

  def drawNetwork(self):
    conf = pd.read_csv ('authors.csv')
    G=nx.DiGraph()

    conf2 = conf.drop_duplicates()
    conf2 = conf2.sort_values(by=['pid','year'])

    # adding nodes:
    G.add_nodes_from(self.conferences)

    for i in range(len(conf2.index)-1):
        if conf2['pid'].iloc[i] == conf2['pid'].iloc[i+1]:
            G.add_edge(conf2['conf'].iloc[i+1], conf2['conf'].iloc[i])

    nx.draw(G, with_labels = True)