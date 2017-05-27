import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


loader = np.load('trainset.npz')
train_x = csr_matrix((  loader['data'], loader['indices'], loader['indptr']), shape = loader['shape'])
train_y = pd.read_csv('trainset_labels.csv')

print(train_x.shape, type(train_x)) # train_x is a csr_matrix
print(train_y.shape, type(train_y)) # train_y is a Pandas Dataframe
