# -*- coding: utf-8 -*-
"""
Created on Sun May 21 21:08:23 2023

@author: Sergey Zhuravlev
"""

from tkinter import *
from  tkinter import ttk
from tkinter import filedialog as fd
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pickle
import pandas as pd
import numpy as np
import imageio as iio
from scipy import interpolate
import matplotlib.image as mpimg
from PIL import Image,ImageTk
from functions import *

class processWin:
    def __init__(self, root):
        # self.master = root
        self.processWin = Toplevel(master=root.mainWin)
        self.processWin.title('Processing')
        self.processWin.geometry('400x600')
        self.processWin.attributes('-topmost', 'true')
        
        # elements
        # functions
        # binding
        # placing
        
        
    def start(self):
        self.processWin.mainloop()