# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:48:37 2023

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

guiproj = {}
with open('tmpProj', 'wb') as f:
    pickle.dump(guiproj, f)

mainWin = Tk()
mainWin.geometry('1300x720')
mainWin.title('MapDecoder DotGEO')

# elements

# buttons
importBut = Button(master = mainWin, text = 'Import map', width = 25)
pickBut = Button(master = mainWin, text = 'Pick point', width = 25)
openClass = Button(master = mainWin, text = 'Class explorer', width = 25)
openProcessingBut = Button(master = mainWin, text = 'Processing', width = 25)

# figures

canvas_map = Canvas(mainWin, width= 1000, height= 700, bg = 'white')
img = Image.open("./prj/import.png")
img = img.resize((1000,700), Image.ANTIALIAS)
pic = ImageTk.PhotoImage(img)
mapContainer = canvas_map.create_image(0,0,anchor=NW,image=pic)

# functions
def importMap(event):
    
    filename = fd.askopenfilename(initialdir = os.getcwd())
    img = Image.open(filename)
    img = img.resize((1000,700), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    canvas_map.itemconfig(mapContainer, image = img)
    canvas_map.imgref = img
    
    curPrb = Problem()
    curPrb.setMap(filename)
    
    guiproj = {}
    guiproj['problem'] = curPrb
    guiproj['pixelSize'] = [canvas_map.winfo_height(), canvas_map.winfo_width()]
    with open('tmpProj', 'wb') as f:
        pickle.dump(guiproj, f)

def updateMap():
    return
    
# def pickPoint(event):
#     xc = event.x
#     yc = event.y   
    
#     canvas_map.update()
#     print(canvas_map.winfo_height())
#     print(canvas_map.winfo_width())
    
#     return xc,yc
    
def addPointToClass(event):
    return

def delPointFromClass(event):
    return

def createClass(event):
    return

def delClass(event):
    return

def openProcessing(event):
    processWin = Toplevel(master=mainWin)
    processWin.title('Processing')
    processWin.geometry('400x600')
    processWin.attributes('-topmost', 'true')
    
    # elements
    # functions
    # binding
    # placing
    
    
    processWin.mainloop()

def openClassExplorer(event):
    classWin = Toplevel(master=mainWin)
    classWin.title('Class explorer')
    classWin.geometry('400x600')
    classWin.attributes('-topmost', 'true')
    
    checkInt = IntVar()
    pickmodeCheck = Checkbutton(master = classWin, text="Picking mode", variable=checkInt)
    
    classList = Listbox(master=classWin, height = 28, width = 30)
    classPoints = Listbox(master=classWin, height = 28, width = 30)
    
    classList.place(x=10,y=10)
    classPoints.place(x=200,y=10)
    
    createClassBut = Button(master = classWin, width = 25, text = 'Add class')
    newClassNameEntry = Entry(master = classWin, width = 30)
    delSelClassBut = Button(master = classWin, width = 25, text = 'Del selected class')
    delSelClassPointBut = Button(master = classWin, width = 25, text = 'Del selected point')
    
    # functions
    def addClass(event):
        className = newClassNameEntry.get()
        if className not in list(classList.get(0,END)) and className!='':
            classList.insert(END, className)
            newClassNameEntry.delete(0,END)
            
    def showPoints(event):
        classPoints.delete(0,END)
        classPoints.insert(END, classList.get(classList.curselection()))

    def pickPoint(event):
        
        if checkInt.get()==1:
            xc = event.x
            yc = event.y   
            print(classList.get(classList.curselection())+' '+str(xc)+'/'+str(yc))
        else:
            print('Mode is not activated')
        
        return xc,yc

    # binding
    createClassBut.bind('<ButtonRelease-1>', addClass)
    canvas_map.bind('<ButtonRelease-1>', pickPoint)
    classList.bind('<ButtonRelease-1>', showPoints)
    # delSelClassBut
    # placing
    
    createClassBut.place(x=10,y=470)
    newClassNameEntry.place(x=200, y = 473)
    
    delSelClassBut.place(x=10,y=500)
    delSelClassPointBut.place(x=200,y=500)
    
    pickmodeCheck.place(x=10,y=530)
    
    
    classWin.mainloop()
#binding

importBut.bind('<ButtonRelease-1>', importMap)
# canvas_map.bind('<ButtonRelease-1>', pickPoint)
openClass.bind('<ButtonRelease-1>', openClassExplorer)
openProcessingBut.bind('<ButtonRelease-1>', openProcessing)


# placing

importBut.place(x=10,y=20)
openClass.place(x=10,y=50)
openProcessingBut.place(x=10,y=80)

canvas_map.place(x = 250, y = 10)

mainWin.mainloop()