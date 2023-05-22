# -*- coding: utf-8 -*-
"""
Created on Sat May 13 22:27:35 2023

@author: Sergey Zhuravlev
"""

from numpy import where
from sklearn.datasets import make_classification
from matplotlib import pyplot
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib.image as mpimg
from sklearn.cluster import MeanShift, estimate_bandwidth

with open('sample', 'rb') as f:
    data = pickle.load(f)
    

data = np.array(data)
# data = np.hstack((data, np.zeros((len(data),2))))



model = KMeans(n_clusters=10)
model.fit(data)

mask = np.zeros((452,691))

k = 0
for i in range(452):
    for j in range(691):
        mask[i,j] = model.labels_[k]
        k = k+1
        
image = mpimg.imread('C:/Users/Sergey Zhuravlev/Documents/science/mapDecoder/map1.png')
fig, ax = plt.subplots(1,2)
ax[0].imshow(image)
ax[1].imshow(mask)

# bandwidth = estimate_bandwidth(data, quantile=0.01, n_samples=10000)
# ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
# ms.fit(data)
# labels = ms.labels_

# mask = np.zeros((452,691))

# k = 0
# for i in range(452):
#     for j in range(691):
#         mask[i,j] = ms.labels_[k]
#         k = k+1
        
# image = mpimg.imread('C:/Users/Sergey Zhuravlev/Documents/science/mapDecoder/map1.png')
# fig, ax = plt.subplots(1,2)
# ax[0].imshow(image)
# ax[1].imshow(mask)