import Heuristic
import random
import time
from OutputFileHandling import saveTestCase
class Test:

    def __init__(self,Heur_test):
        if isinstance(Heur_test,Heuristic.Heuristic):
            self.__Heur = Heur_test
        self.__options = [1,2,3,4]
        self.__current_selection=-1
        self.__index = 0
    
    def FirstTestCase(self):
        #All cities as the first city one time saving the best and worst solution found
        bestsolution = [9999999,0]
        worstsolution = [0,0]
        for i in range(self.__Heur.getNumCities()):
            result=self.__Heur.Nearest_neighborHeuristic(i,0)
            if(result[0]<bestsolution[0]):
                bestsolution = result
            if(result[0] > worstsolution[0]):
                worstsolution = result
        return bestsolution,worstsolution


    def SecondTestCase(self,executiontimes):
        #3 start cities choose randomic and execute x times saving the best worst solutions and average cost
        maxcities = self.__Heur.getNumCities()
        bestsolution = [9999999,0]
        worstsolution = [0,0]
        average = 0
        for i in range(executiontimes):
            tcities = random.sample(range(0,maxcities), 3)
            result=self.__Heur.Cheapest_Insertion(tcities,0)
            average+=result[0]
            if(result[0]<bestsolution[0]):
                bestsolution = result
            if(result[0] > worstsolution[0]):
                worstsolution = result
        average /= executiontimes
        return bestsolution,worstsolution,average
    
    def ThirdTestCase(self, executiontimes,city):
        bestsolution = [99999999999,0]
        worstsolution = [0,0]
        average = 0
        for i in range(executiontimes):
            alpha = random.random()
            result=self.__Heur.Nearest_neighborHeuristic(city,alpha)
            average+=result[0]
            if(result[0] < bestsolution[0]):
                bestsolution = result
            if(result[0] > worstsolution[0]):
                worstsolution = result
        average /= executiontimes
        return bestsolution,worstsolution,average
    def FourthTestCase(self,executiontimes,tcities):
        bestsolution = [9999999,0]
        worstsolution = [0,0]
        average = 0
        for i in range(executiontimes):
            result=self.__Heur.Cheapest_Insertion(tcities,random.random())
            average+=result[0]
            if(result[0] < bestsolution[0]):
                bestsolution = result
            if(result[0] > worstsolution[0]):
                worstsolution = result
        average /= executiontimes
        return bestsolution,worstsolution,average
    
    def __PrintMenu(self):
        print("HEURISTICS TESTS FOR TRAVELING SALESMAN PROBLEM")
        print("0 : Exit")
        print("1 : All cities NearNeighbor")
        print("2 : Random Cheapest Insertion")
        print("3 : Random alpha NearNeighbor")
        print("4 : Random alpha Cheapest Insertion")

    def Startmenu(self):
        menu = True
        while(menu):
            self.__PrintMenu()
            self.__current_selection = int(input("Choose one :"))
            if(int(self.__current_selection==0)):# EXIT
                menu = False
                return
            elif(int(self.__current_selection) in self.__options):
                result = self.__ExecuteTest(int(self.__current_selection))  

    def __ExecuteTest(self, option):
        city = 0
        tcities = []
        numcities = self.__Heur.getNumCities()
        text = ""
        if(option==1):
            startTime = time.time()
            text = "All cities NearNeighbor"
            result = self.FirstTestCase()
        elif(option==2):
            startTime = time.time()
            executiontimes = int(input("How many times ? :"))
            text = "Random Cheapest Insertion"
            result = self.SecondTestCase(executiontimes)    
        elif(option==3): #Heuristica Vizinho Mais Próximo
            print("In range [ 0 -",numcities-1,"]:")
            city = int(input("Choose the city for start :"))
            if(city>numcities or city<0):
                print('Choose in range 0 - ',numcities)
                return False
            executiontimes = int(input("How many times ? :"))
            startTime = time.time()
            text = "Random alpha NearNeighbor"
            result = self.ThirdTestCase(executiontimes,city)
        elif(option==4): #Heuristica Inserção mais barata
            print("In range [ 0 -",numcities-1,"]:")
            tcities.append(int(input("Choose the city for start: ")))
            tcities.append(int(input("Choose the next city: ")))
            tcities.append(int(input("Choose the city for the end: ")))
            if(tcities[0]>numcities-1 or city<0):
                print('Choose in range 0 - ',numcities)
                return False
            if(tcities[1]>numcities-1 or city<0):
                print('Choose in range 0 - ',numcities)
                return False
            if(tcities[2]>numcities-1 or city<0):
                print('Choose in range 0 - ',numcities)
                return False
            executiontimes = int(input("How many times ? :"))    
            startTime = time.time()
            text = "Random alpha Cheapest Insertion"
            result = self.FourthTestCase(executiontimes,tcities)
        endTime = time.time()
        endTime = endTime - startTime
        self.__index += 1
        saveTestCase(text,result,endTime,self.__index)
        return result , endTime  #Retorna custo, solução e tempo