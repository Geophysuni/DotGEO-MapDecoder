# -*- coding: utf-8 -*-
"""
Created on Sat May 20 20:02:40 2023

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
from pcw import processWin
from dgtz import digitizeWin


class mainWin:
    def __init__(self):
        
        self.mainWin = Tk()
        self.mainWin.geometry('1300x720')
        self.mainWin.title('MapDecoder DotGEO')

        # elements

        # buttons
        self.importBut = Button(master = self.mainWin, text = 'Import map', width = 25)
        self.pickBut = Button(master = self.mainWin, text = 'Pick point', width = 25)
        self.openClass = Button(master = self.mainWin, text = 'Class explorer', width = 25)
        self.openProcessingBut = Button(master = self.mainWin, text = 'Processing', width = 25)
        
        self.canvas_map = Canvas(self.mainWin, width= 1000, height= 700, bg = 'white')
        # img = Image.open(os.getcwd()+"\\prj\\import.png")
        # img = img.resize((1000,700), Image.ANTIALIAS)
        
        w, h = 1000, 700
        data = np.zeros((h, w, 3), dtype=np.uint8)
        data[0:256, 0:256] = [0, 0, 0] # red patch in upper left
        img = Image.fromarray(data, 'RGB')
        
        # img = np.zeros((700,1000,4))
        
        pic = ImageTk.PhotoImage(img)
        mapContainer = self.canvas_map.create_image(0,0,anchor=NW,image=pic)
        
        # functions
        
        def importMap(event):
            
            filename = fd.askopenfilename(initialdir = os.getcwd())
            img = Image.open(filename)
            img = img.resize((1000,700), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.canvas_map.itemconfig(mapContainer, image = img)
            self.canvas_map.imgref = img
            
            curPrb = Problem()
            curPrb.setMap(filename)
            
            # вытащить наружу
            curPrb.setWinSize(20,20)
            
            guiproj = {}
            guiproj['problem'] = curPrb
            guiproj['pixelSize'] = [self.canvas_map.winfo_height(), self.canvas_map.winfo_width()]
            with open('tmpProj', 'wb') as f:
                pickle.dump(guiproj, f)
                
        def openProcessing(event):
            self.procWin = processWin(self)
            self.procWin.start()
            
        def openClassExplorer(event):
            self.digitizeWin = digitizeWin(self)
            self.digitizeWin.start()
            
            
        
        # binding
        # 
        self.importBut.bind('<ButtonRelease-1>', importMap)
        # canvas_map.bind('<ButtonRelease-1>', pickPoint)
        self.openClass.bind('<ButtonRelease-1>', openClassExplorer)
        self.openProcessingBut.bind('<ButtonRelease-1>', openProcessing)


        # placing

        self.importBut.place(x=10,y=20)
        self.openClass.place(x=10,y=50)
        self.openProcessingBut.place(x=10,y=80)

        self.canvas_map.place(x = 250, y = 10)
        
    def start(self):
        self.mainWin.mainloop()
        
mainWin = mainWin()
mainWin.start()