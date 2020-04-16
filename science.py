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
        
        # ideally check if authors.csv exist already.
        authors_df = pd.read_csv('authors.csv')

        # list of tier 1 conferences
        tier_1 = []
        for conf, tier in conferences:
            if tier == '1':
                tier_1.append(conf)

        # get df with each conference and its network centrality score
        conf_df = self.get_conf_prestige()

        # create df that will be used to count how many authors have published to tier 1 conferences
        tier1_authors_df = authors_df[authors_df.conf.isin(tier_1)].drop(columns=['name', 'year', 'conf']).drop_duplicates()
        tier1_authors_df['published_in_t1'] = True

        # calculate prestige scores of each author by summing
        temp_df = authors_df.sort_values(by=['pid'])
        temp_df = temp_df.drop(columns=['name', 'year'])
        temp_df = temp_df.set_index('conf').join(conf_df.set_index('conference'))
        grouped = temp_df.groupby(['pid']).sum()

        del temp_df

        locations_df = pd.read_csv('author_aff_rank_distance.csv')
        joined = authors_df.set_index('pid').join(locations_df.set_index('pid'))

        del authors_df, locations_df

        df = joined.loc[~joined.index.duplicated()]
        df = df.join(grouped)
        df = df.join(tier1_authors_df.set_index('pid'))

        del joined, tier1_authors_df

        # now plot some graphs comparing the % of people in each quartile of the distance to top ten and their spread of prestige
        # expect there to be no correlation
        _, _, _, _, quantile25, quantile50, quantile75, _ = df['Distance to Top Ten'].describe()
        df['distance_tier'] = 0
        df.loc[df['Distance to Top Ten'] <= quantile25, 'distance_tier'] = 'min to Q1'
        df.loc[df['Distance to Top Ten'].between(quantile25, quantile50), 'distance_tier'] = 'Q1 to Q2'
        df.loc[df['Distance to Top Ten'].between(quantile50, quantile75), 'distance_tier'] = 'Q2 to Q3'
        df.loc[df['Distance to Top Ten'] >= quantile75, 'distance_tier'] = 'Q3 to max'

        sns_plot = sns.boxplot(
            y='prestige', x='distance_tier', data=df,
            order=['min to Q1', 'Q1 to Q2', 'Q2 to Q3', 'Q3 to max'],
            showfliers=False)
        sns_plot.set(ylabel='Prestige Score', xlabel='Distance to Top 10 Institutes - Inter Quartile Range')
        sns_plot.get_figure().savefig('q2_image.png')

        # extra analysis: probability that an author has published to t1 conference before given distance quartile
        prob_published_t1 = []
        for iqr in ['min to Q1', 'Q1 to Q2', 'Q2 to Q3', 'Q3 to max']:
            t1 = len(df[(df.distance_tier == iqr) & df.published_in_t1.notna()])
            total = len(df[df.distance_tier == iqr])
            prob_published_t1.append(t1 / total)

        # TODO need to return a string that details my analysis.
        return 'Q2 analysis: 420blazeit'

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

        a_percent = [i/sum(a_heights)*100 for i in a_heights]
        b_percent = [i/sum(b_heights)*100 for i in b_heights]
        c_percent = [i/sum(c_heights)*100 for i in c_heights]
        width = (a_bins[1] - a_bins[0])/3


        ax.set_title('Institution Rank vs Percentage of Publications in Different Tiers of Publication')
        ax.set_xlabel('Institution Rank (bin_width = 100)')
        ax.set_ylabel('Percentage of Publications')
        ax.bar(a_bins[:-1], a_percent, width=width, align='edge', label='Tier 1 venues')
        ax.bar(b_bins[:-1]+width, b_percent, width=width, align='edge', label='Tier 2 venues')
        ax.bar(c_bins[:-1]+2*width, c_percent, width=width, align='edge', label='Tier 3 venues')
        ax.legend()
        
        ax.set_xticks(a_bins)
        plt.savefig('q3b_image.png')

        return "This graph shows the spread of the publications across different instition ranks for different tiers of venues."

    def question4(self, conferences):
        # Reputation of Venues vs Career of Scientist
        # conferences comes in the form of [['sigmod','1'],...]
        pass
