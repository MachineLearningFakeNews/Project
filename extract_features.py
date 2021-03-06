import csv
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

df = pd.read_csv('dataset_preprocessed.csv', index_col=False)

articles = df['Content']
labels = df['Label']

print ('Articles count:', articles.shape[0])

vectorizer = TfidfVectorizer(ngram_range=(2,2), lowercase=False, max_features=3000)
tf_idf_matrix = vectorizer.fit_transform(articles)
print ('Matrix shape (articles x features):',  tf_idf_matrix.shape)
joblib.dump(vectorizer, 'vectorizer.pkl')

label_matrix = pd.DataFrame(pd.factorize(labels)[0])
np.savez('trainset',data=tf_idf_matrix.data, indices=tf_idf_matrix.indices, indptr=tf_idf_matrix.indptr, shape=tf_idf_matrix.shape)
label_matrix.to_csv('trainset_labels.csv', index=False)
