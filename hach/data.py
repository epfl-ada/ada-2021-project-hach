import os
import pandas as pd
from text_analysis import *


def _extract_quotes_in_year(reg_query, year):
    # init chunk reader
    df_reader = pd.read_json(f'data/quotebank/quotes-{year}.json.bz2', lines=True, compression='bz2', chunksize = 100000)
    
    # query each chunk
    dfs = []
    for chunk in df_reader:
        df = chunk[chunk.quotation.str.contains(reg_query, case=False, na=False)]
        dfs.append(df)
        
    # combine dfs into one
    related_df = pd.concat(dfs)
    
    # write to pickle
    related_df.to_pickle(f'data/climate_df_{year}.pkl')

def extract_related_quotes(words, years):
    # make regex query from words
    reg_query = "|".join(words)
    # get related quotes for asked years
    for year in years:
        _extract_quotes_in_year(reg_query, year)
        
        
def get_climate_data(years=[2017,2018,2019,2020]):
    dfs = {}
    full_df = pd.DataFrame()
    for year in years:
        df = pd.read_pickle(f"data/climate_df_{year}.pkl")
        dfs[year] = df
        full_df = full_df.append(df)
        
    return full_df, dfs
    

def extract_wiki_speakers(full_climate_df):
    
    # load wiki data (huge)
    wiki_data = pd.read_parquet('parquet-data/speaker_attributes.parquet')
    
    # load the labels for wiki data
    wiki_labels = pd.read_csv('data/wikidata_labels_descriptions_quotebank.csv.bz2', compression='bz2', index_col='QID')
    
    # get speaker ids of the whole climate change quotes dataset
    wiki_speakers = pd.DataFrame(columns=wiki_data.columns)
    speakers_ids = full_climate_df.qids.apply(lambda x: x[0]).unique().tolist()
    wiki_data = wiki_data.set_index(wiki_data.id)
    
    for i in speakers_ids:
        if i in wiki_data.index:
            wiki_speakers = wiki_speakers.append(wiki_data.loc[i])
            
    wiki_speakers = wiki_speakers.drop_duplicates('id')
    
    # write the wiki data to pickle
    wiki_speakers.to_pickle('data/wiki_speakers.pkl')
    
    return wiki_data, wiki_labels, wiki_speakers
    
    
def exctract_speakers(climate_dfs, wiki_speakers, wiki_labels):
    
    for i in range(2017, 2021):
        speakers_df = get_attributes(climate_dfs[i], wiki_speakers, wiki_labels)
        speakers_df.to_pickle('data/speakers_{}.pkl'.format(i))
