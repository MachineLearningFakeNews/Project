import numpy as np
from scipy.sparse import csr_matrix

loader = np.load('trainset.npz')
train_x = csr_matrix((  loader['data'], loader['indices'], loader['indptr']), shape = loader['shape'])
print(train_x.shape)
