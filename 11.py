import numpy as np
from numpy import linalg as LA
a2d=np.array([100,200,300],[111,222,333],[129,461,795])
w,v=LA.eig(a2d)#求特征值和特征向量


