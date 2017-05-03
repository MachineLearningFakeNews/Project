'''
This code is here as an example of how to use the classes included 
in this folder. it will not be used for final product.

'''

from URLParser import Website
from newspaper import Article
from SiteGrabber import csv_reader

def main():
    '''
    The function of this script should be to take in the URL of an article in
    question and break it down into its separate parts.

    To Do:
        Create list of sources in CSV file that we can refer to later

    '''
    csv1 = csv_reader('sources.csv')

if __name__ == "__main__":
    main()