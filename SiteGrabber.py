import csv
import json


class csv_reader():
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
                json_temp['http://www.' + row['website']] = temp_dic
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
