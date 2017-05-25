import argparse
import numpy as np
import pandas as pd
import unicodedata
import csv
import ast
import spacy
from itertools import groupby, zip_longest
from collections import Counter

nlp = spacy.load('en')

def preprocess(content):
    # convert non-ASCII to ASCII equivalents. If none, drop them.
    content = unicodedata.normalize('NFC', content).encode('ascii', 'ignore').decode()
    #Don't include this method yet. It take too long for execution (2 seconds each loop)
    #content = replace_name_place(content)
    return content

def replace_name_place(content):
    
    '''
        Spacy Build-in entity types
        PERSON - People, including fictional.
        GPE - Countries, cities, states.
        
    '''
    
    
    name_holder = "<NAME>"
    place_holder = "<PLACE>"
    
    person_list = []
    location_list = []
    
    doc = nlp(content)
    
    for ent in doc.ents:
        if(ent.ent_type_ == 'PERSON'):
            person_list.append(ent.text)
        if(ent.ent_type_ == 'GPE'):
            location_list.append(ent.text)
    
    #Remove duplicate words
    person_list = list(set(person_list))
    location_list = list(set(location_list))
    
    for person in person_list:
        content = content.replace(person, name_holder)
              
    for location in location_list:
        content = content.replace(location, place_holder)
    
    return content

def expand_type_columns(df):
  keys = ['Type 1', 'Type 2','Type 3']
  types = np.array([list(types.values()) for types in [dict(zip_longest(keys, ast.literal_eval(row))) for row in df['Type']]])
  type_columns = dict(zip(keys, types.T))
  for key in keys:
    df[key] = type_columns[key]
  del df['Type']
  return df

def print_type_frequency(df):
  cat_frequency = Counter()
  for row in df['Type']:
    cat_frequency.update(ast.literal_eval(row))
  print(cat_frequency)
  return df

def balance_one_vs_all(df, type_label):
  return df

parser = argparse.ArgumentParser(description='Reads a CSV data set and preprocesses the content')
parser.add_argument('-o', '--out', type=str, help='Preprocessed CSV filepath', default='dataset_preprocessed.csv')
parser.add_argument('--data', type=str, help='Dataset CSV filepath', default='dataset.csv')
parser.add_argument('--rows', type=int, help='Sample number of data rows to preprocess')
parser.add_argument('--debug', action='store_true', help='Enable debug print')
args = parser.parse_args()

with open(args.out, 'w') as csvfile:
  fieldnames = ['Source','Type 1','Type 2','Type 3','URL','Title','Authors','Date','Content']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

  df = pd.read_csv(args.data)

  if args.rows:
    df = df.sample(n=args.rows, random_state=42)

  if args.debug:
    print('\nTotal: ', df.shape[0])
    print_type_frequency(df)

  df = expand_type_columns(df)    

  df = balance_one_vs_all(df, 'credible')

  print('')

  for index, row in df.iterrows():
    source = row['Source']
    type1 = row['Type 1']
    type2 = row['Type 2']
    type3 = row['Type 3']
    url = row['URL']
    title = row['Title']
    authors = row['Authors']
    publish_date = row['Date']
    article_content = row['Content']

    article_content = preprocess(article_content)

    if args.debug:
      print('Source: ', source)
      print('Type 1: ', type1)
      print('Type 2: ', type2)
      print('Type 3: ', type3)
      print('URL: ', url)
      print('Title: ', title)
      print('Authors: ', authors)
      print('Date: ', publish_date)
      print('Content:\n',  article_content, '\n')

    writer.writerow({
      'Source': source,
      'Type 1': type1,
      'Type 2': type2,
      'Type 3': type3,
      'URL':    url,
      'Title':  title,
      'Authors':authors,
      'Date':   publish_date,
      'Content':article_content
    })
