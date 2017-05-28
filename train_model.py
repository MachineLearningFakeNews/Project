import os
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics

PATH = os.path.dirname(os.path.abspath(__file__))

def load_data():
  loader = np.load(os.path.join(PATH, 'trainset.npz'))
  x = csr_matrix((  loader['data'], loader['indices'], loader['indptr']), shape = loader['shape'])
  y = pd.read_csv(os.path.join(PATH, 'trainset_labels.csv'))
  return (x, y)

def shuffle_split(x, y):
  x, y = shuffle(x, y, random_state=42)
  return train_test_split(x, y, test_size=0.2, random_state=42)

def train(train_x, train_y):
  clf = SVC(kernel='linear', C=2.8)
  clf.fit(train_x, train_y.values.ravel())
  return clf

def evaluate(clf, test_x, test_y):
  predicted = clf.predict(test_x)
  return metrics.accuracy_score(test_y, predicted)

if __name__ == '__main__':
  train_x, train_y = load_data()

  print(train_x.shape, type(train_x)) # train_x is a csr_matrix
  print(train_y.shape, type(train_y)) # train_y is a Pandas Dataframe

  train_x, test_x, train_y, test_y = shuffle_split(train_x, train_y)

  clf = train(train_x, train_y)
  acc = evaluate(clf, test_x, test_y)
  print('Accuracy: %0.4f' % acc)

