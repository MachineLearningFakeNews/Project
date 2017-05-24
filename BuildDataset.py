'''
This code is here as an example of how to use the classes included 
in this folder. it will not be used for final product.

'''

import newspaper
import argparse
import csv
import re
from SiteGrabber import csv_reader, Website

def normalize(content):
    content = re.sub(r'\n+|\t+', ' ', content)
    content = re.sub(r'\s{2,}', ' ', content)
    return content

def main():
    '''
    The function of this script should be to take in the URL of an article in
    question and break it down into its separate parts.

    To Do:
        Create list of sources in CSV file that we can refer to later
   
    ###################################################################################################
    ### OUTPUT DATA FORMAT AS CSV
    #####################################################################################################
    Write to CSV
    
                Source | URL | Title | Authors | Posted Date | Authors | Content
    Article 1
    Article 2
    ...
    ...
    ...
    Article N

    '''

    parser = argparse.ArgumentParser(description='Reads a CSV source and builds an data set')
    parser.add_argument('-o', '--out', type=str, help='Dataset CSV filepath', default='dataset.csv')
    parser.add_argument('--source', type=str, help='Source CSV filepath', default='sources.csv')
    parser.add_argument('--max_per_source', type=int, help='Max articles per source', default=None)
    args = parser.parse_args()

    # If you run this it will go for a long time as it grabs the top sites from all the sites on the CSV
    my_data = csv_reader(args.source)
    sources = my_data.getSources()
    titles = set()

    with open(args.out, 'w') as csvfile:
        fieldnames = ['Source', 'Type','URL','Title','Authors','Date','Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Black lists metadata and action links: /type/, /category/, /feed/, #routes, ?share=
        blacklistRE = re.compile(r'.+((\/(?:type|category|feed)\/.*)|(#.*|\?share=.+$))')

        for s in sources:
            site_ = Website(s)
            count = 0
            for link_ in site_.siteInfo['Articles']:

                if count >= args.max_per_source:
                    print('Source Done')
                    break

                print(link_)

                if blacklistRE.match(link_):
                    print('Blacklisted')
                    continue
                
                try:
                    print('Parsing Article to CSV...')
                    article = newspaper.Article(link_, language='en')
                    article.download()
                    article.parse()
                except:
                    print('Failed to get article.')
                    continue

                content = normalize(article.text)

                if article.title in titles:
                    print('Article was already processed')
                    continue

                if len(content) < 30 and article.authors == []:
                    print('No authors, skipped.')
                    continue

                if content:
                    writer.writerow({
                        'Source': site_.siteInfo['Source'],
                        'Type':   my_data.getTypes(s),
                        'URL':    link_,
                        'Title':  article.title,
                        'Authors':article.authors,
                        'Date':   article.publish_date,
                        'Content':content
                    })
                    titles.add(article.title)
                    count += 1
                else:
                    print('No content')

            print('New Site. Adding Links...')

if __name__ == "__main__":
    main()