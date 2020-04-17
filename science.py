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
        prestige = self.network.getVenuePrestigefromNetwork()
        conference = []
        eigenvector_centrality = []
        
        for key,value in prestige.items():
            conference.append(key)
            eigenvector_centrality.append(value)
        d = {'conference': conference, 'eigenvector_centrality': eigenvector_centrality}
        df =  pd.DataFrame.from_dict(d)
        df = df.sort_values('eigenvector_centrality', ascending = False)
        
        
        tier = [0,0,0]

        for i in conferences:
            if i[1] == '1':
                tier[0] += 1
            elif i[1] == '2':
                tier[1] += 1
            else:
                tier[2] += 1

        count = 0
        newtierlist = []
        
        #barplot 
        plt.figure(figsize=(8, 6))
        current_palette = sns.color_palette()        
        sns_plot = sns.barplot(x="eigenvector_centrality", y="conference", data=df)
        sns_plot.set(ylabel='Conference', xlabel='Eigenvector Centrality')
        for bar in sns_plot.patches:
            if count < tier[0]:
                bar.set_color(current_palette[0])
                count += 1
            elif count < tier[0]+tier[1]:
                bar.set_color(current_palette[1])
                count += 1
            else:
                bar.set_color(current_palette[2])

        sns_plot.set_title('Eigenvector Centrality of Conferences (Ordered)')
        sns_plot.get_figure().savefig('q1_image.png')
        
        # extra analysis: accuracy of new tierlist
        count2 = 0
        newtierlist = {}
        for i in range(len(df.index)):
            if count2 < tier[0]:
                newtierlist[df['conference'].iloc[i]] = '1'
                count2 += 1
            elif count < tier[0]+tier[1]:
                newtierlist[df['conference'].iloc[i]] = '2'  
                count2 += 1
            else:
                newtierlist[df['conference'].iloc[i]] = '3'
                count2 += 1
                
        
        

        tldict = {}
        for i in conferences:
            tldict[i[0]] = i[1]
            
        sum = 0
        for key,value in tldict.items():
            if newtierlist[key] == value:
                sum += 1
        
        accuracy = str(round(sum/len(newtierlist)*100, 2))
        
        string = "Using eigenvector centrality, the network graph has an accuracy of " + accuracy + " as compared to the given tierlist."
        
        plt.clf()
        return string

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
        conf_dict = self.network.getVenuePrestigefromNetwork()
        # conf_df = pd.DataFrame.from_dict(conf_dict, orient='index', columns=['conference', 'prestige'])
        conf_list = []
        for key, value in conf_dict.items():
            conf_list.append([key, value])
        conf_df = pd.DataFrame(conf_list, columns=['conference', 'prestige'])

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

        plt.figure(figsize=(8, 6))
        sns_plot = sns.boxplot(
            y='prestige', x='distance_tier', data=df,
            order=['min to Q1', 'Q1 to Q2', 'Q2 to Q3', 'Q3 to max'],
            showfliers=False)
        sns_plot.set(ylabel='Prestige Score', xlabel="Distance to Top 10 Institutes - Inter Quartile Range")
        sns_plot.get_figure().savefig('q2_image.png')

        # extra analysis: probability that an author has published to t1 conference before given distance quartile
        prob_published_t1 = []
        for iqr in ['min to Q1', 'Q1 to Q2', 'Q2 to Q3', 'Q3 to max']:
            t1 = len(df[(df.distance_tier == iqr) & df.published_in_t1.notna()])
            total = len(df[df.distance_tier == iqr])
            prob_published_t1.append(t1 / total)
        
        plt.clf()

        return f"This graph shows the relationship between the distance of an author's institute to one of the Top Ten institutes, and the author's prestige. The authors are split into 4 buckets based on the distance. The buckets correspond to the quartiles of the distribution of the available distances. Based on the relative distribution of author prestige in each bucket, the graph can potentially show a relationship (or lack thereof) between author prestige and distance of author's institute to the Top Ten institutions. The following numbers denote the probability that an author from each of the distance buckets have published at least once in a tier 1 conference: {prob_published_t1}"

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

        fig, ax = plt.subplots(figsize=(8, 6))

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
        
        plt.clf()

        return "This graph shows the percentage of unique authors in each institution ranking bin for the 3 different tiers. The x-axis denotes the bins of the institution rankings with intervals of 100 and the y-axis denotes the percentage of authors that published in this particular ranking bin. In this graph, we aim to investigate if there is a relationship between the number of unique author publishing from each of the ranking bins and the tier of the venue. If there is a higher proportion of authors coming from a certain ranking bins for a particular tier, the relationship we are investigating might exist."

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

        fig, ax = plt.subplots(figsize=(8, 6))

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
        
        plt.clf()

        return "This graph shows the percentage of publication from each of the 3 tiers for the different institution rankings. If there is no correlation between the ranking of the institution and the percentage of publication from the different tiers, the graph should show a consistent spread of percentages across the different institution rankings for all 3 tiers. Otherwise, if certain tier has higher proportion in certain institution ranking bin and lower in another, the relationship we are investigating might exist."

    def question4(self, conferences):
        # Reputation of Venues vs Career of Scientist
        # conferences comes in the form of [['sigmod','1'],...]
        
        df = self.network.get_authors_rep()
        low = np.quantile(df['initial'].tolist(),0.3)
        high = np.quantile(df['initial'].tolist(),0.7)
        
        maintainhigh = 0
        maintainlow = 0
        uprep = 0
        downrep = 0

        for i in range(len(df)):
            if df['initial'].iloc[i] < low and df['final'].iloc[i] < low:
                maintainlow+=1
            elif df['initial'].iloc[i] < low and df['final'].iloc[i] > high:
                uprep+=1
            elif df['initial'].iloc[i] > high and df['final'].iloc[i] > high:
                maintainhigh+=1
            elif df['initial'].iloc[i] > high and df['final'].iloc[i] < low:
                downrep+=1
        
        initial_low = np.sum(df['initial'] < low)
        initial_high = np.sum(df['initial'] > high)
        
        df['Authors'] = ''
        plt.figure(figsize=(8, 6))
        sns_plot = sns.scatterplot(x="initial", y="final",size= 'Authors', data=df)
        sns_plot.set(ylabel='Final Reputation', xlabel='Initial Reputation')
        sns_plot.set_title('Scatterplot of authors\' Initial Reputation to Final Reputation')
        sns_plot.get_figure().savefig('q4_image.png')
        
        rep_remain_high = str(round(maintainhigh/initial_high*100, 2))
        rep_remain_low = str(round(maintainlow/initial_low*100, 2))
        rep_down = str(round(downrep/initial_high*100, 2))
        rep_up = str(round(uprep/initial_low*100, 2))
        
        result = "Of the data scientists who had an initial high reputation, " + rep_remain_high + "% continued to have a high reputation while " + rep_down + "% ended up publishing in low-tier conferences. On the other hand, of the data scientists who had an initial low reputation, " + rep_remain_low + "% did not have much of a change in their reputation while " + rep_up + "% managed to publish in high-tiered conferences."
        
        plt.clf()
        return result
