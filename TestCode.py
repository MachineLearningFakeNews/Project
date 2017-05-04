'''
This code is here as an example of how to use the classes included 
in this folder. it will not be used for final product.

'''

import newspaper
from SiteGrabber import csv_reader

def main():
    '''
    The function of this script should be to take in the URL of an article in
    question and break it down into its separate parts.

    To Do:
        Create list of sources in CSV file that we can refer to later

    '''

    # If you run this it will go for a long time as it grabs the top sites from all the sites on the CSV
    my_data = csv_reader('sources.csv')
    try:
        for i in my_data.parsed_data:
            x = newspaper.build(i)
            for article in x.articles:
                print(article.url)
                #print(i, '\t\t', my_data.parsed_data[i])
    except:
        print('Web Error')

    print(my_data.getNotes('FreeBeacon.com'))


if __name__ == "__main__":
    main()