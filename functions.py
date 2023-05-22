# -*- coding: utf-8 -*-
"""
Created on Sat May 13 19:31:02 2023

@author: Sergey Zhuravlev
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numba import jit, njit
import statistics as stat
import pickle
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.preprocessing import StandardScaler 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix


class Problem:
    def __init__(self):
        self.image = None
        self.wind = None
        self.classes = {}
        self.classesPos = {}
        self.classDistMaps = {}
    
    def setMap(self, filepath):
        self.image = mpimg.imread(filepath)
    
    def setWinSize(self, ny, nx):
        self.wind = np.array([ny,nx]).astype(int)
        
    # @njit
    def getWinHist(self, i,j):
        # i,j = 100,100
        curWin = self.image[i-self.wind[0]:i+self.wind[0], j-self.wind[1]:j+self.wind[1]]
        res0 = np.ravel(curWin[:,:,0])
        res1 = np.ravel(curWin[:,:,1])
        res2 = np.ravel(curWin[:,:,2])
        hist = [np.histogram(res0, bins = 10, range=[0,1])[0]/len(res0),np.histogram(res1, bins = 10, range=[0,1])[0]/len(res0),
                np.histogram(res2, bins = 10, range=[0,1])[0]/len(res0)]

        return hist
    
    def getWin(self, i,j):
        # i,j = 100,100
        curWin = self.image[i-self.wind[0]:i+self.wind[0], j-self.wind[1]:j+self.wind[1]]
        res0 = np.ravel(curWin[:,:,0])
        res1 = np.ravel(curWin[:,:,1])
        res2 = np.ravel(curWin[:,:,2])
        
        return [res0, res1, res2]
    
    def getImageMask(self):
        
        spMatr = np.zeros((np.shape(self.image)[0], np.shape(self.image)[1], 3, 10))
        print('Calculation of spectral charachteristic has been started. It may take several minutes...')
        for i in range(self.wind[0],np.shape(self.image)[0]-self.wind[0]):
            print(i)
            for j in range(self.wind[1],np.shape(self.image)[1]-self.wind[1]):
                h = self.getWinHist(i,j)
                spMatr[i,j,0,:] = h[0]
                spMatr[i,j,1,:] = h[1]
                spMatr[i,j,2,:] = h[2]
        self.spectrMask = spMatr
        print('Calculation of image spectrum is finished')
        
    def addEmptyClass(self, objName):
        self.classes[objName] = []
        self.classesPos[objName] = []
        self.classDistMaps[objName] = []
        
    def addToClass(self, objname, i, j):
        try:
            self.classes[objname].append(self.getWinHist(i,j))
            self.classesPos[objname].append([i,j])
        except:
            self.classes[objname] = [self.getWinHist(i,j)]
            self.classesPos[objname]= list([i,j])
    
    def removeClass(self, objName):
        
        try:
            del self.classes[objName]
            del self.classesPos[objName]
        except:
            bonk = 1
        try:
            del self.classDistMaps[objName]
        except:
            bonk = 1
            
    
    def getDist(self, tar, cur):
        r = stat.stdev(tar-cur)
        return r
            
    def findUniqueClass(self, objname):
        iniClass = self.classes[objname]
        spec = []
        for i in range(len(iniClass)):
            tmp = np.hstack((iniClass[i][0], iniClass[i][1], iniClass[i][2]))
            spec.append(tmp)
        
        tarData = np.array(spec)
        
        data = []
        for i in range(np.shape(self.spectrMask)[0]):
            for j in range(np.shape(self.spectrMask)[1]):
                data.append(np.hstack((self.spectrMask[i,j,0,:],self.spectrMask[i,j,1,:],self.spectrMask[i,j,2,:])))
        data = np.array(data)
        
        tarMin,tarMax = np.min(tarData , axis = 0), np.max(tarData , axis = 0)
        tarMean = np.mean(np.vstack((tarMin, tarMax)), axis = 0)
        
        print('Calculation is started it may take time ...')
        rel = []
        for i in range(len(data)):
            cur = data[i]
            r = self.getDist(tarMean,cur)
            rel.append(r)
        print('Calculation is done')
        
        tarMask = np.zeros((np.shape(self.spectrMask)[0], np.shape(self.spectrMask)[1]))
        k = 0
        for i in range(np.shape(self.spectrMask)[0]):
            for j in range(np.shape(self.spectrMask)[1]):
                tarMask[i,j] = rel[k]
                k = k+1
        
        try:
            self.classDistMaps[objname] = tarMask 
        except:
            self.classDistMaps = {}
            self.classDistMaps[objname] = tarMask 
        
    
    def getAutoClassMap(self):
        
        s = np.shape(self.spectrMask)
        spList = []
        for i in range(s[0]):
            for j in range(s[1]):
                # if np.max(prb.spectrMask[i,j,0,:])!=np.min(prb.spectrMask[i,j,0,:]):
                spList.append(np.hstack((self.spectrMask[i,j,0,:],self.spectrMask[i,j,1,:],self.spectrMask[i,j,2,:]))) 
        data = np.array(spList)
        
        model = KMeans(n_clusters=10)
        model.fit(data)
        
        mask = np.zeros((np.shape(self.image)[0], np.shape(self.image)[1]))

        k = 0
        for i in range(np.shape(mask)[0]):
            for j in range(np.shape(mask)[1]):
                mask[i,j] = model.labels_[k]
                k = k+1
        
        self.autoClassMap = mask
    
    
# prb = Problem()
# prb.setMap('C:/Users/Sergey Zhuravlev/Documents/science/mapDecoder/map1.png')
# prb.setWinSize(20,20)
# prb.getImageMask()
# prb.getAutoClassMap()

# fig, ax = plt.subplots(1,2)
# ax[0].imshow(prb.image)
# ax[1].imshow(prb.autoClassMap)

# prb.addClass('Травка', 200, 500)
# prb.addClass('Травка', 80, 500)
# prb.addClass('Травка', 100, 550)
# prb.addClass('Травка', 110, 550)

# # prb.findUniqueClass('Травка')

# # fig, ax = plt.subplots(1,2)
# # ax[0].imshow(prb.image)
# # ax[1].imshow(prb.classDistMaps['Травка'])

# prb.addClass('Речка', 240, 203)
# prb.addClass('Речка', 269, 89)
# prb.addClass('Речка', 298, 368)
# prb.addClass('Речка', 200, 293)

# prb.findUniqueClass('Речка')

# fig, ax = plt.subplots(1,2)
# ax[0].imshow(prb.image)
# ax[1].imshow(prb.classDistMaps['Речка'])

# prb.removeClass('Речка')



