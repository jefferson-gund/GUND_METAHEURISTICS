'''
#*************************************
#UTFPR 2020 | METAHEURÍSTICAS | CPGEI
#Aluno: Jefferson Gund    RA: 1054040
#*************************************


#Algoritmo Tabu Search para o problema
#de maximizacao de valor monetário de carga de 
#carregamento de container em 3 dimensoes
#*************************************



------------------------------------------------------------------------------
Start to load container by the left lower quarter in the end of the container,
and then, stack the boxes in X direction. Then, when the Y axis loaded, start 
a new loading in the neighborhood from the boxes, going to Z direction. 

                         Y________________
                        /|               /|
                       / |              / |
                      /  |             /  |
                     /   |            /   | ->CONTAINER
                    /____|___________/    |
                    |    |__         |    |
                    |   /|_/| ->BOX  |    |
                    |   ||_||________|____| X->
                    |   |__|/        |   / 
                    |  /             |  /  
                    | /              | /
                    |/_______________|/
                    Z
------------------------------------------------------------------------------
'''


import numpy as np
import pandas as pd
import random
import itertools as itr
import time
import tracemalloc
import math
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
sns.set(color_codes=True)
sns.set(style="darkgrid")



class BOX: 
    #def __init__(self, height=None, lenght=None, width=None, volume=None, 
    #             weight=None, price=None, quantity=None): 
    def __init__(self, height=None, lenght=None, width=None, volume=None, 
                 weight=None, price=None):        
        self._height = height #altura
        self._lenght = lenght #comprimento
        self._width = width   #largura
        self._volume = volume
        self._weight = weight
        self._price = price
        #self._quantity = quantity;
        self._position = [0,0,0]
    
    def removeItem(self):
        if self._quantity > 0:
            self._quantity -= 1
            
    def removeItem(self, qtd=0):
        if qtd >= 0 and self._quantity > 0:
            self._quantity -= qtd
            
    def addItem(self):
        self._quantity += 1
        
    def addItem(self, qtd=0):
        if qtd >= 0:
            self._quantity += qtd
            
    def __eq__(self, other):
        expression = ((self.__class__ == other.__class__) and (self._height == other._height) and (self._lenght == other._lenght) and \
                       (self._width == other._width) and (self._weight == other._weight) and (self._price == other._price))

        return expression


class CONTAINER: 
    def __init__(self, height=None, lenght=None, width=None, MaxWeight=None, MaxPrice=None): 
        
        self._height = height
        self._lenght = lenght
        self._width = width
        self._MaxWeight = MaxWeight
        self._MaxPrice = MaxPrice
        self._MaxVolume = self._height * self._lenght * self._width
        
        
        self.clearContainer()

    def getTotalPriceContainer(self):
       
        totalPrice=0;
        for box in self._loadedBoxes[2:]:
            totalPrice += box[0]._price
        
        return totalPrice

    def getTotalWeightContainer(self):
       
        totalWeight=0;
        for box in self._loadedBoxes[2:]:
            totalWeight += box[0]._weight
        
        return totalWeight  
    
    def getTotalVolumeBoxesContainer(self):
       
        totalBoxesVolume=0;
        for box in self._loadedBoxes[2:]:
            totalBoxesVolume += box[0]._volume
        
        return totalBoxesVolume;  
        
    def rotate_box(self, option):
        switcher_list={0:[0,0,1], #Z axis rotation
                       1:[0,1,0], #Y axis rotation
                       2:[1,0,0], #X axis rotation
                       3:[0,1,1], #Y and Z axis rotation
                       4:[1,0,1], #X and Z axis rotation
                       5:[1,1,0]} #X and Y axis rotation
        
        return switcher_list.get(option, lambda :'Invalid')

    def findMaxHeight(self):
        i=0
        dist = 0
        max = 0
        for bx in self._loadedBoxes:
            if (dist + bx[1][0]) <= self._width:
                dist += bx[1][0]
                
                #i=0
                
                if max < bx[1][1]:
                    max = bx[1][1]
                i +=1
            else:
                break
        
        return max
      
    def neighborhood(self):
        pass
        
    def unloadBox(self):
        self._totalBoxes -= 1
        
    def clearContainer(self):
        #loading container info
        self._trackPos = [0,0,0] #Begin at the origin [0,0,0] cm
        self._trackBox = [0,0,0] #track by counting the the boxes packing in the three axis
       
        self._totalBoxes = 0
        
        
        self._loadedPrice = 0
        self._loadedVolume = 0
        self._loadedWeight = 0
        self._loadedBoxes = []
        
        self._remainingHeight = self._height
        self._remainingLenght = self._lenght
        self._remainingWidth = self._width
        self._remainingWeight = self._MaxWeight
        self._remainingPrice = self._MaxPrice
        self._remainingVolume = self._MaxVolume
        
        self.actual_max_box_height = 0
        self.actual_max_box_lenght = 0
        
        print("self._loadedBoxes.clear-> len(self._loadedBoxes) =", len( self._loadedBoxes) )
        #self._loadedBoxes = [];


    def loadBox(self, BOX):
           
        #if self.score();        
        if (BOX._width <= self._remainingWidth) :
             
    
            self._remainingWidth -= BOX._width
            
            self._loadedBoxes.append([BOX, self._trackPos])       
            
            print("loading BOX._price:", self._loadedBoxes[len(self._loadedBoxes) - 1][0]._price, "location: ", self._loadedBoxes[len(self._loadedBoxes) - 1][1] )
            
            self._trackPos[0] += BOX._width
            
            
            #Get the largest value of height from a "stacking" or "wall" 
            if self.actual_max_box_height < BOX._height:            
                self.actual_max_box_height = BOX._height
            #Get the largest value of lenght from a "stack"    
            if self.actual_max_box_lenght < BOX._lenght:
                self.actual_max_box_lenght = BOX._lenght 
                
            return False
        
        elif (BOX._height <= (self._remainingHeight - self.actual_max_box_height)): #altura
                  
                      
            self._remainingHeight -= self.actual_max_box_height
            self._remainingWidth = self._width - BOX._width
            
            self._trackPos[0] = 0
            self._trackPos[1] = self._height - self._remainingHeight
            
            self.actual_max_box_height = BOX._height      
           
            self._loadedBoxes.append([BOX, self._trackPos])       
            
            print("loading BOX._price:", self._loadedBoxes[len(self._loadedBoxes) -1][0]._price, "location: ", self._loadedBoxes[len(self._loadedBoxes) -1][1] )
            
            self._trackPos[0] += BOX._width
                       
            #Get the largest value of lenght from a "stack"
            if self.actual_max_box_lenght < BOX._lenght:
                self.actual_max_box_lenght = BOX._lenght 

            return False
        
        elif (BOX._lenght <= (self._remainingLenght - self.actual_max_box_lenght)):
        
            
            
            self._remainingLenght -= self.actual_max_box_lenght
            self._remainingHeight = self._height
            self._remainingWidth = self._width
           
            self._trackPos[0] = self._width - self._remainingWidth
            self._trackPos[1] = self._height - self._remainingHeight
            self._trackPos[2] = self._lenght - self._remainingLenght

            self._loadedBoxes.append([BOX, self._trackPos])
           
            print("loading BOX._price:", self._loadedBoxes[len(self._loadedBoxes) -1][0]._price, "location: ", self._loadedBoxes[len(self._loadedBoxes)-1][1] )
            
            self._trackPos[0] += BOX._width
            
            #Get the largest value of lenght from a "stack"
            self.actual_max_box_lenght = BOX._lenght          
            
            return False
        else:
            return True #Container is full!!
        
        
        return -1 #ERROR!


