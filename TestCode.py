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

    '''

    # If you run this it will go for a long time as it grabs the top sites from all the sites on the CSV
    my_data = csv_reader('sources.csv')
    sources = my_data.getSources()
    dataset_final = {}
    '''
    
    dataset_final = {
        'Article: {
            'Source: string,
            'Url': string,
            'Title': string,
            'Date': string,
            'Authors': list,
            'Content': string
        },
        
    }
    
    Write to CSV
    
                Source | URL | Title | Authors | Posted Date | Authors | Content
    Article 1
    Article 2
    
     '''

    with open('dataset.csv', 'w') as csvfile:
        fieldnames = ['Source', 'Type','URL','Title','Authors','Date','Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        blacklistRE = [
            re.compile(r'.+\/type\/.*'),
            re.compile(r'.+\/category\/.*')
        ]

        for s in sources:
            site_ = Website(s)
            visited_links = {}
            for link_ in site_.siteInfo['Articles']:
                link_ = re.sub(r'#.*$|\/feed\/*$', '', link_)
                print(link_)

                blacklisted = False
                for blacklist in blacklistRE:
                    if blacklist.match(link_):
                        blacklisted = True
                        break
                if blacklisted:
                    print('Blacklisted')
                    continue

                if (link_ in visited_links):
                    print('Link visited')
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

                visited_links[link_] = True

            print('New Site. Adding Links...')
    '''    
    site1 = Website(sources[5])
    print(site1.siteInfo)
    d = enchant.Dict("en_US")

    if site1.siteInfo['Articles']:
        tempSite = newspaper.Article(site1.siteInfo['Articles'][0])
        tempSite.download()
        tempSite.parse()
        tempSite.nlp()
        for word in tempSite.keywords:
            print(word, d.check(word))
    '''
if __name__ == "__main__":
    main()