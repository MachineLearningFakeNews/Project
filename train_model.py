import os
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from time import time
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


PATH = os.path.dirname(os.path.abspath(__file__))

def load_data():
  loader = np.load(os.path.join(PATH, 'trainset.npz'))
  x = csr_matrix((  loader['data'], loader['indices'], loader['indptr']), shape = loader['shape'])
  y = pd.read_csv(os.path.join(PATH, 'trainset_labels.csv'))
  return (x, y)

def shuffle_split(x, y):
  x, y = shuffle(x, y, random_state=42)
  return train_test_split(x, y, test_size=0.2, random_state=42)

def train_svm(train_x, train_y, c_value):
  clf = SVC(kernel='linear', C = c_value, probability = True, random_state = 42)
  clf.fit(train_x, train_y.values.ravel())
  return clf

# def train_NB(train_x, train_y, a_values): # which NB?
#   clf = MultinomialNB(alpha = a_values)
#   clf.fit(train_x, train_y.values.ravel())
#   return clf


def evaluate(clf, test_x, test_y):  
  predicted = clf.predict(test_x)

  acc = metrics.accuracy_score(test_y, predicted)
  f1 = f1_score(test_y, predicted, average="macro")
  precision = precision_score(test_y, predicted, average="macro")
  recall = recall_score(test_y, predicted, average="macro")

  return acc, f1, precision, recall


def analyze_svm(train_x, test_x, train_y, test_y):
  print ('Training SVM model with different C:')

  C = [0.0001, 0.001, 0.01, 0.1, 1, 10]
  # C = [0.0001, 0.001] # quick test
  result = []

  for c_value in C:
    print ('C value: %f' % c_value)
    clf = train_svm(train_x, train_y, c_value)
    ret = evaluate(clf, test_x, test_y)
    print ('----------------------------------------')

    model_used = 'SVM, C: ' + str('%.6f' % c_value)
    ret += model_used,
    result.append(ret)
  
  return result
  # return:
  # model name, acc, f1, precision, recall
  # add returned value to a list and use this list to print (plain text or graph)


if __name__ == '__main__':
  train_x, train_y = load_data()

  print(train_x.shape, type(train_x)) # train_x is a csr_matrix
  print(train_y.shape, type(train_y)) # train_y is a Pandas Dataframe

  train_x, test_x, train_y, test_y = shuffle_split(train_x, train_y)

  svm_result = analyze_svm(train_x, test_x, train_y, test_y)
  for r in svm_result:
    print ('Model: ' + r[4])
    print ('acc: %.4f' % [0])
    print ('f1: %.4f' % r[1])
    print ('precision: %.4f' % r[2])
    print ('recall: %.4f' % r[3])
    print ('----------------------------------------')
    
