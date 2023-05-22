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

class digitizeWin:
    def __init__(self, root):
        
        self.classWin = Toplevel(master=root.mainWin)
        self.classWin.title('Class explorer')
        self.classWin.geometry('400x600')
        self.classWin.attributes('-topmost', 'true')
        
        
        # elements
        
        self.checkInt = IntVar()
        self.pickmodeCheck = Checkbutton(master = self.classWin, text="Picking mode", variable=self.checkInt)
        
        self.classList = Listbox(master=self.classWin, height = 28, width = 30)
        self.classPoints = Listbox(master=self.classWin, height = 28, width = 30)
        
        self.createClassBut = Button(master = self.classWin, width = 25, text = 'Add class')
        self.newClassNameEntry = Entry(master = self.classWin, width = 30)
        self.delSelClassBut = Button(master = self.classWin, width = 25, text = 'Del selected class')
        self.delSelClassPointBut = Button(master = self.classWin, width = 25, text = 'Del selected point')
        self.saveBut = Button(master = self.classWin, width = 25, text = 'Save')
        
        with open('tmpProj', 'rb') as f:
            guiproj = pickle.load(f)
        try:
            for key in guiproj['problem'].classesPos:
                self.classList.insert(END, key)
        except:
            bonk = 1    
        
        def addClass(event):
            
            with open('tmpProj', 'rb') as f:
                guiproj = pickle.load(f)
            
            className = self.newClassNameEntry.get()
            if className not in list(self.classList.get(0,END)) and className!='':
                self.classList.insert(END, className)
                self.newClassNameEntry.delete(0,END)
                
                guiproj['problem'].addEmptyClass(className)
                
                with open('tmpProj', 'wb') as f:
                    pickle.dump(guiproj, f)
                
        def showPoints(event):
            self.classPoints.delete(0,END)
            className = self.classList.get(self.classList.curselection()) 
            
            with open('tmpProj', 'rb') as f:
                guiproj = pickle.load(f)
                
            for el in guiproj['problem'].classesPos[className]:
                self.classPoints.insert(END, str(el[0])+'/'+str(el[1]))

        def pickPoint(event):
            
            if self.checkInt.get()==1:
                xc = event.x
                yc = event.y   
                
                with open('tmpProj', 'rb') as f:
                    guiproj = pickle.load(f)
                
                ind_i = int((yc/guiproj['pixelSize'][0])*np.shape(guiproj['problem'].image)[0])
                ind_j = int((xc/guiproj['pixelSize'][1])*np.shape(guiproj['problem'].image)[1])
                
                className = self.classList.get(self.classList.curselection())                
                guiproj['problem'].addToClass(className, ind_i, ind_j)    
                
                self.classPoints.delete(0,END)
                for el in guiproj['problem'].classesPos[className]:
                    self.classPoints.insert(END, str(el[0])+'/'+str(el[1]))
                
                
                with open('tmpProj', 'wb') as f:
                    pickle.dump(guiproj, f)                
            else:
                print('Mode is not activated')
            
            # return xc,yc
        
        def saveAndClose(event):
            self.classWin.destroy()

        # binding
        self.createClassBut.bind('<ButtonRelease-1>', addClass)
        root.canvas_map.bind('<ButtonRelease-1>', pickPoint)
        self.classList.bind('<ButtonRelease-1>', showPoints)
        self.saveBut.bind('<ButtonRelease-1>', saveAndClose)
                
        # placing
        self.classList.place(x=10,y=10)
        self.classPoints.place(x=200,y=10)
        
        self.createClassBut.place(x=10,y=470)
        self.newClassNameEntry.place(x=200, y = 473)
        
        self.delSelClassBut.place(x=10,y=500)
        self.delSelClassPointBut.place(x=200,y=500)
        
        self.pickmodeCheck.place(x=10,y=530)
        
        self.saveBut.place(x=10,y=560)
        
    def start(self):
        self.classWin.mainloop()