# analyzes the network
from preprocessing import Network
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('agg')
sns.set()


class Science:

    def __init__(self):
        self.network = Network()

    def question1(self, conferences):
        # Network Science Measures that Reflect Prestige of Venues/Authors
        # conferences comes in the form of [['sigmod','1'],...]
        pass

    def question2(self, conferences):
        # Location of Scientist's Institute vs Success of Scientist
        # conferences comes in the form of [['sigmod','1'],...]
        pass

    def question3(self, conferences):
        # Correlation of Prestige of Institutes and Authors who Publish in Premium Venues
        # conferences comes in the form of [['sigmod','1'],...]
        pass

    def question4(self, conferences):
        # Reputation of Venues vs Career of Scientist
        # conferences comes in the form of [['sigmod','1'],...]
        pass
