# analyzes the network
from preprocessing import Network
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import numpy as np
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

    def question3a(self, conferences):
        
        # Get the tier lists
        tier1 = []
        tier2 = []
        tier3 = []

        for conference in conferences:
            if conference[1] == '1':
                tier1.append(conference[0])

            elif conference[1] == '3':
                tier2.append(conference[0])
            else:
                tier3.append(conference[0])


        df_authors = pd.read_csv("authors.csv")
        df_institutes = pd.read_csv("author_aff_rank_distance.csv")

        # tier1
        df_tier1 = df_authors[df_authors['conf'].isin(tier1)]
        df_tier1.drop_duplicates(subset ="pid", keep = "first", inplace = True)
        df_tier1_authors_institute_rank = df_institutes[df_institutes['pid'].isin(df_tier1.pid.unique())].drop(['affiliation', 'latitude', "longitude", "Distance to Top Ten"], axis=1)

        # tier2
        df_tier2 = df_authors[df_authors['conf'].isin(tier2)]
        df_tier2.drop_duplicates(subset ="pid", keep = "first", inplace = True)
        df_tier2_authors_institute_rank = df_institutes[df_institutes['pid'].isin(df_tier2.pid.unique())].drop(['affiliation', 'latitude', "longitude", "Distance to Top Ten"], axis=1)

        # tier3
        df_tier3 = df_authors[df_authors['conf'].isin(tier3)]
        df_tier3.drop_duplicates(subset ="pid", keep = "first", inplace = True)
        df_tier3_authors_institute_rank = df_institutes[df_institutes['pid'].isin(df_tier3.pid.unique())].drop(['affiliation', 'latitude', "longitude", "Distance to Top Ten"], axis=1)

        fig, ax = plt.subplots()


        a_heights, a_bins = np.histogram(df_tier1_authors_institute_rank['rank'].dropna(), bins=6, range=[0, 600])
        b_heights, b_bins = np.histogram(df_tier2_authors_institute_rank['rank'].dropna(), bins=6, range=[0, 600])
        c_heights, c_bins = np.histogram(df_tier3_authors_institute_rank['rank'].dropna(), bins=6, range=[0, 600])

        
        a_percent = [i/sum(a_heights)*100 for i in a_heights]
        b_percent = [i/sum(b_heights)*100 for i in b_heights]
        c_percent = [i/sum(c_heights)*100 for i in c_heights]
        width = (a_bins[1] - a_bins[0])/3

        ax.set_title('Institution Rank vs Percentage of Unique Authors in Different Tiers of Publication')
        ax.set_xlabel('Institution Rank (bin_width = 100)')
        ax.set_ylabel('Percentage of Unique Authors')
        ax.bar(a_bins[:-1], a_percent, width=width, align='edge', label='Tier 1 venues')
        ax.bar(b_bins[:-1]+width, b_percent, width=width, align='edge', label='Tier 2 venues')
        ax.bar(c_bins[:-1]+2*width, c_percent, width=width, align='edge', label='Tier 3 venues')
        ax.legend()
        
        ax.set_xticks(a_bins)
        plt.savefig('q3a_image.png')

        return "This graph shows the spread of the unique authors across different instition ranks for different tiers of venues."

    def question3b(self, conferences):
        # Get the tier lists
        tier1 = []
        tier2 = []
        tier3 = []

        for conference in conferences:
            if conference[1] == '1':
                tier1.append(conference[0])

            elif conference[1] == '3':
                tier2.append(conference[0])
            else:
                tier3.append(conference[0])


        df_authors = pd.read_csv("authors.csv")
        df_institutes = pd.read_csv("author_aff_rank_distance.csv").drop(['affiliation', 'latitude', "longitude", "Distance to Top Ten"], axis=1)

        # tier1
        df_tier1 = df_authors[df_authors['conf'].isin(tier1)]
        df_tier1_num_pub = df_tier1.groupby(['pid']).size().reset_index(name='num_publications')
        df_tier1_publications_institute_rank = pd.merge(df_tier1_num_pub, df_institutes, left_on='pid', right_on='pid', how='left')

        # tier2
        df_tier2 = df_authors[df_authors['conf'].isin(tier2)]
        df_tier2_num_pub = df_tier2.groupby(['pid']).size().reset_index(name='num_publications')
        df_tier2_publications_institute_rank = pd.merge(df_tier2_num_pub, df_institutes, left_on='pid', right_on='pid', how='left')
        
        # tier3
        df_tier3 = df_authors[df_authors['conf'].isin(tier3)]
        df_tier3_num_pub = df_tier3.groupby(['pid']).size().reset_index(name='num_publications')
        df_tier3_publications_institute_rank = pd.merge(df_tier3_num_pub, df_institutes, left_on='pid', right_on='pid', how='left')


        fig, ax = plt.subplots()

        a_heights, a_bins = np.histogram(df_tier1_publications_institute_rank['rank'].dropna(), bins=6, range=[0, 600])
        b_heights, b_bins = np.histogram(df_tier2_publications_institute_rank['rank'].dropna(), bins=6, range=[0, 600])
        c_heights, c_bins = np.histogram(df_tier3_publications_institute_rank['rank'].dropna(), bins=6, range=[0, 600])

        a_percent = []
        b_percent = []
        c_percent = []

        for i in range(len(a_heights)):
            total_value = a_heights[i] + b_heights[i] + c_heights[i]
            a_percent.append(a_heights[i]/total_value)
            b_percent.append(b_heights[i]/total_value)
            c_percent.append(c_heights[i]/total_value)

        width = 100


        ax.set_title('Institution Rank vs Number of Publications for Different Tiers of Publication')
        ax.set_xlabel('Institution Rank (bin_width = 100)')
        ax.set_ylabel('Percentage of Publications (for each tier)')
        ax.bar(a_bins[:-1], a_percent, width=width, align='edge', label='Tier 1 venues')
        ax.bar(b_bins[:-1], b_percent, width=width, align='edge', label='Tier 2 venues', bottom=a_percent)
        ax.bar(c_bins[:-1], c_percent, width=width, align='edge', label='Tier 3 venues', bottom=[sum(x) for x in zip(a_percent, b_percent)])
        ax.legend()
        
        ax.set_xticks(a_bins)
        plt.savefig('q3b_image.png')

        return "This graph shows the spread of the publications across different instition ranks for different tiers of venues."

    def question4(self, conferences):
        # Reputation of Venues vs Career of Scientist
        # conferences comes in the form of [['sigmod','1'],...]
        pass
