import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from .metrics import *

def plot_top_speakers(df, n):
    """Function plotting top n speakers for all years"""
    
    fig, ax = plt.subplots(4, figsize=(20,20), sharey=True)
    
    for year in range(2017, 2021):
        i = (year-2017)
        
        top_speakers_i = top_speakers(df[year], n)
        
        ax[i].set_title('Top speakers in {}'.format(year))
        sns.barplot(ax = ax[i], x=top_speakers_i.speaker, y=top_speakers_i.quotation_count)
        
    plt.show()


def plot_gender(speakers):
    """Function plotting the gender proportion pie charts"""
    
    # plot
    fig, axs = plt.subplots(1, 4, figsize=(14,6))
    
    for year in range(2017, 2021):
        i = year - 2017
        
        #gender_count = speakers[year].groupby('gender').speaker.count().reset_index(drop=False)
        nb_men = speakers[year][speakers[year].gender == 'male'].speaker.count()
        nb_women = speakers[year][speakers[year].gender == 'female'].speaker.count()
        
        axs[i].set_title('Gender of speakers {}'.format(year))
        axs[i].pie([nb_men, nb_women], labels=['men', 'women'], autopct='%1.0f%%')
        
    plt.show()
    
    
def plot_age(speakers):
    """Function plotting the age of speakers"""
    
    fig, axs = plt.subplots(2, 2, figsize=(16,14), sharey=True)
    for year in range(2017, 2021):
        i = (year - 2017) + 1
        
        axs[math.floor(i/3)][1-(i%2)].set_title('Age of speakers in {}'.format(year))
        sns.histplot(speakers[year]['age'], ax = axs[math.floor(i/3)][1-(i%2)], kde=True)
        
    plt.show()


def top_count(df, attribute):
    """Helper function for plotting the attribute pie charts (for nationality and political party)"""
    
    count = df.groupby(attribute).speaker.count().to_frame()
    count = count.sort_values(by='speaker', ascending=False)
    total_count = count.speaker.sum()
    
    # we show the top countries/political parties 
    if attribute == 'political_party':
        # for political parties we choose to show only the parties that represent over 5% of all
        threshold = 0.05
        best_count = count[(count.speaker/total_count) >= threshold]
    else:
        best_count = count.head(5)
    # group all the other countries/political parties
    others_count = count.drop(best_count.index).speaker.sum()
    others = pd.DataFrame([others_count], index=['Others'], columns=['speaker'])
    
    top_count = best_count.append(others)
    
    return top_count


def plot_nationality_charts(speakers, attribute='nationality'):
    """Function plotting the nationalty proportion pie charts"""    

    # plot pie charts
    fig, axs = plt.subplots(2, 2, figsize=(12,10))
    
    fig.suptitle('Nationality proportion of climate speakers per year')
    for year in range(2017, 2021):
        i = (year - 2017)+1
        
        nationality_count_i = top_count(speakers[year], attribute)
        countries = nationality_count_i.index.tolist()
        
        axs[math.floor(i/3)][1-(i%2)].set_title('{}'.format(year))
        wedges, texts, autotexts = axs[math.floor(i/3)][1-(i%2)].pie(nationality_count_i.speaker.tolist(), labels = countries, autopct='%1.0f%%')
    
        plt.setp(autotexts, size=10, weight="bold", color='w')
        plt.setp(texts, size=10)
        
    plt.show()

    
def plot_party(speakers, country):
    """Function plotting the political party proportion pie chart for a country"""
    
    fig, axs = plt.subplots(2, 2, figsize=(12,10))
    
    fig.suptitle('Biggest political parties of climate speakers per year')
    for year in range(2017, 2021):
        i = (year - 2017)+1
        
        party_count_i = top_count(speakers[year][speakers[year]['nationality'] == country], 'political_party')
        political_parties = party_count_i.index.tolist()
        
        axs[math.floor(i/3)][1-(i%2)].set_title('{}'.format(year))
        wedges, texts, autotexts = axs[math.floor(i/3)][1-(i%2)].pie(party_count_i.speaker.tolist(), labels = political_parties, autopct='%1.0f%%')
    
        plt.setp(autotexts, size=10, weight="bold", color='w')
        plt.setp(texts, size=10)
        
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

        sns.jointplot(x=age_complexity_mean_i.age, y=age_complexity_mean_i.complexity, kind='hex')
        
    plt.show()
    
def plot_age_sentiment(dfs):
    """Function plotting age vs sentiment score"""
    
    for year in range(2017, 2021):
        i = (year - 2017)+1
        
        age_sentiment_i = dfs[year][['age', 'sentiment_score']]
        age_sentiment_i = age_sentiment_i[~age_sentiment_i.age.isna()]
        age_sentiment_mean_i = age_sentiment_i.groupby('age').mean().reset_index(drop=False)

        sns.jointplot(x=age_sentiment_mean_i.age, y=age_sentiment_mean_i.sentiment_score, kind='hex', color='orange')
        
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
    plt.show()
    
    fig2 = sns.lineplot(x=men_speach_df.year, y = men_speach_df.sentiment_score, color='blue', label='men')
    fig2 = sns.lineplot(x=women_speach_df.year, y = women_speach_df.sentiment_score, color='orange', label='women')  
    plt.title('Gender x sentiment score')
    plt.legend()
    plt.show()

