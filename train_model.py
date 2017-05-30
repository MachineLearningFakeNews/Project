import os
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from time import time
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression, SGDClassifier
from texttable import Texttable


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

def train_default(train_x, train_y, model_name):  
  if model_name == 'LR':
    clf = LogisticRegression()
  elif model_name == 'NB':
    clf = MultinomialNB()
  elif model_name == 'SGD':
    clf = SGDClassifier()
  else:
    clf = SVC() # as default

  clf.fit(train_x, train_y.values.ravel())
  return clf

def evaluate(clf, test_x, test_y):  
  predicted = clf.predict(test_x)

  acc = metrics.accuracy_score(test_y, predicted)
  f1 = f1_score(test_y, predicted, average="macro")
  precision = precision_score(test_y, predicted, average="macro")
  recall = recall_score(test_y, predicted, average="macro")

  return acc, f1, precision, recall


def analyze_svm(train_x, test_x, train_y, test_y):
  print ('Training SVM model with different C:')

  # C = [0.0001, 0.001, 0.01, 0.1, 1, 10]
  C = [2.8] # quick test
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

# def analyze_nb(train_x, test_x, train_y, test_y):
#   result = []
#   print ('Training Naive_Bayes model (MultinomialNB)')
#   clf = train_NB(train_x, train_y)
#   ret = evaluate(clf, test_x, test_y)
#   model_used = 'MultinomialNB'
#   ret += model_used,
#   result.append(ret)
#   return result



def analyze_model(train_x, test_x, train_y, test_y, model_name):
  result = []

  if model_name != 'SVM':
    print ('Training model : %s' % model_name)
    clf = train_default(train_x, train_y, model_name)
    ret = evaluate(clf, test_x, test_y)
    model_used = model_name
    ret += model_used,
    result.append(ret)
    return result

  else:
      print ('Training SVM model with different C:')
      C = [0.0001, 0.001, 0.01, 0.1, 1, 10]
      # C = [2.8] # quick test
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


def make_diagram(results):
  indices = np.arange(len(results))
  results = [[x[i] for x in results] for i in range(5)]
  acc, f1, precision, recall, clf_names = results

  plt.title('Report')

  # create plot
  plt.barh(indices + .2,  acc, .2,        label = 'acc',  color = 'navy')  
  plt.barh(indices + .4 , f1, .2,         label = 'f1',   color = 'c')
  plt.barh(indices + .6,  precision, .2,  label = 'precision', color = 'darkorange')
  plt.barh(indices + .8,  recall, .2,     label = 'recall', color = 'red')

  plt.yticks(())
  plt.legend(loc = 'best')
  plt.subplots_adjust(left = .25)
  plt.subplots_adjust(top = .95)
  plt.subplots_adjust(bottom = .15)

  for i, c in zip(indices, clf_names):
      plt.text(-.1, i+.5, c)

  plt.show()


if __name__ == '__main__':
  train_x, train_y = load_data()

  print(train_x.shape, type(train_x)) # train_x is a csr_matrix
  print(train_y.shape, type(train_y)) # train_y is a Pandas Dataframe

  train_x, test_x, train_y, test_y = shuffle_split(train_x, train_y)

  svm_result = analyze_model(train_x, test_x, train_y, test_y, 'SVM')
  nb_result = analyze_model(train_x, test_x, train_y, test_y, 'NB')
  lr_result = analyze_model(train_x, test_x, train_y, test_y, 'LR')
  sgd_result = analyze_model(train_x, test_x, train_y, test_y, 'SGD')

  all_result = []
  all_result += nb_result
  all_result += lr_result
  all_result += sgd_result
  all_result += svm_result

  # print tabulate ([ r[4], r[0], r[1], r[2], r[3] ], headers=['Model', 'Acc', 'f1', 'Precision', 'Recall'])
  
  # make a table
  t = Texttable()
  for r in all_result:
    # print ('Model: ' + r[4])
    # print ('acc: %.4f' % r[0])
    # print ('f1: %.4f' % r[1])
    # print ('precision: %.4f' % r[2])
    # print ('recall: %.4f' % r[3])
    # print ('----------------------------------------')
    t.add_rows([['Model', 'Acc', 'f1', 'Precision', 'Recall'], [r[4], r[0], r[1], r[2], r[3]]])

  print (t.draw())
  make_diagram(all_result)
