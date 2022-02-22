import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('stopwords')
nltk.download('punkt')

pd.set_option('display.max_columns', 200)

investors = pd.read_csv('/home/bruno/Downloads/investors.csv')
funding = pd.read_csv('/home/bruno/Downloads/funding-rounds.csv')
companies = pd.read_csv('/home/bruno/Downloads/companies.csv')

print("investors dataframe created!")

def transform_companies(df):
    df['words'] = df['Industries'] + df['Headquarters Location'] + df['Description'] + df['Full Description']
    df = df[['Organization Name', 'words']]
    df = df.rename(columns={'Organization Name': 'Name'})
    
    df['key_words'] = ""
    for index, row in df.iterrows():
        words = str(row['words'])
        r = Rake()
        r.extract_keywords_from_text(words)
        key_words_dict_scores = r.get_word_degrees()
        row['key_words'] = list(key_words_dict_scores.keys())
        df.key_words[index] = row['key_words']
    df.drop(columns=['words'], inplace=True)
    
    df['bag_of_words'] = ""
    for index, row in df.iterrows():
        df['bag_of_words'][index] = ' '.join(row['key_words'])
    df.drop(columns=['key_words'], inplace=True)
    
    df.set_index('Name', inplace=True)
    
    return df


def transform_investors(df):
    df['words'] = df['Investor Type'] + df['Location'] + df['Description'] + df['Full Description']
    df = df[['Organization/Person Name', 'words']]
    df = df.rename(columns={'Organization/Person Name': 'Name'})
    
    df['key_words'] = ""
    for index, row in df.iterrows():
        words = str(row['words'])
        r = Rake()
        r.extract_keywords_from_text(words)
        key_words_dict_scores = r.get_word_degrees()
        row['key_words'] = list(key_words_dict_scores.keys())
        df.key_words[index] = row['key_words']
    df.drop(columns=['words'], inplace=True)
    
    df['bag_of_words'] = ""
    for index, row in df.iterrows():
        df['bag_of_words'][index] = ' '.join(row['key_words'])
    df.drop(columns=['key_words'], inplace=True)
    
    df.set_index('Name', inplace=True)
    
    return df


def transform_investor(name, fundingType, location, description, fullDescription):
    data = {'Name': [name],
        'words': [fundingType + ' ' + description + ' ' + location + ' ' + fullDescription]}

    df = pd.DataFrame(data)
    
    df['key_words'] = ""
    for index, row in df.iterrows():
        words = str(row['words'])
        r = Rake()
        r.extract_keywords_from_text(words)
        key_words_dict_scores = r.get_word_degrees()
        row['key_words'] = list(key_words_dict_scores.keys())
        df.key_words[index] = row['key_words']
    df.drop(columns=['words'], inplace=True)
    
    df['bag_of_words'] = ""
    for index, row in df.iterrows():
        df['bag_of_words'][index] = ' '.join(row['key_words'])
    df.drop(columns=['key_words'], inplace=True)
    
    df.set_index('Name', inplace=True)
    
    return df


def similarity(df):    
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['bag_of_words'])
    
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    return cosine_sim


def recommendations(name, fundingType, location, description, fullDescription, df_companies):
    invest = transform_investor(name, fundingType, location, description, fullDescription)
    comp = transform_companies(df_companies)
    
    df = comp.append(invest)
    
    cosine_sim = similarity(df)
    
    indices = pd.Series(df.index)
    
    recommended_comp = []
    
    idx = indices[indices == name].index[0]
    
    score = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
    # print('scores', score)
    
    top_10_indices = list(score.iloc[1:21].index)
    
    for i in top_10_indices:
        recommended_comp.append(list(df.index)[i])
    
    return recommended_comp



