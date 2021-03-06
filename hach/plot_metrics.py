""" Module with plotting functions """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from .metrics import *
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_top_speakers(df, n):
    """Function plotting top n speakers for all years"""
    
    fig, ax = plt.subplots(4, figsize=(20,20), sharey=True)
    
    for year in range(2017, 2021):
        i = (year-2017)
        
        top_speakers_i = top_speakers(df[year], n)
        
        ax[i].set_title('Top speakers in {}'.format(year))
        sns.barplot(ax = ax[i], x=top_speakers_i.speaker, y=top_speakers_i.quotation_count)
        
    plt.show()


def plot_gender(speakers, plotly=False):
    """Function plotting the gender proportion pie charts"""

    if plotly:
        
        specs = [[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]]
        fig = make_subplots(rows=2, cols=2, specs=specs, subplot_titles=['2017', '2018', '2019', '2020'])
        
        for year in range(2017, 2021):
            i = year - 2017 + 1
            
            nb_men = speakers[year][speakers[year].gender == 'male'].speaker.count()
            nb_women = speakers[year][speakers[year].gender == 'female'].speaker.count()
            
            labels = ['men', 'women']
            values= [nb_men, nb_women]
            row = math.floor(i/3)+1
            col = 2-(i%2)
        
            fig.add_trace(go.Pie(labels=labels, values= values), row, col)
        
        fig.update_layout(title = {
         'text': "Climate speakers gender between 2017 and 2020",
         'x':0.5,
         'xanchor': 'center',
         'yanchor': 'top'})
        fig.write_html('plots/gender_piecharts.html', include_plotlyjs='cdn')
        fig.show()
        
    
    else:
        fig, axs = plt.subplots(2, 2, figsize=(12,12))
        for year in range(2017, 2021):
            i = year - 2017 + 1

            #gender_count = all_speakers[year].groupby('gender').speaker.count().reset_index(drop=False)
            nb_men = speakers[year][speakers[year].gender == 'male'].speaker.count()
            nb_women = speakers[year][speakers[year].gender == 'female'].speaker.count()

            axs[math.floor(i/3)][1-(i%2)].set_title('{}'.format(year))
            axs[math.floor(i/3)][1-(i%2)].pie([nb_men, nb_women], labels=['men', 'women'], autopct='%1.0f%%')

        plt.savefig('plots/gender.png')
        plt.show()      
    
    
    
def plot_age(speakers, plotly=False):
    """Function plotting the age of speakers"""
    
    if plotly:
        all_speakers = get_speakers_by_year(speakers)    
    
        fig = px.histogram(all_speakers, x='age', animation_frame='year', nbins=100, histnorm="percent")
        fig.update_layout(title = {
         'text': "Age distribution of climate speakers",
         'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
        
        fig.write_html('plots/age_plot.html', include_plotlyjs='cdn')
        fig.show()
    else:
        fig, axs = plt.subplots(2, 2, figsize=(16,14), sharey=True)
        for year in range(2017, 2021):
            i = (year - 2017) + 1

            axs[math.floor(i/3)][1-(i%2)].set_title('Age of speakers in {}'.format(year))
            axs[math.floor(i/3)][1-(i%2)].hist(speakers[year].age, density=True)
    


def top_count(df, attribute, threshold):
    """Helper function for plotting the attribute pie charts (for nationality and political party)"""
    
    count = df.groupby(attribute).speaker.count().to_frame()
    count = count.sort_values(by='speaker', ascending=False)
    total_count = count.speaker.sum()
    
    # we show the top countries/political parties 
    if attribute == 'political_party':
        # for political parties we choose to show only the parties that represent over 5% of all
        best_count = count[(count.speaker/total_count) >= threshold]
    else:
        best_count = count.head(5)
    # group all the other countries/political parties
    others_count = count.drop(best_count.index).speaker.sum()
    others = pd.DataFrame([others_count], index=['Others'], columns=['speaker'])
    
    top_count = best_count.append(others)
    
    return top_count


def plot_nationality_charts(speakers, attribute='nationality', plotly=False):
    """Function plotting the nationalty proportion pie charts"""    
   
    if plotly:
        specs = [[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]]
        fig = make_subplots(rows=2, cols=2, specs=specs, subplot_titles=['2017', '2018', '2019', '2020'])
        
        for year in range(2017, 2021):
            i = year - 2017 + 1
            
            nationality_count_i = top_count(speakers[year], attribute, 0.01)
            countries = nationality_count_i.index.tolist()
            
            row = math.floor(i/3)+1
            col = 2-(i%2)
        
            fig.add_trace(go.Pie(labels=countries, values= nationality_count_i.speaker.tolist()), row, col)
        
        fig.update_layout(title='Climate speakers nationality distribution between 2017 and 2020', height=500, width=600)
        fig.write_html('plots/nationality_plot.html', include_plotlyjs='cdn')
        fig.show()
    
    else:
        # plot pie charts
        fig, axs = plt.subplots(2, 2, figsize=(12,10))

        #fig.suptitle('Nationality proportion of climate speakers per year')
        for year in range(2017, 2021):
            i = (year - 2017)+1

            nationality_count_i = top_count(speakers[year], attribute, 0.05)
            countries = nationality_count_i.index.tolist()

            axs[math.floor(i/3)][1-(i%2)].set_title('{}'.format(year))
            wedges, texts, autotexts = axs[math.floor(i/3)][1-(i%2)].pie(nationality_count_i.speaker.tolist(), labels = countries, autopct='%1.0f%%')

            plt.setp(autotexts, size=10, weight="bold", color='w')
            plt.setp(texts, size=10)

            plt.savefig('plots/nationality_charts.png')

        plt.show()

    
def plot_party(speakers, country, threshold):
    """Function plotting the political party proportion pie chart for a country"""
    
    fig, axs = plt.subplots(2, 2, figsize=(12,10))
    
    #fig.suptitle('Biggest political parties of climate speakers per year')
    for year in range(2017, 2021):
        i = (year - 2017)+1
        
        party_count_i = top_count(speakers[year][speakers[year]['nationality'] == country], 'political_party', threshold)
        political_parties = party_count_i.index.tolist()
        
        axs[math.floor(i/3)][1-(i%2)].set_title('{}'.format(year))
        wedges, texts, autotexts = axs[math.floor(i/3)][1-(i%2)].pie(party_count_i.speaker.tolist(), labels = political_parties, autopct='%1.0f%%')
    
        plt.setp(autotexts, size=10, weight="bold", color='w')
        plt.setp(texts, size=10)
        
        plt.savefig('plots/political_party_charts.png')
        
    plt.show()

########################################################
# 'Age and gender vs complexity and sentiment' functions
########################################################
    
def plot_age_complexity(dfs):
    """Function plotting age vs language complexity"""
    
    for year in range(2017, 2021):
        i = (year - 2017)+1
        
        age_complexity_i = dfs[year][['age', 'complexity']]
        age_complexity_i = age_complexity_i[~age_complexity_i.age.isna()]
        age_complexity_mean_i = age_complexity_i.groupby('age').mean().reset_index(drop=False)

        p = sns.jointplot(x=age_complexity_mean_i.age, y=age_complexity_mean_i.complexity, kind='hex')
        p.fig.suptitle("Age x complexity in {}".format(year))
        p.fig.tight_layout()

        
    plt.show()
    
def plot_age_sentiment(dfs):
    """Function plotting age vs sentiment score"""
    
    for year in range(2017, 2021):
        i = (year - 2017)+1
        
        age_sentiment_i = dfs[year][['age', 'sentiment_score']]
        age_sentiment_i = age_sentiment_i[~age_sentiment_i.age.isna()]
        age_sentiment_mean_i = age_sentiment_i.groupby('age').mean().reset_index(drop=False)

        p = sns.jointplot(x=age_sentiment_mean_i.age, y=age_sentiment_mean_i.sentiment_score, kind='hex', color='orange')
        p.fig.suptitle("Age x sentiment score in {}".format(year))
        p.fig.tight_layout()
        
    plt.show()
    
    
def gender_speach(dfs):
    """Function creating a df with mean language complexity and sentiment score per gender"""
    
    for year in range(2017, 2021):
        i = (year - 2017)+1
        
        gender_text_i = dfs[year][['gender', 'complexity', 'sentiment_score']]
        gender_text_i = gender_text_i[~gender_text_i.gender.isna()]
        gender_text_mean_i = gender_text_i.groupby('gender').mean()
        gender_text_mean_i = gender_text_mean_i.loc[['male', 'female']].reset_index(drop=False)
        gender_text_mean_i['year'] = year
        
        if i == 1:
            gender_complexity_sentiment = gender_text_mean_i
        else:
            gender_complexity_sentiment = gender_complexity_sentiment.append(gender_text_mean_i)
            
    return gender_complexity_sentiment.reset_index(drop=True)

def plot_gender_speach(dfs):
    """Function plotting the change in language complexity and sentiment score for men and women"""
    
    gender_speach_df = gender_speach(dfs)
    
    men_speach_df = gender_speach_df[gender_speach_df.gender == 'male']
    women_speach_df = gender_speach_df[gender_speach_df.gender == 'female']
        
    fig1 = sns.lineplot(x=men_speach_df.year, y = men_speach_df.complexity, color='blue', label='men')
    fig1 = sns.lineplot(x=women_speach_df.year, y = women_speach_df.complexity, color='orange', label='women')
    plt.title('Gender x complexity')
    plt.legend()
    
    plt.savefig('plots/gender_x_complexity.png')
    plt.show()
    
    fig2 = sns.lineplot(x=men_speach_df.year, y = men_speach_df.sentiment_score, color='blue', label='men')
    fig2 = sns.lineplot(x=women_speach_df.year, y = women_speach_df.sentiment_score, color='orange', label='women')  
    plt.title('Gender x sentiment score')
    plt.legend()
    
    plt.savefig('plots/gender_x_sentiment.png')
    plt.show()

