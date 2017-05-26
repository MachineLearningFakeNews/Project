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
entityRE = re.compile(r'<(.+)>')

parser = argparse.ArgumentParser(description='Reads a CSV data set and preprocesses the content')
parser.add_argument('-o', '--out', type=str, help='Preprocessed CSV filepath', default='dataset_preprocessed.csv')
parser.add_argument('--data', type=str, help='Dataset CSV filepath', default='dataset.csv')
parser.add_argument('--rows', type=int, help='Sample number of data rows to preprocess')
parser.add_argument('--debug', action='store_true', help='Enable debug print')
args = parser.parse_args()

def preprocess(content):
    # convert non-ASCII to ASCII equivalents. If none, drop them.
    content = unicodedata.normalize('NFC', content).encode('ascii', 'ignore').decode()
    content = content.replace(' .', '.')
    content = content.replace('....', '...')
    content = nlp_preprocess(content)
    return content

def nlp_preprocess(content):
    doc = nlp(content)

    placeholders = set()
    for ent in doc.ents:
      placeholders.add(ent.label_)
      text = ent.text.strip()
      if text:
        content = content.replace(' %s ' % text, ' <%s> ' % ent.label_)

    tokens = SpaceTokenizer().tokenize(content)

    result = [token if placeholders.issuperset(entityRE.findall(token)) else token.lower() for token in tokens]
    result = [token for token in result if token not in STOPWORDS]
    result = [token for token in result if token not in UNUSE_SYMBOLS]

    content = " ".join(result)
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