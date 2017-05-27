import argparse
import numpy as np
import pandas as pd
import unicodedata
import csv
import ast
import spacy
import re
import string
from urllib.parse import urlparse
from itertools import groupby, zip_longest
from collections import Counter
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

nlp = spacy.load('en')

STOPWORDS = list(ENGLISH_STOP_WORDS)
UNUSED_SYMBOLS = ['[', ']', '(', ')', '_']
PUNCTUATIONS = ' '.join(string.punctuation).split()
entityRE = re.compile(r'<(.+)>')

parser = argparse.ArgumentParser(description='Reads a CSV data set and preprocesses the content')
parser.add_argument('-o', '--out', type=str, help='Preprocessed CSV filepath', default='dataset_preprocessed.csv')
parser.add_argument('--data', type=str, help='Dataset CSV filepath', default='dataset.csv')
parser.add_argument('--rows', type=int, help='Sample number of data rows to preprocess')
parser.add_argument('--verbose', type=int, help='Enables verbosity of console output', default=1)
args = parser.parse_args()

def preprocess(content):
    # convert non-ASCII to ASCII equivalents. If none, drop them.
    content = unicodedata.normalize('NFC', content).encode('ascii', 'ignore').decode()
    content = nlp_preprocess(content)
    return content

def nlp_preprocess(content):
    for symbol in UNUSED_SYMBOLS:
      content = content.replace(symbol, ' ')

    for symbol in PUNCTUATIONS:
      content = content.replace(' ' + symbol, ' ')
      content = content.replace(symbol + ' ', ' ')

    doc = nlp(content)
    placeholders = set()
    for ent in doc.ents:
      placeholders.add(ent.label_)
      text = ent.text.strip()
      if text:
        content = content.replace(' %s ' % text, ' <%s> ' % ent.label_, 1)

    tokens = content.split()

    result = [token if placeholders.issuperset(entityRE.findall(token)) else token.lower() for token in tokens]
    result = [token for token in result if token not in STOPWORDS]

    content = ' '.join(result)
    return content

def expand_type_columns(df):
  df = pd.DataFrame.copy(df)
  keys = ['Type 1', 'Type 2','Type 3']
  types = np.array([list(types.values()) for types in [dict(zip_longest(keys, ast.literal_eval(row.lower().replace('fake news', 'fake')))) for row in df['Type']]])
  return df.join(pd.DataFrame(dict(zip(keys, types.T))))

def print_type_frequency(df):
  cat_frequency = Counter()
  for row in df['Type']:
    cat_frequency.update([label.strip() for label in ast.literal_eval(row.lower().replace('fake news', 'fake'))])

  print('\nType Frequency:')
  for key, value in cat_frequency.most_common():
    print('%12s %12s' % (key, value))

def write_domain_frequency(domain_frequency):
  print('domain_frequency.csv created')
  with open('domain_frequency.csv', 'w') as csvfile:
    for key, value in domain_frequency.most_common():
      csvfile.write('%s,%s\n' % (key, value))

def balance_data(df, first, cat1, cat2):
  print('Set 1 size: ', first.shape[0])
  second = df[~df.index.isin(first.index)]
  print('Set 2 size: ', second.shape[0])
  second = second.sample(n=first.shape[0])
  first['Label'] = cat1
  second['Label'] = cat2
  return pd.concat([first, second])

def __main__():
  df = pd.read_csv(args.data)

  if args.rows:
    df = df.sample(n=args.rows, random_state=42)

  df = expand_type_columns(df)
  qType1 = df['Type 1']
  qType2 = df['Type 2']
  qType3 = df['Type 3']
  reliable = df[
    ((qType1 == 'reliable') | (qType2 == 'reliable') | (qType3 == 'reliable')) |
    ((qType1 == 'political') & qType2.isnull() & qType3.isnull())
  ]

  print_type_frequency(df)
  print('\nBalance between reliable (Set 1) and unreliable (Set 2) data')
  balanced = balance_data(df, reliable, 'reliable', 'unreliable')
  print('\nPreprocessing...')

  domain_frequency = Counter()
  prevTotal = df.shape[0]
  for index, row in balanced.iterrows():
    source = row['Source']
    types = row['Type']
    url = row['URL']
    title = row['Title']
    authors = row['Authors']
    publish_date = row['Date']
    article_content = row['Content']
    label = row['Label']
    
    url = urlparse(url)
    domain_frequency.update([url.hostname])

    article_content = preprocess(article_content)

    row['Content'] = article_content

    if args.verbose > 1:
      print('\nSource: ', source)
      print('Type: ', types)
      print('URL: ', url)
      print('Title: ', title)
      print('Authors: ', authors)
      print('Date: ', publish_date)
      print('Content:\n',  article_content)
      print('Label:', label, '\n')

  print('\n[Total] Before:', df.shape[0], ' After:', balanced.shape[0])
  print('')
  if args.verbose > 0:
    write_domain_frequency(domain_frequency)
    print('')

  df = balanced
  del df['Type 1']
  del df['Type 2']
  del df['Type 3']
  df.to_csv(args.out, index=False)

if __name__ == "__main__":
    __main__()