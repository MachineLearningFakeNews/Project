import csv
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


df = pd.read_csv('dataset_preprocessed.csv', index_col=False)

articles = df['Content']

# df = df.sample(frac=0.5)


# creating term frequency matrix
count_vectorizer = CountVectorizer()
count_vectorizer.fit_transform(df['Content'])

freq_term_matrix = count_vectorizer.transform(df['Content'])

print ("shape: ", freq_term_matrix.shape)
print (freq_term_matrix.todense())


# calculate tf-idf wieghts
tfidf = TfidfTransformer(norm="l2")
tfidf.fit(freq_term_matrix)

# transforms to tf-idf weight matrix
tf_idf_matrix = tfidf.transform(freq_term_matrix)

print (tf_idf_matrix.todense())

print (tf_idf_matrix.shape)

trainset = pd.DataFrame(tf_idf_matrix.todense())
trainset.to_csv("trainset.csv")
