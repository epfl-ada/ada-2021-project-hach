""" Helpers module for the natural disasters notebook """

# imports

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# global variables

years = range(2016, 2021)

month_names = ['Jan','Feb','Mar','Apr','May','Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']

# helpers

def as_number(nb):
    """ Function to convert abbreviations to numbers"""
    if 'K' in nb:
        return float(nb.replace('K', '')) * 1000
    elif 'M' in nb:
        return float(nb.replace('M', '')) * 1000 * 1000
    elif 'B' in nb:
        return float(nb.replace('B', '')) * 1000 * 1000 * 1000
    
def M_K(x):
    """ Function to convert numbers into abbreviations"""
    x = round(x/1000)
    
    if x >= 1000 * 1000:
        x = round(x/(1000*1000), ndigits=1)
        x = str(x) + 'B'
        return x
    elif x >= 1000:
        x = round(x/1000)
        x = str(x) + 'M'
        return x
    return str(x) + 'K'

# plots

def plot_nb_events(df_det_skinned):
    """ Function to plot the nb of events per year """
    nb_events = []

    for year in years:
        nb_events.append(len(df_det_skinned[df_det_skinned['YEAR'] == year]))

    plt.bar(years, nb_events)
    plt.xlabel('Year')
    plt.ylabel('Number of extreme weather events')
    
def plot_event_types_frequency(df_det_skinned):
    """ Function to plot the nb of events per type for each year """
    for year in years:
        df_year = df_det_skinned[df_det_skinned['YEAR'] == year]
        df_events = df_year[['EVENT_TYPE']]
        df_events_count = df_events.apply(pd.value_counts)
        df_events_count.plot(kind='bar', figsize=(15,5))
        plt.title('Year %i' %year)
        
def plot_top_10_event_types(df_det_skinned):
    """ Function to plot the top 10 event types for each year """
    for year in years:
        df_year = df_det_skinned[df_det_skinned['YEAR'] == year]
        df_events = df_year[['EVENT_TYPE']]
        df_events_count = df_events.apply(pd.value_counts)
        df_events_count.sort_values(by='EVENT_TYPE') # Sort for later selection
        df_events_count[:10].plot(kind='bar', figsize=(10,5)) # Keep only the top 10
        plt.title('Year %i' %year)
        
def plot_damages(df_damages):
    """ Function to plot the total damages per month """
    damage = df_damages.unstack(level=0).plot(kind='bar', 
                                         subplots=True, 
                                         rot=0, 
                                         figsize=(10, 15), 
                                         layout=(5, 1), 
                                         sharey=True, 
                                         ylabel="Property damage in millions of $", 
                                         xlabel="Months")

    
    plt.xticks(range(0, 12), month_names)
    plt.tight_layout()
    
def plot_global_greta_sentiment_damages(mean_sentiment_score_global, mean_sentiment_score_greta, natural):
    """ Function to plot the comparison between the total damages per month and mean sentiment score of the world and greta """
    fig, ax = plt.subplots(3, figsize=(10,15))
    for i, year in enumerate(range(2018, 2021)):
        ax2 = ax[i].twinx()
        ax3 = ax[i].twinx()

        # Plotting language complexity lines
        #nat = ax2.plot(natural[year], color='purple', label='Natural events', alpha=0.5)
        nat = ax3.bar(x=range(1,13), height=natural[year], color='purple', label='Property damage caused by natural events', alpha=0.5)
        greta = ax2.plot(mean_sentiment_score_greta[year], color='green', label='Greta trend')
        global_ = ax[i].plot(mean_sentiment_score_global[year], color='red', label='Global trend')

        # Parameters for plotting
        ax[i].set_title(str(year))
        ax[i].legend(loc=(1.1,0.87))
        ax[i].tick_params(axis='y', which='both', direction='in')
        ax2.tick_params(axis='y', which='both', direction='in')
        ax3.tick_params(axis='y', which='both', width=0)
        ax3.axes.get_yaxis().set_ticks([])

        # Legends
        ax2.bar_label(nat, labels=natural[year].apply(lambda x : M_K(x)), rotation=0, weight='bold')
        ax[i].set_ylabel('Global sentiment', color='red')
        ax2.set_ylabel('Greta sentiment', color='green')
        ax2.legend(loc=(1.1,0.78))
        ax3.legend(loc=(1.1,0.7))
        plt.xticks(range(1, 13), month_names) 
        
def plot_global_trump_sentiment_damages(mean_sentiment_score_global, mean_sentiment_score_trump, natural):
    """ Function to plot the comparison between the total damages per month and mean sentiment score of the world and trump """
    fig, ax = plt.subplots(3, figsize=(10,15))
    for i, year in enumerate(range(2018, 2021)):
        ax2 = ax[i].twinx()
        ax3 = ax[i].twinx()

        # Plotting language complexity lines
        #nat = ax2.plot(natural[year], color='purple', label='Natural events', alpha=0.5)
        nat = ax3.bar(x=range(1,13), height=natural[year], color='purple', label='Property damage caused by natural events', alpha=0.5)
        greta = ax2.plot(mean_sentiment_score_trump[year], color='green', label='Trump trend')
        global_ = ax[i].plot(mean_sentiment_score_global[year], color='red', label='Global trend')

        # Parameters for plotting
        ax[i].set_title(str(year))
        ax[i].legend(loc=(1.1,0.87))
        ax[i].tick_params(axis='y', which='both', direction='in')
        ax2.tick_params(axis='y', which='both', direction='in')
        ax3.tick_params(axis='y', which='both', width=0)
        ax3.axes.get_yaxis().set_ticks([])

        # Legends
        ax2.bar_label(nat, labels=natural[year].apply(lambda x : M_K(x)), rotation=0, weight='bold')
        ax[i].set_ylabel('Global sentiment', color='red')
        ax2.set_ylabel('Trump sentiment', color='green')
        ax2.legend(loc=(1.1,0.78))
        ax3.legend(loc=(1.1,0.7))
        plt.xticks(range(1, 13), month_names)
        
        
def plot_greta_trump_sentiment_damages(mean_sentiment_score_greta, mean_sentiment_score_trump, natural):
    """ Function to plot the comparison between the total damages per month and mean sentiment score of greta and trump quotes"""
    fig, ax = plt.subplots(3, figsize=(10,15))

    for i, year in enumerate(range(2018, 2021)):
        ax2 = ax[i].twinx()

        # Plotting language complexity lines
        #nat = ax2.plot(natural[year], color='purple', label='Natural events', alpha=0.5)
        nat = ax2.bar(x=range(1,13), height=natural[year], color='purple', label='Property damage caused by natural events', alpha=0.5)
        greta = ax[i].plot(mean_sentiment_score_greta[year], color='green', label='Greta trend')
        trump = ax[i].plot(mean_sentiment_score_trump[year], color='red', label='Trump trend')

        # Parameters for plotting
        ax[i].set_title(str(year))
        ax[i].legend(loc=(1.1,0.87))
        ax[i].tick_params(axis='y', which='both', direction='in')
        #ax2.tick_params(axis='y', which='both', direction='in')
        ax2.tick_params(axis='y', which='both', width=0)
        ax2.axes.get_yaxis().set_ticks([])

        # Legends
        ax2.bar_label(nat, labels=natural[year].apply(lambda x : M_K(x)), rotation=0, weight='bold')
        ax[i].set_ylabel('Trump and Greta sentiment')
        #ax2.set_ylabel('Trump sentiment', color='green')
        ax2.legend(loc=(1.1,0.78))
        #ax3.legend(loc=(1.1,0.7))
        plt.xticks(range(1, 13), month_names)
        
def plot_damages_weighted_sentiment(damages_sum, scores_mean):
    """ Function to plot the comparison between the total damages per month and weighted sentiment of climate change related quotes"""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add curves
    fig.add_trace(
        go.Bar(
            x=damages_sum.date, 
            y=damages_sum.DAMAGE_PROPERTY, 
            text=damages_sum.DAMAGE_PROPERTY.apply(M_K), 
            marker_color='pink',
            name="Damages"
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=scores_mean.date, 
            y=scores_mean.weighted_sentiment, 
            line={"color": "black"},
            name="Weighted sentiment"
        ),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Weighted sentiment related to damages from extreme weather events (monthly average)",

    )

    # Set x-axis title
    fig.update_xaxes(
        title_text="Date",
        range=["2018-12-15","2020-01-15"],
        tickformat="%b\n%Y",
        dtick="M1",
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="Damages", range=[0, 3e9], secondary_y=False, visible=False)
    fig.update_yaxes(title_text="Weighted sentiment", secondary_y=True, side="left", range=[0.4,1])

    fig.show()
    fig.write_html('plots/damages_weighted_sentiment.html', include_plotlyjs='cdn')
    
def plot_damages_weighted_sentiment_greta_trump(damages_sum, greta_scores_mean, trump_scores_mean):
    """ Function to plot the comparison between the total damages per month and weighted sentiment of greta and trump quotes"""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add curves
    fig.add_trace(
        go.Bar(
            x=damages_sum.date, 
            y=damages_sum.DAMAGE_PROPERTY,
            text=damages_sum.DAMAGE_PROPERTY.apply(M_K),
            marker_color='pink',
            showlegend=True,
            name="Damages",
        ),
    )

    fig.add_trace(
        go.Scatter(x=trump_scores_mean.date, y=trump_scores_mean.weighted_sentiment, name="Trump"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=greta_scores_mean.date, y=greta_scores_mean.weighted_sentiment, name="Greta", line={"color": "blue"}),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Greta vs Trump weighted sentiment related to damages (monthly average)",
    )

    # Set x-axis title
    fig.update_xaxes(
        title_text="Date",
        range=["2018-12-15","2020-01-15"],
        tickformat="%b\n%Y",
        dtick="M1",
    )

    # Set y-axes 

    fig.update_yaxes(title_text="Weighted sentiment", secondary_y=True, side="left", range=[-10,15])
    fig.update_yaxes(
        title_text="Damages",
        range=[0, 3e9],
        secondary_y=False,
        visible= False,
    )

    fig.show()
    fig.write_html('plots/damages_weighted_sentiment_greta_trump.html', include_plotlyjs='cdn')
    