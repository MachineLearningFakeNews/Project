import csv
import json
import re
import newspaper


class csv_reader:
    def __init__(self, fname):
        '''
        Initialize the CSV Reader.
        '''
        site_type = []
        json_temp = {}
        with open(fname) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                site_type.append(row['type'])
                if row['2nd type'].replace(' ', ''):
                    site_type.append(row['2nd type'])
                    if row['3rd type'].replace(' ', ''):
                        site_type.append(row['3rd type'])
                if row['Source Notes (things to know?)'].replace(' ', ''):
                    extra_notes = row['Source Notes (things to know?)']
                else:
                    extra_notes = 'No extra notes for website!'
                temp_dic = {'Type': site_type, 'Notes': extra_notes}
                json_temp['http://www.' + row['website'].replace(' ','')] = temp_dic
                site_type = []

        print('Created')
        self.parsed_data = json_temp

    def getRawData(self):
        '''
        Return the JSON file as a Dictionary
        :return dict: 
        '''
        return self.parsed_data

    def getSources(self):
        '''
        Return all the websites as a List
        :return list: 
        '''
        return list(self.parsed_data.keys())

    def getTypes(self, website):
        '''
        Take a website name and return the type
        :return list: 
        '''
        return self.parsed_data[website]['Type']

    def getNotes(self, website):
        '''
        Take a website name and return the Extra Notes
        :return list: 
        '''
        return self.parsed_data[website]['Notes']

    def exportJSON(self, dict, filename):
        '''
        Exports the file to filename
        :param dict: 
        '''
        try:
            with open(filename + '.json', 'w') as outfile:
                json.dump(dict, outfile)
        except:
            print('Invalid File Name or Failed to Write to File')


class Website:
    def __init__(self, url_):
        self.__regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:([A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        self.webAddress = url_
        if self.isValidURL(url_) == True:
            if self.getSource() != 'Invalid Site':
                self.siteInfo = {
                    'Source': self.getSource(),
                    'Articles': self.getArticles(self.webAddress)
                }
            else:
                print('Invalid Site!')
        else:
            print('Invalid URL!')

    def getSource(self):
        ''' Get Source
        returns the source given a url
        :return string: 
        '''
        try:
            url_source = re.search(self.__regex, self.webAddress).group(1)[:-1]
            return url_source if url_source else 'Invalid Site'
        except:
            print('Source could not be found...')

    def getArticles(self, url_):
        list = []
        temp = newspaper.build(url_)
        [list.append(article.url) for article in temp.articles]
        return list

    def isValidURL(self, url_):
        '''
        Check if URL is valid. Will be used to observe extra notes.
        :return bool: 
        '''
        return True if self.__regex.search(url_) else False
