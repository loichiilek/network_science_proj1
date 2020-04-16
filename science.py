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

    def question3(self, conferences):
        # Correlation of Prestige of Institutes and Authors who Publish in Premium Venues
        # conferences comes in the form of [['sigmod','1'],...]
        pass

    def question4(self, conferences):
        # Reputation of Venues vs Career of Scientist
        # conferences comes in the form of [['sigmod','1'],...]
        pass
