import os
import pandas as pd


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
    
    
    
