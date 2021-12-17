# imports
import numpy as np
import pandas as pd
from datetime import datetime

#################
# Top_ funnctions
#################

def top_speakers(df, n):
    """Function to extract the top n speakers"""
    
    top_speakers = df.groupby('speaker')['quotation'].count().sort_values(ascending=False).to_frame().add_suffix('_count')
    top_speakers.reset_index(drop=False, inplace=True)
    
    return top_speakers.head(n)


def top_quotations(df, n):
    """Function to extract the top n most repeated quotations"""
    
    top_quotations = df.sort_values('numOccurrences', ascending=False)[['speaker', 'quotation', 'numOccurrences']]
    # remove quotations of unidentified speakers
    top_quotations.reset_index(drop=True, inplace=True)
    
    return top_quotations.head(n)


def get_quotes(speaker, df):
    """Function to get all the quotes for a speaker and classify them by its nb of occurrences"""
    
    quotes = df[df['speaker'] == speaker][['quotation', 'numOccurrences']]
    
    return quotes.sort_values(by='numOccurrences', ascending=False).reset_index(drop=True)

################################
# Extracting attribute functions
################################

def get_qids(name, df): 
    """Function giving the list of qids for a speaker from df"""
    
    ids = df[df.speaker == name].iloc[0].qids
    
    return ids

def get_gender(name, df, wiki_speakers, wiki_labels):
    """Function extracting the gender for a speaker"""
    
    ids = get_qids(name, df)
    
    if ids is None:
        gender = None
    else:
        if ids[0] not in wiki_speakers.index:
            gender = None
        else:
            gender_qids = wiki_speakers.loc[ids[0]]['gender']
            if gender_qids is None:
                gender = None
            else:
                qid = gender_qids[0]
                gender = wiki_labels.loc[qid]['Label']
    
    return gender

def get_age(name, df, wiki_speakers):
    """Function extracting the age of the speaker"""
    
    ids = get_qids(name, df)
    
    if ids is None:
        age = None
    else:
        if ids[0] not in wiki_speakers.index:
            age = None
        else:
            date_qid = wiki_speakers.loc[ids[0]]['date_of_birth']
            if date_qid is None:
                age = None
            else: 
                birth_date = date_qid[0]
                birth_year = birth_date[1:5]
                # @TODO: what about speakers already dead? -> check death date
                age = int(datetime.now().strftime('%Y')) - int(birth_year)
        
    return age


def get_nationality(name, df, wiki_speakers, wiki_labels):
    """Function extracting the nationality of the speakers"""
    
    ids = get_qids(name, df)
    
    if ids is None:
        nationality = None
    else:
        if ids[0] not in wiki_speakers.index:
            nationality = None
        else:
            country_qid = wiki_speakers.loc[ids[0]]['nationality']
            if country_qid is None:
                nationality = None
            else:
                qid = wiki_speakers.loc[ids[0]]['nationality'][0]
                nationality = wiki_labels.loc[qid]['Label']
    
    return nationality


def get_party(name, df, wiki_speakers, wiki_labels):
    """Function extracting the political party of the speakers"""
    
    ids = get_qids(name, df)
    
    if ids is None:
        party = None
    else:
        if ids[0] not in wiki_speakers.index:
            party = None
        else:
            party_id = wiki_speakers.loc[ids[0]].party
            if party_id is None:
                party = None
            else:
                # @TODO are the parties given always in the same chronological order ??
                party = wiki_labels.loc[party_id[0]].Label
        
    return party


def get_occupation(name, df, wiki_speakers, wiki_labels):
    """Function extracting the occupation of the speakers"""
    
    ids = get_qids(name, df)
    
    if ids is None:
        occupation = None
    else:
        if ids[0] not in wiki_speakers.index:
            occupation = None
        else:
            occupation_id = wiki_speakers.loc[ids[0]].occupation
            if occupation_id is None:
                occupation = None
            else:
                occupation = wiki_labels.loc[occupation_id[0]].Label
        
    return occupation
    

def get_attributes(df, wiki_attributes, labels):
    """THE FUNCTION exctracting all the relevant attributes of the speakers"""
    
    # unique speakers and their quotation count
    speakers = top_speakers(df, len(df.speaker.unique()))
    
    # extracting gender
    speakers['gender'] = speakers['speaker'].apply(lambda s: get_gender(s, df, wiki_attributes, labels))
    # extracting age 
    speakers['age'] = speakers['speaker'].apply(lambda s: get_age(s, df, wiki_attributes))
    # extracting nationality
    speakers['nationality'] = speakers['speaker'].apply(lambda s: get_nationality(s, df, wiki_attributes, labels))
    # extracting political party 
    speakers['political_party'] = speakers['speaker'].apply(lambda s: get_party(s, df, wiki_attributes, labels))
    # extarcting occupation
    speakers['occupation'] = speakers['speaker'].apply(lambda s: get_occupation(s, df, wiki_attributes, labels))
    
    return speakers


def get_speakers_by_year(speakers):
    """Function putting all the speakers for all the years in one df"""

    for year in range (2017, 2021):
        s = speakers[year].copy()
        if year == 2017:
            all_speakers = s
            all_speakers['year'] = year
        else:
            s['year'] = year
            all_speakers = all_speakers.append(s)
            
    return all_speakers