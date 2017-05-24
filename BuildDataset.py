'''
This code is here as an example of how to use the classes included 
in this folder. it will not be used for final product.

'''

import newspaper
#import enchant
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

    # If you run this it will go for a long time as it grabs the top sites from all the sites on the CSV
    my_data = csv_reader('sources.csv')
    sources = my_data.getSources()
    dataset_final = {}  

    with open('dataset.csv', 'w') as csvfile:
        fieldnames = ['Source', 'Type','URL','Title','Authors','Date','Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Black lists metadata links: /type/, /category/, /feed/, #routes
        blacklistRE = re.compile(r'.+((\/(?:type|category|feed)\/.*)|(#.*$))')

        for s in sources:
            site_ = Website(s)
            for link_ in site_.siteInfo['Articles']:
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

                if article.authors == []:
                    print('No authors, skipped.')
                    continue

                content = normalize(article.text)
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
                else:
                    print('No content')

            print('New Site. Adding Links...')

if __name__ == "__main__":
    main()