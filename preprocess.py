import argparse
import numpy as np
import pandas as pd
import unicodedata
import csv
import ast
import spacy
import re
from urllib.parse import urlparse
from itertools import groupby, zip_longest
from collections import Counter
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.tokenize import SpaceTokenizer

nlp = spacy.load('en')

STOPWORDS = list(ENGLISH_STOP_WORDS)
UNUSE_SYMBOLS = ['"']

parser = argparse.ArgumentParser(description='Reads a CSV data set and preprocesses the content')
parser.add_argument('-o', '--out', type=str, help='Preprocessed CSV filepath', default='dataset_preprocessed.csv')
parser.add_argument('--data', type=str, help='Dataset CSV filepath', default='dataset.csv')
parser.add_argument('--rows', type=int, help='Sample number of data rows to preprocess')
parser.add_argument('--debug', action='store_true', help='Enable debug print')
args = parser.parse_args()

def preprocess(content):
    # convert non-ASCII to ASCII equivalents. If none, drop them.
    content = unicodedata.normalize('NFC', content).encode('ascii', 'ignore').decode()
    
    content = nlp_preprocess(content)
    return content

def nlp_preprocess(content):
    
    #PERSON, NORP, FACILITY, ORG, GPE, LOC, PRODUCT, EVENT, WORK_OF_ART, LANGUAGE
    
    place_holders = ['<PERSON>', '<NORP>', '<FACILITY>', '<ORG>', '<GPE>', '<LOC>', '<PRODUCT>', '<EVENT>', '<WORK_OF_ART>', '<LANGUAGE>']
    
    person_list = []
    norp_list = []
    facility_list = []
    org_list = []
    gpe_list = []
    loc_list = []
    product_list = []
    event_list = []
    work_of_art_list = []
    language_list = []
    
    result = []
    
    '''
    for token in tokens:
        result.append(token.text.lower() if token.ent_type_ == "" else "<{}>".format(token.ent_type_))
    '''
    tokens = nlp(content)
    
    for ent in tokens.ents:
        if ent.label_ == 'PERSON':
            person_list.append(ent.text)
        elif ent.label_ == 'NORP':
            norp_list.append(ent.text)
        elif ent.label_ == 'FACILITY':
            facility_list.append(ent.text)
        elif ent.label_ == 'ORG':
            org_list.append(ent.text)
        elif ent.label_ == 'GPE':
            gpe_list.append(ent.text)
        elif ent.label_ == 'LOC':
            loc_list.append(ent.text)
        elif ent.label_ == 'PRODUCT':
            product_list.append(ent.text)
        elif ent.label_ == 'EVENT':
            event_list.append(ent.text)
        elif ent.label_ == 'WORK_OF_ART':
            work_of_art_list.append(ent.text)
        elif ent.label_ == 'LANGUAGE':
            language_list.append(ent.text)
            
    person_list = list(set(person_list))
    norp_list = list(set(norp_list))
    facility_list = list(set(facility_list))
    org_list = list(set(org_list))
    gpe_list = list(set(gpe_list))
    loc_list = list(set(loc_list))
    product_list = list(set(product_list))
    event_list = list(set(event_list))
    work_of_art_list = list(set(work_of_art_list))
    language_list = list(set(language_list))
    
    
    for person in person_list:
        content = content.replace(person, "<PERSON>")	
    for norp in norp_list:
        content = content.replace(norp, "<NORP>")	
    for facility in facility_list:
        content = content.replace(facility, "<FACILITY>")	
    for org in org_list:
        content = content.replace(org, "<ORG>")	
    for gpe in gpe_list:
        content = content.replace(gpe, "<GPE>")	
    for loc in loc_list:
        content = content.replace(loc, "<LOC>")	
    for product in product_list:
        content = content.replace(product, "<PRODUCT>")	
    for event in event_list:
        content = content.replace(event, "<EVENT>")	
    for work in work_of_art_list:
        content = content.replace(work, "<WORK_OF_ART>")	
    for lang in language_list:
        content = content.replace(lang, "<LANGUAGE>")	
        
   
    tokens = SpaceTokenizer().tokenize(content)

    for token in tokens: 
        result.append(token.lower().strip() if token not in place_holders else token)
        
    #result = [token.lower().strip() for token in result if token not in place_holders]
    
    result = [token for token in result if token not in STOPWORDS]
    result = [token for token in result if token not in UNUSE_SYMBOLS]

    content  = " ".join(result)
    return content

def get_type_columns(df):
  df = pd.DataFrame.copy(df)
  keys = ['Type 1', 'Type 2','Type 3']
  types = np.array([list(types.values()) for types in [dict(zip_longest(keys, ast.literal_eval(row.lower().replace('fake news', 'fake')))) for row in df['Type']]])
  type_columns = dict(zip(keys, types.T))
  for key in keys:
    df[key] = type_columns[key]
  del df['Type']
  return df

def print_type_frequency(df):
  cat_frequency = Counter()
  for row in df['Type']:
    cat_frequency.update([label.strip() for label in ast.literal_eval(row.lower().replace('fake news', 'fake'))])

  print('Type Frequency:')
  for key, value in cat_frequency.most_common():
    print('%12s %12s' % (key, value))

def write_domain_frequency(domain_frequency):
  print('domain_frequency.csv created')
  with open('domain_frequency.csv', 'w') as csvfile:
    for key, value in domain_frequency.most_common():
      csvfile.write('%s,%s\n' % (key, value))

def balance_data(df, query_split):
  first = df[df.isin(query_split)]
  second = df[~df.isin(first)]
  return df[df.isin(first) | df.isin(second)]

def __main__():
  df = pd.read_csv(args.data)

  if args.rows:
    df = df.sample(n=args.rows, random_state=42)
  
  print('Preprocessing...')

  domain_frequency = Counter()
  prevTotal = df.shape[0]
  for index, row in df.iterrows():
    source = row['Source']
    types = row['Type']
    url = row['URL']
    title = row['Title']
    authors = row['Authors']
    publish_date = row['Date']
    article_content = row['Content']
    
    url = urlparse(url)
    domain_frequency.update([url.hostname])

    article_content = preprocess(article_content)

    row['Content'] = article_content

    if args.debug:
      print('\nSource: ', source)
      print('Type: ', types)
      print('URL: ', url)
      print('Title: ', title)
      print('Authors: ', authors)
      print('Date: ', publish_date)
      print('Content:\n',  article_content, '\n')

  types = get_type_columns(df)
  qType1 = types['Type 1']
  qType2 = types['Type 2']
  qType3 = types['Type 3']

  reliable = types[((qType1 == 'reliable') | (qType2 == 'reliable') | (qType3 == 'reliable'))]
  balanced = balance_data(types, reliable)

  print('\nSummary')
  print_type_frequency(df)
  print('')
  print('\n[Total] Before:', df.shape[0], ' After:', balanced.shape[0])
  print('')
  if args.debug:
    write_domain_frequency(domain_frequency)

  df.to_csv(args.out, index=False)

if __name__ == "__main__":
    __main__()