# -*- coding: utf-8 -*-
"""
Created on Sun May 21 22:58:49 2023

@author: Sergey Zhuravlev
"""

from functions import *
import pickle

with open('tmpProj', 'rb') as f:
    guiproj = pickle.load(f)