# constructs the network
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
