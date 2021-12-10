import pandas as pd
import textstat
from flair.models import TextClassifier
from flair.data import Sentence
import seaborn as sns
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def get_sentiment_score(text, classifier): 
    """Function to get sentiment of a quote using the flair library"""

    sentence = Sentence(text)
    classifier.predict(sentence)
    return sentence.labels

def sentiment_mapping(df): 
    """Function mapping the sentiment to a sentiment score, where negative sentiments map to negative values"""
    
    df['sentiment_score'] = df.sentiment.apply(lambda x: float(str(x)[11:-2]) if str(x)[1] == 'P' else -float(str(x)[11:-2]))
    
    
def get_quote_complexity(text):
    """Function computing the language complexity of a quote base on the textstat library"""
    
    return textstat.text_standard(text, float_output=True)

def month_mapping(df): 
    """Function creating a new month column based on the quote ID"""
    
    df['month'] = df.quoteID.str.slice(start= 5, stop=7)
    
def plot_months(df, title): 
    """Function plotting the number of quotes per month"""
    
    #Plotting the number of quotes per month
    df.groupby('month')['quoteID'].count().plot(kind='bar', title=title)
    
def plot_wordcloud(df, title_text): 
    """Function plotting wordcloud of quotes in a dataframe"""
    
    #Wordcloud for the specific dataframe
    text = "".join(quote for quote in df.quotation)
    wordcloud = WordCloud( background_color="white").generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title_text)
    plt.axis("off")
    plt.show()

def plot_sentiment_months(df):
    """Function plotting the average sentiment of quotes for each month"""
    
    #Plotting the mean sentiment score of each month
    sentiment_monthly = df.groupby('month')['sentiment_score'].mean()
    fig = sns.lineplot(data=sentiment_monthly , x=sentiment_monthly.index, y=sentiment_monthly.values, legend='brief')
    fig.set(xlabel='month', ylabel='mean sentiment score', title='mean monthly sentiment score')
    
    
def plot_top_parties(df):
    """Function to plot complexity and sentiment of top 10 parties in df"""
    
    top_10_parties = df.groupby('political_party')['quoteID'].count().sort_values(ascending=False).head(10).to_frame()
    data = df[df['political_party'].apply(lambda x: x in top_10_parties.index)]
    average_complexity = data.groupby('political_party')['complexity'].mean().round(2)
    average_sentiment = data.groupby('political_party')['sentiment_score'].mean().round(2)

    fig = sns.pointplot(x=average_complexity, y=average_sentiment, hue=top_10_parties.index)
    plt.xticks(rotation=70)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    fig.set(xlabel='average complexity', ylabel='average sentiment')   
    plt.show()
     
def plot_complexity_evolution(df, title_text):
    """Function to plot average complexity """
    
    month_mapping(df)
    monthly_average = df.groupby('month')['complexity'].mean().round(2)
    fig = sns.lineplot(x=monthly_average.index, y= monthly_average.values)
    fig.set(ylabel='average quote complexity')  
    plt.title(title_text)

    
def plot_sentiment_evolution(df, title_text):
    """Function to plot average sentiment """
    
    month_mapping(df)
    monthly_average = df.groupby('month')['sentiment_score'].mean().round(2)
    fig = sns.lineplot(x=monthly_average.index, y= monthly_average.values)
    fig.set(ylabel='average quote sentiment')  
    plt.title(title_text)

def plot_comparison_sentiment(dfs, title_text, labels):
    """Function to compare language sentiment of two sets over time"""
    
    monthly_average= {}
    
    for i in range(1, 3):
        month_mapping(dfs[i])
        monthly_average[i] = dfs[i].groupby('month')['sentiment_score'].mean().round(2)
        fig = sns.lineplot(x=monthly_average[i].index, y= monthly_average[i].values)
                      
    fig.set(ylabel='average quote sentiment') 
    plt.legend(labels=labels)
    plt.title(title_text)
    plt.show()

         
def plot_comparison_complexity(dfs, title_text, labels): 
    """Function to compare language sentiment of two sets over time"""
    
    monthly_average= {}
    
    for i in range(1, 3):
        month_mapping(dfs[i])
        monthly_average[i] = dfs[i].groupby('month')['complexity'].mean().round(2)
        fig = sns.lineplot(x=monthly_average[i].index, y= monthly_average[i].values)
        
    fig.set(ylabel='average quote complexity')  
    plt.title(title_text)
    plt.legend(labels=labels)
    plt.show()