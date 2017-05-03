import re
from newspaper import Article


class Website():
    def __init__(self, _url):
        self.webAddress = _url
        self.source = self.getSource()
        if self.source != 'Invalid Site':
            # Get article
            self.article = Article(_url)
            self.article.download()
            self.article.parse()

            self.authors = self.getAuthors()
            self.summary = self.article.summary
        else:
            print('Error: Link given is not a valid URL')

    def getArticleText(self):
        '''
        Get Text of article
        :return String: 
        '''
        return self.article.text

    def getAuthors(self):
        '''
        Get Authors returns the authors found by newspaper
        :return List: 
        '''
        return self.article.authors

    def getSource(self):
        ''' Get Source
        returns the source given a url
        :return string: 
        '''
        url_regex = re.compile('http[s]?://www\.(.*)\.com.*')
        url_source = re.search(url_regex, self.webAddress).group(1).lower()
        return url_source if url_source else 'Invalid Site'

    def isValidURL(self, url_):
        '''
        Check if URL is valid. Will be used to observe extra notes.
        :return bool: 
        '''
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return True if regex.search(url_) else False