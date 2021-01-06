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


from binpacking import BOX, CONTAINER

import numpy as np
import pandas as pd
import random
import itertools as itr
import time
import tracemalloc
import math
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from scipy import stats
from seaborn import boxplot
from matplotlib import pyplot
sns.set(color_codes=True)
sns.set(style="darkgrid")




class METAHEURISTIC_SOLUTION():
    def __init__(self, meta_Container=None, meta_BOX=None, coefficients=None, testConfig=None, name=None): 
        
        self.metaheuristicName = name
        self.testConfig = testConfig
        self._meta_container = meta_Container
        self._meta_boxes = meta_BOX
        self._boxesOrdered = []
        self._listOfAllBoxes = []
        
        self._mean = 0
        self._deviation = 0
        self._best_fit = 0
        
        self.coefficients = coefficients
   
    def fitness_volume(self, meta_cntnr):
        meta_cntnr._loadedVolume = meta_cntnr.getTotalVolumeBoxesContainer()
        fitValue = (meta_cntnr._loadedVolume / meta_cntnr._MaxWeight * 100)
        return fitValue
        
    def fitness_weight(self, meta_cntnr):
        meta_cntnr._loadedWeight = meta_cntnr.getTotalWeightContainer();
        fitValue = (meta_cntnr._loadedWeight / meta_cntnr._MaxVolume * 100)
        return  fitValue
    
    def fitness_gravity_center(self, meta_cntnr):
        #return ((self._height*1.5 - ((self._loadedWeight * ) /) / self._height) *100)
        
        return 0;
    
    def fitness_value(self, meta_cntnr):
        meta_cntnr._loadedPrice = meta_cntnr.getTotalPriceContainer();
        
        if (self._meta_container._loadedPrice > self._meta_container._MaxPrice):
            self._meta_container._loadedPrice = 0
            
        fitValue = (meta_cntnr._loadedPrice / meta_cntnr._MaxPrice * 100)
        return  fitValue



         
    def fitness_volume(self):
        self._meta_container._loadedVolume = self._meta_container.getTotalVolumeBoxesContainer()
        if (self._meta_container._loadedVolume > self._meta_container._MaxVolume):
            self._meta_container._loadedVolume = 0
            
        fitValue = (self._meta_container._loadedVolume / self._meta_container._MaxWeight * 100)
        return fitValue
        
    def fitness_weight(self):
        self._meta_container._loadedWeight = self._meta_container.getTotalWeightContainer();
    
        if (self._meta_container._loadedWeight > self._meta_container._MaxWeight):
            self._meta_container._loadedWeight = 0
        
        fitValue = (self._meta_container._loadedWeight / self._meta_container._MaxVolume * 100)
        return  fitValue
    
    def fitness_gravity_center(self):
        #return ((self._height*1.5 - ((self._loadedWeight * ) /) / self._height) *100)
        
        return 0;
    
    def fitness_value(self):
        self._meta_container._loadedPrice = self._meta_container.getTotalPriceContainer();
        fitValue = (self._meta_container._loadedPrice / self._meta_container._MaxPrice * 100)
        return  fitValue
        
        
    #Fitness function for this problem statement is to maximize TOTAL PRICE!
    #def fitness_function(self):
    def score(self):
        self._coef_volume = self.coefficients[0]
        self._coef_weight = self.coefficients[1]
        self._coef_gravity = self.coefficients[2]
        self._coef_value = self.coefficients[3]
    
        self._obj_value = (self._coef_volume * self.fitness_volume() + 
                          self._coef_weight * self.fitness_weight() + 
                          self._coef_gravity * self.fitness_gravity_center() + 
                          self._coef_value * self.fitness_value()) / (self._coef_volume + 
                          self._coef_weight + self._coef_gravity + self._coef_value)
        
        return self._obj_value  

    def plotHistogram(self, Final_solutions):
        i=0
        values=[]
        for i in range(len(Final_solutions)):
            values.append(Final_solutions[i][0][0])
                          
        fig, (ax1) = plt.subplots(1, 1, figsize=(15, 5))
        sns.distplot(values, ax=ax1)
        plt.title('Distribuition of Obj Function for different Initializations')
        plt.ylabel('Probability density')
        plt.xlabel('Obj Function Values')
        plt.show()

        
    def statistics(self, Final_solutions, convergence, CPUstats): 
        self._mean = 0
        self._deviation = 0
        self._best_fit = 0
        
        #Find best solutions results
        rankedB = sorted(Final_solutions, key = lambda x: x[:][0][0], reverse=True)
        
        bestSolution = rankedB[0][0]
        indexbestSolution = rankedB[0][1]    
        
        rankedW = sorted(Final_solutions, key = lambda x: x[:][0][0], reverse=False)
        
        worstSolution = rankedW[0][0]
        indexWorstSolution = rankedW[0][1] 
        
        i=0
        values=[]
        for i in range(len(Final_solutions)):
            values.append(Final_solutions[i][0][0])
            
        mean = np.average(values)
        deviation = np.std(values)
        
        i=0
        memCPU=[]
        for MEM in CPUstats:
            memCPU.append(MEM[0])
        
        meanMEMCPU = np.average(memCPU)
        devMEMCPU = np.std(memCPU)
        
        #print("memCPU: ", memCPU)
        
        rank = sorted(memCPU, key = lambda x: x, reverse=True)
        #print("rankMEM: ", rank)
        bestMEMCPU = rank[0]
        worstMEMCPU = rank[len(rank) - 1]
        
        i=0
        timeCPU=[]
        for timeC in CPUstats:
            timeCPU.append(timeC[1])
        
        #print("timeCPU: ", timeCPU)

        meanTIMECPU = np.average(timeCPU)
        devTIMECPU = np.std(timeCPU)    

        rank = sorted(timeCPU, key = lambda x: x, reverse=True)
        #print("rankTIME: ", rank)
        bestTIMECPU = rank[0]
        worstTIMECPU = rank[len(rank) - 1]
        

        
        i=0
        total_price_loadded = 0 
        for box in bestSolution[2:]:
            total_price_loadded += box[0]._price

        i=0
        total_volume_loadded = 0 
        for box in bestSolution[2:]:
            total_volume_loadded += box[0]._volume
            
        i=0
        total_weight_loadded = 0 
        for box in bestSolution[2:]:
            total_weight_loadded += box[0]._weight
            
            
        i=0
        worst_total_price_loadded = 0 
        for box in worstSolution[2:]:
            worst_total_price_loadded += box[0]._price

        i=0
        worst_total_volume_loadded = 0 
        for box in worstSolution[2:]:
            worst_total_volume_loadded += box[0]._volume
            
        i=0
        worst_total_weight_loadded = 0 
        for box in worstSolution[2:]:
            worst_total_weight_loadded += box[0]._weight
            
            
        print("************ " + self.metaheuristicName + " STATISTICS ****************")
        print("-----TEST SETTINGS --------")

        
        for key, value in self.testConfig.items() :
            print (key, ':', value)
        
        #print("Max iterations: ", testConfigTS[0])
        #print("Max tabu size : ", testConfigTS[1])
        #print("Max Neighborhood: ", testConfigTS[2])
        #print("Max execution time (s): ", testConfigTS[3])
        print("---------------------------") 
        
        print("----- Overall Profile of Best Solutions --------")
        print("Obj Function Mean: ", mean)
        print("Obj Function Deviation: ", deviation)
        print("Max Memory Used: ", bestMEMCPU)
        print("Min Memory Used: ", worstMEMCPU)
        print("Mean Memory Used: ", meanMEMCPU)
        print("Standard Deviation of Memory Used: ", devMEMCPU)
        print("Max Time Used: ", bestTIMECPU)
        print("Min Time Used: ", worstTIMECPU)
        print("Mean Time Used: ", meanTIMECPU)
        print("Standard Deviation of Time Used: ", devTIMECPU)
        #print("Best Fit: ", self._best_fit)
        print("---------------------------") 
        print("----- Profile of Best Solution --------")
        print("Max execution time used (s): ", CPUstats[indexbestSolution][1])
        print("Memory used (MB): ", CPUstats[indexbestSolution][0])
        print("Value of Fitness Function: ", Final_solutions[indexbestSolution][0][0])
        print("Total boxes loadded: ", len(Final_solutions[indexbestSolution][0]) - 1)
        print("Total price loadded [R$]: ", total_price_loadded)
        print("Total volume loadded [cm³]: ", total_volume_loadded)
        print("Total weight loadded [Kg]: ", total_weight_loadded)
        #print("Value utilization (%): ", self._mean)
        #print("Volume utilization (%): ", self._mean)
        #print("Weight utilization (%): ", self._mean)
        print("****************************************")
        
        print("----- Profile of Worst Solution --------")
        print("Max execution time used (s): ", CPUstats[indexWorstSolution][1])
        print("Memory used (MB): ", CPUstats[indexWorstSolution][0])
        print("Value of Fitness Function: ", Final_solutions[indexWorstSolution][0][0])
        print("Total boxes loadded: ", len(Final_solutions[indexWorstSolution][0]) - 1)
        print("Total price loadded [R$]: ", worst_total_price_loadded)
        print("Total volume loadded [cm³]: ", worst_total_volume_loadded)
        print("Total weight loadded [Kg]: ", worst_total_weight_loadded)
        #print("Value utilization (%): ", self._mean)
        #print("Volume utilization (%): ", self._mean)
        #print("Weight utilization (%): ", self._mean)
        print("****************************************")
        
        
        plt.plot(convergence[indexbestSolution])
        plt.title('Convergence of Best Solution')
        plt.ylabel('Obj Function')
        plt.xlabel('Iteractions')
        plt.show()

        plt.plot(convergence[indexWorstSolution])
        plt.title('Convergence of Worst Solution')
        plt.ylabel('Obj Function')
        plt.xlabel('Iteractions')
        plt.show()
        
        self.plotHistogram(Final_solutions)
        
        
        #fig, (ax1) = plt.subplots(1, 2, figsize=(20, 6))
        #sns.distplot(memCPU, ax=ax1)
        sns.distplot(memCPU)
        plt.title('Distribuition of Memory Utilization for different Initializations')
        plt.ylabel('Probability density')
        plt.xlabel('Memory (MB)')
        plt.show()
        
        #fig, (ax2) = plt.subplots(1, 2, figsize=(20, 6))
        #sns.distplot(timeCPU, ax=ax2)
        sns.distplot(timeCPU)
        plt.title('Distribuition of Time (s) values for different Initializations')
        plt.ylabel('Probability density')
        plt.xlabel('Time (s)')
        plt.show()
        
        
    #get the input string name of parameters and transforms it to an acronym to abrevviate in graphs    
    def acronym(self, textUpperCase):
        glue = ' '
        words =  ''.join(glue + x if x.isupper() else x for x in textUpperCase).strip(glue).split(glue)
        acr = ""
        for upper in words:
            acr += upper[0]
            
        return acr        

    def statisticsParameterVariation(self, data):
        
        OF_values = []
        for i in range(len(data)):
            OF_values.append(data[i][0])
            
        MEM_values = []
        for i in range(len(data)):
            MEM_values.append(data[i][1][0])

        TIME_values = []
        for i in range(len(data)):
            TIME_values.append(data[i][1][1])
            
        
        parameters = []
        for i in range(len(data)):
            parameters.append(data[i][2])
        
        listVarParam = []
        for prm in parameters:
            strParam = ""
            if self.metaheuristicName == 'TABU SEARCH':
                
                if 'MaxSolutionsTS' in prm:
                    acr = self.acronym('MaxSolutionsTS')
                    strParam += acr + "=" + str(prm['MaxSolutionsTS']) + "\n"
                    
                if 'MaxNeighborhoodTS' in prm:
                    acr = self.acronym('MaxNeighborhoodTS')
                    strParam += acr + "=" +  str(prm['MaxNeighborhoodTS']) + "\n"
                    
            
            if self.metaheuristicName == 'ADAPTIVE CUCKOO SEARCH':
                if 'populationSizeACS' in prm:
                    acr = self.acronym('populationSizeACS')
                    strParam += acr + "=" +  str(prm['populationSizeACS']) + "\n"        
    
                if 'p_a_ACS' in prm:
                    acr = self.acronym('p_a_ACS')
                    strParam += acr + "=" +  str(prm['p_a_ACS']) + "\n"
                    
                if 'lambdaACS' in prm:
                    acr = self.acronym('lambdaACS')
                    strParam += acr + "=" +  str(prm['lambdaACS']) + "\n"
                
            listVarParam.append(strParam)
            
       
        if self.metaheuristicName == 'TABU SEARCH':   
            print("*********** LIST OF ABREVIATIONS ***********")
            print(self.acronym('MaxSolutionsTS') + " = MaxSolutionsTS")
            print(self.acronym('MaxNeighborhoodTS') + " = MaxNeighborhoodTS")
            print("********************************************")
        
        if self.metaheuristicName == 'ADAPTIVE CUCKOO SEARCH':
            print("*********** LIST OF ABREVIATIONS ***********")
            print(self.acronym('populationSizeACS') + " = populationSizeACS")
            print(self.acronym('p_a_ACS') + " = p_a_ACS")
            print(self.acronym('lambdaACS') + " = lambdaACS")
            print("********************************************")       
            
        #PLOT THE OBJECTIVE FUNCTION VALUES FOR DIFFERENT PARAMETER VARIATION 
        #data = {'C=10\nP=12\npa=0.25':20, 'C++':15, 'Java':30,  
        #        'Python':35}  
        
        #parameters = list(data.keys()) 
        #values = list(data.values()) 
           
        fig = plt.figure(figsize = (15, 8)) 
          
        ''' PLOT OBJECTIVE FUNCTION '''
        barplot = plt.bar(listVarParam, OF_values, color ='blue',  
                width = 0.4) 
        #red_patch = mpatches.Patch(color='red', label='Neighborhood')
        #blue_patch = mpatches.Patch(color='blue', label='The blue data')
        #plt.legend(handles=[red_patch, blue_patch])        
        plt.xlabel("Parameters Variation") 
        plt.ylabel("Objective Function Values") 
        plt.title("O.F. For Different Parameter Combinations in "+ self.metaheuristicName + " For Best Initial Solution") 
        # Turn grid on for both major and minor ticks and style minor slightly
        # differently.
        plt.grid(which='major', color='#CCCCCC', linestyle='--')
        plt.grid(which='minor', color='#CCCCCC', linestyle=':')
        fig.tight_layout() 
        
        
        for bar in barplot:
            yval = bar.get_height()*1.0
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, '%.2f' % float(yval), va='bottom') #va: vertical alignment y positional argument
         
        plt.show() 
        
        ''' PLOT MEMORY UTILIZATION '''
        fig = plt.figure(figsize = (15, 8)) 
        barplot = plt.bar(listVarParam, MEM_values, color ='red',  
                width = 0.4) 
        #red_patch = mpatches.Patch(color='red', label='Neighborhood')
        #blue_patch = mpatches.Patch(color='blue', label='The blue data')
        #plt.legend(handles=[red_patch, blue_patch])        
        plt.xlabel("Parameters Variation") 
        plt.ylabel("Memory (MB) Values") 
        plt.title("Memory Utilization For Different Parameter Combinations in "+ self.metaheuristicName + " For Best Initial Solution") 
        plt.grid(which='major', color='#CCCCCC', linestyle='--')
        plt.grid(which='minor', color='#CCCCCC', linestyle=':')
        fig.tight_layout()
        
        for bar in barplot:
            yval = bar.get_height()*1.0
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, '%.2f' % float(yval), va='bottom') #va: vertical alignment y positional argument
 
        plt.show() 
        
        
        ''' PLOT TIME UTILIZATION '''
        fig = plt.figure(figsize = (15, 8)) 
        barplot = plt.bar(listVarParam, TIME_values, color ='green',  
                width = 0.4) 
        #red_patch = mpatches.Patch(color='red', label='Neighborhood')
        #blue_patch = mpatches.Patch(color='blue', label='The blue data')
        #plt.legend(handles=[red_patch, blue_patch])        
        plt.xlabel("Parameters Variation") 
        plt.ylabel("Time (s) Values") 
        plt.title("Time Utilization For Different Parameter Combinations in "+ self.metaheuristicName + " For Best Initial Solution") 
        plt.grid(which='major', color='#CCCCCC', linestyle='--')
        plt.grid(which='minor', color='#CCCCCC', linestyle=':')
        fig.tight_layout()
        
        for bar in barplot:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0,  yval,'%.2f' % float(yval), va='bottom') #va: vertical alignment y positional argument
 
        plt.show() 
        
        
        
        
        

        
        
        
        
    def createListFromAllBoxes(self):
        i=0
        for box in self._meta_boxes:
            quantity = box[1]
            while quantity > 0:
                self._listOfAllBoxes.append(box[0])
                quantity -= 1
                
       # print("_listOfAllBoxes[0].price: ", self._listOfAllBoxes[0]._price)  
        return 1
    
    
    def printProperties(self):
        print("fitness_volume(): ", self.fitness_volume())
        
        print("fitness_weight(): ", self.fitness_weight())
        
        print("fitness_value(): ", self.fitness_value())       
        
        print("fitness_gravity_center(): ", self.fitness_gravity_center())  
        
        #return FirstSolution
        
        print("self._meta_boxes[1]._quantity= ", self._meta_boxes[1][1])
    
    def printStatistics(self):
        pass
    
    def shuffleList(self, list_boxes, number_of_changes):
       
        i=0
        while i < number_of_changes:
            index_box_a = random.randint(0,len(list_boxes)-1) 
            index_box_b = random.randint(0,len(list_boxes)-1)
            
            print("list_boxes[index_box_a] = ", list_boxes[index_box_a], "list_boxes[index_box_b]", list_boxes[index_box_b])
            
            aux_box = list_boxes[index_box_b]
            list_boxes[index_box_b] = list_boxes[index_box_a]
            list_boxes[index_box_a] = aux_box
            i += 1
    
        return list_boxes     
    
    def clearContainer(self):
        self._meta_container.clearContainer()
        
        return True
    
    def createContainerSolution(self, list_boxes):
         
        i=0;
        #for box in self._boxesOrdered:
        for box in list_boxes:  
                
            returnedValue = self._meta_container.loadBox(box)
            
            if returnedValue == False:
                pass;
                
            elif returnedValue == True:
                
                #print("CONTAINER IS FULL!")                
                
                score = self.score();
                
                self._meta_container._loadedBoxes.insert(0, score)
                
                break
                
            else:
                print("ERROR IN LOADING CONTAINER!!!")
            

        print("price of least box: ", self._meta_container._loadedBoxes[len(self._meta_container._loadedBoxes) - 1][0]._price)
        
        print("Total price loaded in container: ", self._meta_container.getTotalPriceContainer(), "Max Price of Container: ",  self._meta_container._MaxPrice)

        print("Total weight loaded in container: ", self._meta_container.getTotalWeightContainer(), "Max Weight of container: ", self._meta_container._MaxWeight)

        print("Total volume of boxes loaded in container: ;", self._meta_container.getTotalVolumeBoxesContainer(),"Max Volume of the container: ", self._meta_container._MaxVolume)
                
        print("Number of boxes packed: ", len(self._meta_container._loadedBoxes) - 1)
        
        return self._meta_container._loadedBoxes
    
        
    def compareLoaddedBoxes(self, list1, list2):
       
        if len(list1) == len(list2):
            i=0
            for i in range(len(list2)):   
                if list1[i] != list2[i]:
                    return False #Lists are not identical!
        else:
            return False
        
        return True      
           
    
    
    
    
#-------------- Metaheuristics --------------  
    
    
class TABU_SEARCH(METAHEURISTIC_SOLUTION):
    def __init__(self, meta_BOX=None, meta_Container=None,  coefficients=None, testConfig=None):
        super().__init__(meta_Container, meta_BOX, coefficients, testConfig, name="TABU SEARCH")
  
  
        self.TABU_LIST = []
        self.MaxSolutions =  testConfig['MaxSolutionsTS']
        self.MaxNeighborhood = testConfig['MaxNeighborhoodTS']
        self.MaxRunTime = testConfig['MaxRunTimeTS']
        self.MaxIterations = testConfig['MaxIterationsTS']
        
    def addInTabuList(self, list_boxes):  
       # print("tabu list")
       # print("self.MaxSolutions= ", self.MaxSolutions)
       # print("len(self.TABU_LIST)= ", len(self.TABU_LIST))
        if len(self.TABU_LIST) > 0:    
            for listOfLoaddedBoxes in self.TABU_LIST:                           
                if self.compareLoaddedBoxes(list_boxes[1:], listOfLoaddedBoxes[1:]) == True: #Compare if two lists are identical
                    #print("There is another equal solution already added in tabu list!")
                    return False #There is another equal solution in tabu list and it will not be replicated!
                
            if (len(self.TABU_LIST) < self.MaxSolutions):   
                #print("added in tabu list of lenght: ", len(self.TABU_LIST))                    
                self.TABU_LIST.append(list_boxes) 
                return True
                
            else:
                #print("first item removed and added in tabu list of lenght: ", len(self.TABU_LIST))
                self.TABU_LIST.pop(0) #delete first solution item loadded in tabu list and add a new one
                self.TABU_LIST.append(list_boxes) 
                return True
                                      
        self.TABU_LIST.append(list_boxes)
        #print("First tabu list added!")
        return True 




    ''' Fucntion to generate neighborhood solutions from a seed list '''
    def generateNeighborhood(self, SeedList):
        step = 5
        times = 10
        
        tempList = []
        tempList = SeedList
        neighborhoodLists = []
        neighborhoodLists.append(tempList)
        
        j=0
        k=j+step
        l=k+3*step
        m=l+step
        
        for i in range(self.MaxNeighborhood -1):
            
            for n in range(times):
                if m < len(SeedList):
                    swap_a = tempList[j]
                    tempList[j] = tempList[k]
                    tempList[k] = swap_a  
                    
                    swap_a = tempList[l]
                    tempList[m] = tempList[l]
                    tempList[l] = swap_a   
                    
                    j += 1
                    k=j+step
                    l=k+10*step
                    m=l+step
                    
                else:
                    break

            neighborhoodLists.append(tempList)
                            
        return neighborhoodLists
    
    
    def rankSolutions(self, Solutions):
        #bestSolution = []
        #bestSolution.append(Solutions[0])
        rankedSol = sorted(Solutions, key = lambda x: x[0][0], reverse=True);
       
        return rankedSol
    
    def rankFinalSolutions(self, Solutions):
        #bestSolution = []
        #bestSolution.append(Solutions[0])
        rankedSol = sorted(Solutions, key = lambda x: x[0], reverse=True);
       
        return rankedSol       
    
    def diversifySearch(self):
        pass    


    def getSolutions(self, InitialSolution):
        start=time.time()   #init timer
        tracemalloc.start() #Check memory usage
        
        print("\n---------------------TABU SEARCH-------------------------------------\n")
    
        self.createListFromAllBoxes()
            
        FinalSolution = []
        loaddedSolutions = []
        rankedSolutions = []
        convergence = []
        
        #Start loading sequence by max box values
        #OneListSolution = sorted(self._listOfAllBoxes, key = lambda x: x._price, reverse=True)
        OneListSolution = InitialSolution
        
        oneLoaddedSolution = self.createContainerSolution(OneListSolution)
        self.addInTabuList(oneLoaddedSolution)
        
        convergence.append(oneLoaddedSolution[0])
    
        #return oneLoaddedSolution
    
        iterations = 1;
        while iterations <= self.MaxIterations and time.time() <= (start + self.MaxRunTime):
            
            ''' GENERATE NEIGHBORHOOD FROM FIRST SOLUTION (INTENSIFICATION SEARCH) '''
            NeighborhoodLists = self.generateNeighborhood(OneListSolution)
            
            indexNeighborhood=0
            for oneLoad in NeighborhoodLists:  
                self.clearContainer()
                oneSolution = self.createContainerSolution(oneLoad);
                loaddedSolutions.append([oneSolution, indexNeighborhood])
                indexNeighborhood +=1
                        
            rankedSolutions = self.rankSolutions(loaddedSolutions)
            
            
            ''' ADD BEST SOLUTION TO TABU LIST '''
            i=0
            #SEARCH FOR THE NEXT BEST RANKED SOLUTION THAT ISN'T ALREADY IN TABU LIST                
            while (self.addInTabuList(rankedSolutions[i][0]) == False):
                if (i + 1) < len(rankedSolutions):
                    i += 1
                    #Update index from current best solution
                    indexNeighborhood = rankedSolutions[i][1]
                    
                else:
                    break
            
            ''' BEST NEIGHBORHOOD SOLUTION IS THE NEW SEED IN SEARCH SPACE '''
            #print("\n\n indexNeighborhood: \n\n", indexNeighborhood)
            OneListSolution = NeighborhoodLists[indexNeighborhood - 1]
            
            convergence.append(rankedSolutions[0][0][0]) #get the objective function value through iteractions
            
            ''' START DIVERSIFICATION SEARCH '''
            random.shuffle(OneListSolution) 
            #OneListSolution = diversifySearch(OneListSolution)
      
            
            iterations += 1
            
        ranked = []
        ranked = self.rankFinalSolutions(self.TABU_LIST)
        
        convergence.append(ranked[0][0])
        
        FinalSolution = ranked[0]
        
        #self.printProperties(FinalSolution)
        
        #self.printStatistics()
       
        
        current, peak = tracemalloc.get_traced_memory()
        print(f"TABU SEARCH: Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        tracemalloc.stop() #stop memory usage tracking
        
        tm = (time.time() - start) 
        print("TABU SEARCH: Current time comsumption was: {%H}", tm)
        
        print("\n\n----------------------------------------------------------------------\n\n")
        
        
        CPUutilization=[]
        CPUutilization.append(current/10**6)
        CPUutilization.append(tm)
        #return self.TABU_LIST
        return FinalSolution, convergence, CPUutilization
    
    
    
    



   

class ADAPTIVE_CUCKOO_SEARCH(METAHEURISTIC_SOLUTION):
    def __init__(self, meta_BOX=None, meta_Container=None,  coefficients=None, testConfig=None):
        super().__init__(meta_Container, meta_BOX, coefficients, testConfig, name="ADAPTIVE CUCKOO SEARCH")

        self.MaxPopulation = testConfig['populationSizeACS']
        self.MaxRunTime = testConfig['MaxRunTimeACS']
        self.MaxIterations = testConfig['MaxIterationsACS']
        self.p_a = testConfig['p_a_ACS']
        self.lambdaACS = testConfig['lambdaACS']
        self.stepSize = 5
        self.dimension = 1
    
    def levy_flight(self):
        #generate step from levy distribution
        sigma1 = np.power((math.gamma(1 + self.lambdaACS) * np.sin((np.pi * self.lambdaACS) / 2)) \
                          / math.gamma((1 + self.lambdaACS) / 2) * np.power(2, (self.lambdaACS - 1) / 2), 1 / self.lambdaACS)
        sigma2 = 1
        u = np.random.normal(0, sigma1, size=self.dimension)
        v = np.random.normal(0, sigma2, size=self.dimension)
        step = u / np.power(np.fabs(v), 1 / self.lambdaACS)
    
        return step    

    
    def localRandomMove(self):
        pass
  
    def globalRandomMove(self, oneListSolution):
        
        #use levy_flight() function to move!
        tempSol = []
        i=0
        for cuckoo in oneListSolution:
            tempSol.append([cuckoo, i + self.stepSize*self.levy_flight()])
            i +=1
        
        #RANKED ORDER VALUE (ROV)
        tempSol = sorted(tempSol, key = lambda x: x[:][1], reverse=False);
        
        newSol = []        
        for item in tempSol:
            newSol.append(item[0])

        return newSol
    


    def getSolutions(self, initialSolution):
        
        start=time.time()   #init timer
        tracemalloc.start() #Check memory usage 
        CPUutilization=[]
        print("\n----------------------CUCKOO SEARCH------------------------------------\n")
     
        self.createListFromAllBoxes()
        
        self.clearContainer()
           
        Nests = []
        FinalSolution = []
        #OneListSolution = sorted(self._listOfAllBoxes, key = lambda x: x._price, reverse=True)   
        
        OneListSolution = initialSolution

        ''' Create Initial Solutions (Nests) '''
        Nests.append(OneListSolution)
        #create random initial list of all possible solutions
        for i in range(1, self.MaxPopulation):
            random.shuffle(OneListSolution)
            Nests.append(OneListSolution)
 
        #load nest to container that will fit to size and other constrains
        loadded_container_nest = []
        for i in range(len(Nests)):
            self.clearContainer()
            loadded_container_nest.append([self.createContainerSolution(Nests[i]), i])

        ''' Sort List '''        
        loadded_container_nest = sorted(loadded_container_nest, key = lambda x: x[:][0], reverse=False)

        ''' Find Initial Best'''
        bestSolutionNest = loadded_container_nest[0][0]
        bestPosition = Nests[loadded_container_nest[0][1]] #Actualy stores the sequence list that generate the actual loading container that maximizes objective function!

        convergence = []
        
        convergence.append(bestSolutionNest[0])
        
        newNest = []
        solutionNests = []

        iterations = 0;
        while iterations <= self.MaxIterations and time.time() <= (start + self.MaxRunTime):
            
            ''' Generate New Solutions '''
            for i in range(len(Nests)):
                
                ''' Get Cuckoo: set new position by levy_flight() function and evaluate obj function'''
                tempNest = self.globalRandomMove(Nests[i])
                self.clearContainer()
                newNest = self.createContainerSolution(tempNest)
                
                #random choice
                j = np.random.randint(0, len(Nests))
                while j == i:
                    j = np.random.randint(0, len(Nests))
                
                self.clearContainer()
                otherNest = self.createContainerSolution(Nests[j])

                ''' Random position Choice and compare with current obj function '''
                if(newNest[0] > otherNest[0]):    
                    Nests[j] = tempNest

            loadded_container_nest = []
            for i in range(len(Nests)):
                self.clearContainer()
                loadded_container_nest.append([self.createContainerSolution(Nests[i]), i])

            ''' Sort solutions according to objective function '''
            loadded_container_nest = sorted(loadded_container_nest, key = lambda x: x[:][0], reverse=False)      
            
            ''' Based on probability, abandon nests (create new positions), except the best current solution '''
            for i in range(1, len(loadded_container_nest)):
                if i != loadded_container_nest[0][1]:
                    rdn = np.random.rand()
                    if(rdn < self.p_a):
                        random.shuffle(Nests[i]) #abandon nest, or, in other words, create a new solution
                        self.clearContainer()
                        loadded_container_nest[i][0] = self.createContainerSolution(Nests[i])
                        loadded_container_nest[i][1] = i
            
            
            ''' Sort solutions according to objective function '''
            loadded_container_nest = sorted(loadded_container_nest, key = lambda x: x[:][0], reverse=False)             
            
          
            ''' Get best current fitnes and position from current cuckoo solutions for next iteration comparisons '''
            if bestSolutionNest[0] < loadded_container_nest[0][0][0]:
                bestSolutionNest = loadded_container_nest[0][0]
                bestPosition = Nests[loadded_container_nest[0][1]] #Actually stores the sequence list that generate the actual loading container that maximizes objective function!
            
            convergence.append(bestSolutionNest[0])
            
            iterations += 1;
    

    
        current, peak = tracemalloc.get_traced_memory();
        print(f"CUCO SEARCH: Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        tracemalloc.stop() #stop memory usage tracking
        
        tm = (time.time() - start) 
        print("CUCKOO SEARCH: Current time comsumption was: {%H}", tm)
        print("\n\n-----------------------------------------------------------------------\n\n")
        
        
        CPUutilization=[]
        CPUutilization.append(current/10**6)
        CPUutilization.append(tm)
        
        return bestSolutionNest, convergence, CPUutilization
    
    
    
