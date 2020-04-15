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
        # df_tier1_authors_institute_rank.hist(bins=[0,100,200,300,400,500,600])

        # tier2
        df_tier2 = df_authors[df_authors['conf'].isin(tier2)]
        df_tier2.drop_duplicates(subset ="pid", keep = "first", inplace = True)
        df_tier2_authors_institute_rank = df_institutes[df_institutes['pid'].isin(df_tier2.pid.unique())].drop(['affiliation', 'latitude', "longitude", "Distance to Top Ten"], axis=1)
        # df_tier2_authors_institute_rank.hist(bins=[0,100,200,300,400,500,600])

        # tier3
        df_tier3 = df_authors[df_authors['conf'].isin(tier3)]
        df_tier3.drop_duplicates(subset ="pid", keep = "first", inplace = True)
        df_tier3_authors_institute_rank = df_institutes[df_institutes['pid'].isin(df_tier3.pid.unique())].drop(['affiliation', 'latitude', "longitude", "Distance to Top Ten"], axis=1)
        # df_tier3_authors_institute_rank.hist(bins=[0,100,200,300,400,500,600], alpha=0.5)

        fig, ax = plt.subplots()

        # plt.hist(data, bins=6, range=[0, 600], histtype='step')
        a_heights, a_bins = np.histogram(df_tier1_authors_institute_rank['rank'].dropna(), bins=6, range=[0, 600])
        b_heights, b_bins = np.histogram(df_tier2_authors_institute_rank['rank'].dropna(), bins=6, range=[0, 600])
        c_heights, c_bins = np.histogram(df_tier3_authors_institute_rank['rank'].dropna(), bins=6, range=[0, 600])

        width = (a_bins[1] - a_bins[0])/3

        print(a_bins)
        ax.set_title('Institution Rank Frequency for Different Tiers of Publication')
        ax.set_xlabel('Institution Rank (bin_width = 100)')
        ax.set_ylabel('Frequency')
        ax.bar(a_bins[:-1], a_heights, width=width, align='edge', label='Tier 1 venues')
        ax.bar(b_bins[:-1]+width, b_heights, width=width, align='edge', label='Tier 2 venues')
        ax.bar(c_bins[:-1]+2*width, c_heights, width=width, align='edge', label='Tier 3 venues')
        ax.legend()
        
        ax.set_xticks(a_bins)
        plt.savefig('q3_image.png')

        return "This is the analysis of this particular graph. I cannot tell."

    def question3b(self, conferences):
        # I have two parts, still doing second half.
        pass

    def question4(self, conferences):
        # Reputation of Venues vs Career of Scientist
        # conferences comes in the form of [['sigmod','1'],...]
        pass
