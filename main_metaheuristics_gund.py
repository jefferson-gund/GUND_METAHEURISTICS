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
from metaheuristicsClass import TABU_SEARCH, ADAPTIVE_CUCKOO_SEARCH
import random
import datetime
import time
import tracemalloc

startTime=time.time()   #init timer
#tracemalloc.start() #Check memory usage 
#CPUutilization=[]

#Objective Function Coefficients for Price Maximization (0.0 to 1.0):
k1 = 0.4; #Volume maximization coefficient 
k2 = 0.2; #Weight maximization coefficient 
k3 = 0.0; #Gravity center maximization coefficient (NOT IMPLEMENTED!!)
k4 = 0.95; #Price maximization coefficient 

coefficients = [k1, k2, k3, k4]

#height, lenght, width [cm], MaxWeight [Kg], MaxPrice [R$]
LOADDED_CONTAINER = CONTAINER(135.0, 500.0, 108.0, 18070.0, 300000.0)

#height,lenght,width [cm], Volume [cm³], Weight [Kg], Price [R$], quantity 
BOXES = []
BOXES.append([BOX(47.7, 46.0, 36.0, 78991.2, 14.1, 1253.0), 20])
BOXES.append([BOX(41.9, 56.3, 35.8, 84451.1, 9.6,  626.0), 25])
BOXES.append([BOX(41.9, 56.3, 35.8, 84451.1, 10.0, 704.0), 20])
BOXES.append([BOX(41.9, 56.3, 35.8, 84451.1, 10.6, 791.0), 15])
BOXES.append([BOX(41.9, 56.3, 35.8, 84451.1, 10.6, 1018.0), 10])
BOXES.append([BOX(45.6, 47.3, 38.2, 82392.8, 13.7, 1488.0), 5])
BOXES.append([BOX(44.5, 44.1, 33.5, 65742.1, 10.7, 1096.0), 5])




''' ****************** TABU SEARCH ****************** '''

numberOfInitialSolutionsTS = 2
CPU_utilizationTS = []
#Simulation Parameters
MaxIterationsTS = 5
MaxSolutionsTS = 30 #size of tabu list
MaxNeighborhoodTS = 20 #size of neighborhood for intensification search
MaxRunTimeTS = 300 #Set max runtime of 5 min
#MaxMemoryUsage = 100 #100MB

parametersTS = {'MaxIterationsTS':MaxIterationsTS, 'MaxSolutionsTS':MaxSolutionsTS, 
                'MaxNeighborhoodTS':MaxNeighborhoodTS, 'MaxRunTimeTS':MaxRunTimeTS}

TABU = TABU_SEARCH(BOXES, LOADDED_CONTAINER, coefficients, parametersTS)

InitialSolution = TABU.createListFromAllBoxes()

finalTS= []
CPU_utilizationTS = []
convergenceTS = []
#Start loading sequence by max box values
InitialSolution = sorted(TABU._listOfAllBoxes, key = lambda x: x._price, reverse=True)

InitialSolutionWithOF = [] #track initial solution and objective function to further analysis

for i in range(numberOfInitialSolutionsTS):
    
    Final_solution_tabu_search, convTS, CPU_TS = TABU.getSolutions(InitialSolution)
    
    finalTS.append([Final_solution_tabu_search, i])
    CPU_utilizationTS.append(CPU_TS)
    convergenceTS.append(convTS) 
    
    InitialSolutionWithOF.append([InitialSolution, Final_solution_tabu_search[0]])
    
    random.shuffle(InitialSolution)

#Get the best initial solution
OF = []
for i in range(len(InitialSolutionWithOF)):
    OF.append(InitialSolutionWithOF[i][1])

print("OF[0]", OF[0])

indexBestInitialSolution = OF.index(max(OF))


BestInitialSolution = InitialSolutionWithOF[indexBestInitialSolution][0]


''' CREATE PARAMETER VARIATION FOR TABU SEARCH '''
#Set parameters to variate
#ListMaxSolutionsTS = [10, 20, 40, 60]
#ListMaxNeighborhoodTS = [5, 15, 30]
ListMaxSolutionsTS = [10, 60]
ListMaxNeighborhoodTS = [5, 30]

BestParametersTS = []

for TABU_SIZE in ListMaxSolutionsTS:
    for Neighbor in ListMaxNeighborhoodTS:
        
        MaxSolutionsTS = TABU_SIZE
        MaxNeighborhoodTS = Neighbor
        
        parametersTS = {'MaxIterationsTS':MaxIterationsTS, 'MaxSolutionsTS':MaxSolutionsTS, 
                'MaxNeighborhoodTS':MaxNeighborhoodTS, 'MaxRunTimeTS':MaxRunTimeTS}
        
        BEST_TABU = TABU_SEARCH(BOXES, LOADDED_CONTAINER, coefficients, parametersTS)

        #InitialSolution = TABU.createListFromAllBoxes()
        
        Best_tabu_search, BestconvTS, BestCPU_TS = TABU.getSolutions(BestInitialSolution)
        
        BestParametersTS.append([Best_tabu_search[0], BestCPU_TS, parametersTS])
        


    
 
    

    
    

''' ****************** ADAPTIVE CUCKOO SEARCH ****************** '''
numberOfInitialSolutionsACS = 2
CPU_utilizationACS = []

MaxRunTimeACS = 300
MaxIterationsACS = 5
populationSizeACS = 10
p_a_ACS = 0.21 #Portion of bad solutions
lambdaACS = 1.5 #levy flights parameter


parametersACS = {'MaxIterationsACS':MaxIterationsACS, 'MaxRunTimeACS':MaxRunTimeACS, 
                 'populationSizeACS':populationSizeACS, 'p_a_ACS': p_a_ACS, 
                  'lambdaACS':lambdaACS}


ACS = ADAPTIVE_CUCKOO_SEARCH(BOXES, LOADDED_CONTAINER, coefficients, parametersACS)

InitialSolutionACS = ACS.createListFromAllBoxes()
#Start loading sequence by max box values
InitialSolutionACS = sorted(ACS._listOfAllBoxes, key = lambda x: x._price, reverse=True)

finalACS= []
CPU_utilizationACS = []
convergenceACS = []

ACSInitialSolutionWithOF = []


for i in range(numberOfInitialSolutionsACS):
    Final_solution_adaptive_cuckoo_search, convACS, CPU_ACS = ACS.getSolutions(InitialSolutionACS)
    finalACS.append([Final_solution_adaptive_cuckoo_search, i])
    CPU_utilizationACS.append(CPU_ACS)
    convergenceACS.append(convACS)  
    
    ACSInitialSolutionWithOF.append([InitialSolutionACS, Final_solution_adaptive_cuckoo_search[0]])
    
    random.shuffle(InitialSolutionACS)




#Get the best initial solution
ACSOF = []
for i in range(len(ACSInitialSolutionWithOF)):
    ACSOF.append(ACSInitialSolutionWithOF[i][1])

print("ACSOF[0]", ACSOF[0])

indexBestInitialSolution = ACSOF.index(max(ACSOF))


BestInitialSolutionACS = ACSInitialSolutionWithOF[indexBestInitialSolution][0]



''' CREATE PARAMETER VARIATION FOR ADAPTIVE CUCKOO SEARCH '''
ListP_a_ACS = [0.1, 0.3]
ListLambdaACS = [1.0, 3.0]
ListPopulationSizeACS = [5, 10]


BestParametersACS = []


for P_a in ListP_a_ACS:
    for Lambda in ListLambdaACS:
        for pop in ListPopulationSizeACS:
        
            lambdaACS = Lambda
            p_a_ACS = P_a
            populationSizeACS = pop
            
            parametersACS = {'MaxIterationsACS':MaxIterationsACS, 'MaxRunTimeACS':MaxRunTimeACS, 
                             'populationSizeACS':populationSizeACS, 'p_a_ACS': p_a_ACS, 
                              'lambdaACS':lambdaACS}
            
            ACS = ADAPTIVE_CUCKOO_SEARCH(BOXES, LOADDED_CONTAINER, coefficients, parametersACS)
    
            #InitialSolutionACS = ACS.createListFromAllBoxes()
            
            Best_adaptive_cuckoo_search, BestConvACS, BestCPU_ACS = ACS.getSolutions(BestInitialSolutionACS)
            
            
            BestParametersACS.append([Best_adaptive_cuckoo_search[0], BestCPU_ACS, parametersACS])






''' ****************** PRINT STATISTICS ****************** '''

TABU.statistics(finalTS, convergenceTS, CPU_utilizationTS)

ACS.statistics(finalACS, convergenceACS, CPU_utilizationACS)


TABU.statisticsParameterVariation(BestParametersTS)

ACS.statisticsParameterVariation(BestParametersACS)




#current, peak = tracemalloc.get_traced_memory();
seconds = time.time() - startTime
tempo = str(datetime.timedelta(seconds=seconds))
print("\n************************************************")
print("TOTAL SIMULATION ELAPSED  TIME = ", tempo)
#print(f"TOTAL MEMORY USAGE WAS: {current / 10**6}MB; Peak was {peak / 10**6}MB")
print("************************************************\n")
#tracemalloc.stop() #stop memory usage tracking









