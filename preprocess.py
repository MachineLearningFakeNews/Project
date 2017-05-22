import argparse
import pandas as pd
import unicodedata
import csv

def preprocess(content):
  # convert non-ASCII to ASCII equivalents. If none, drop them.
  content = unicodedata.normalize('NFC', content).encode('ascii', 'ignore').decode()
  return content

parser = argparse.ArgumentParser(description='Reads a CSV data set and preprocesses the content')
parser.add_argument('--max_rows', type=int, help='Limit number of data rows to preprocess')
parser.add_argument('--debug', action='store_true', help='Enable debug print')
args = parser.parse_args()

with open('trainset.csv', 'w') as csvfile:
  fieldnames = ['Source', 'Type','URL','Title','Authors','Date','Content']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()

  df = pd.read_csv('dataset.csv')

  if args.debug:
    print('\nTotal: ', df.count, '\n')

  for index, row in df.iterrows():
    if (index >= args.max_rows):
      break

    source = row['Source']
    label_categories = row['Type']
    url = row['URL']
    title = row['Title']
    authors = row['Authors']
    publish_date = row['Date']
    article_content = row['Content']

    article_content = preprocess(article_content)

    if args.debug:
      print('Source: ', source)
      print('Type: ', label_categories)
      print('URL: ', url)
      print('Title: ', title)
      print('Authors: ', authors)
      print('Date: ', publish_date)
      print('Content:\n',  article_content, '\n')

    writer.writerow({
      'Source': source,
      'Type':   label_categories,
      'URL':    url,
      'Title':  title,
      'Authors':authors,
      'Date':   publish_date,
      'Content':article_content
    })
