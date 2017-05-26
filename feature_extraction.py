from collections import defaultdict
import csv
import pandas as pd
import numpy as np
from numpy import genfromtxt

from sklearn.feature_extraction.text import TfidfVectorizer


# used to store dataset contents in a list (Might not be the most efficient way)

# csvfile = open('dataset.csv', 'r')
# reader = csv.reader(csvfile, delimiter=',')


df = pd.read_csv('dataset.csv')

saved_column = df.Content #you can also use df['column_name']



print (articles)
# for row in reader:
#     articles[row[1]].append(row[6])
#
# for articles_id, text in articles.items():
#     articles[articles_id] = "".join(text)
#
# corpus = []
# for id, article in sorted(articles.items(), key=lambda t: t[0]):
#     corpus.append(article)



#TfidfVectorizer:
# analyzer: string, {‘word’, ‘char’} or callable
#    the feature should be made of word or character n-grams.
#    If a callable is passed it is used to extract the sequence of features out of the raw, unprocessed input.
#
# ngram_range:  tuple (min_n, max_n)
#    The lower and upper boundary of the range of n-values for different n-grams to be extracted. All values of n such that min_n <= n <= max_n will be used.
#
# min_df: float in range [0.0, 1.0] or int, default=1
#     When building the vocabulary ignore terms that have a document frequency strictly lower than the given threshold. This value is also called cut-off in the literature. If float, the parameter represents a proportion of documents, integer absolute counts. This parameter is ignored if vocabulary is not None.
#
# stop_words: : string {‘english’}, list, or None (default)
#    If a string, it is passed to _check_stop_list and the appropriate stop list is returned. ‘english’ is currently the only supported string value.
#    If a list, that list is assumed to contain stop words, all of which will be removed from the resulting tokens. Only applies if analyzer == 'word'.
#    If None, no stop words will be used. max_df can be set to a value in the range [0.7, 1.0) to automatically detect and filter stop words based on intra corpus document frequency of terms.


tf =TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')


# Learn vocabulary and idf, return term-document matrix.
tfidf_matrix = tf.fit_transform(articles)

# Array mapping from feature integer indices to feature name
feature_names = tf.get_feature_names()
print (len(feature_names))

print (tfidf_matrix.shape)
dense = tfidf_matrix.todense()

print (dense)
df = pd.DataFrame(dense)
df.to_csv('feature_matrix.csv', index=False)
