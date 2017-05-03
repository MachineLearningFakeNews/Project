import csv, json, re

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
                json_temp[row['website']] = temp_dic
                site_type = []

        with open('data.json', 'w') as outfile:
            json.dump(json_temp, outfile)

        print('Created')