# -*- coding: utf-8 -*-
"""
Created on Tue May  9 19:13:13 2023

@author: Sergey Zhuravlev
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numba import jit, njit
import statistics as stat


mapimg = mpimg.imread('C:/Users/Sergey Zhuravlev/Documents/science/mapDecoder/map1.png')

win = [100,100]

@jit
def getWinHist(img, win_size, i,j):
    # i,j = 100,100
    curWin = img[i-win_size[0]:i+win_size[0], j-win_size[1]:j+win_size[1]]
    res0 = np.ravel(curWin[:,:,0])
    res1 = np.ravel(curWin[:,:,1])
    res2 = np.ravel(curWin[:,:,2])
    hist = [np.histogram(res0, bins = 10, range=[0,1])[0],np.histogram(res1, bins = 10, range=[0,1])[0],
            np.histogram(res2, bins = 10, range=[0,1])[0]]

    return hist

spMatr = np.zeros((np.shape(mapimg)[0], np.shape(mapimg)[1], 3, 10))

for i in range(win[0],np.shape(mapimg)[0]-win[0]):
    print(i)
    for j in range(win[1],np.shape(mapimg)[1]-win[1]):
        h = getWinHist(mapimg, win, i,j)
        spMatr[i,j,0,:] = h[0]
        spMatr[i,j,1,:] = h[1]
        spMatr[i,j,2,:] = h[2]
        
        # for i in range(len(h)):
        #     plt.plot(h[i])


def getDist(tar, cur):
    r = 0
    for i in range(3):
        r = r+stat.stdev(tar[i]-cur[i])
    return r

tarPoint = spMatr[200,500,:,:]
plt.figure()
for i in range(len(tarPoint)):
    plt.plot(tarPoint[i])

mask = np.zeros_like(mapimg[:,:,0])
for i in range(win[0],np.shape(mapimg)[0]-win[0]):
    if i%5==0:
        print(i)
    for j in range(win[1],np.shape(mapimg)[1]-win[1]):
        cur = spMatr[i,j,:,:]
        mask[i,j] = getDist(tarPoint, cur)
             
plt.imshow(mask)
