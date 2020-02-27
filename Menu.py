#coding: utf-8
import time
from Heuristic import Heuristic
class Menu:

    def __init__(self,path):
        
        self.__HeurAux = Heuristic(path)#chama a heuristica construtiva
        self.__current_selection = -1 #seleção diferente das outras possiveis seleções
    def __PrintMenu(self):
        print("HEURISTICS FOR TRAVELING SALESMAN PROBLEM")
        print("0 : Exit")
        print("1 : Nearest Neighbor")
        print("2 : Cheapest Insertion")
        print("3 : Hungry Nearest Neighbor from all cities best and worst")
        self.__current_selection = int(input("Choose one :"))

    def __PrintRefineMenu(self):
        print("CHOOSE A REFINE METHOD FOR TRAVALERSALESMAN")
        print("0 : Non")
        print("1 : UP/DOWN HILL  FOR TRAVELER SALESMAN")
        print("2 : FIRST BETTER")
        print("3 : RANDOM")
        print("4 : VNS")
        print("5 : VND")
        self.__current_refine_selection = int(input("Choose one :"))

    def Start_Menu(self):
        menu = True
        while(menu):
            self.__PrintMenu()

            if(int(self.__current_selection==0)):# EXIT
                menu = False
                return
            elif(int(self.__current_selection) in self.__HeurAux.MethodsOptions and int(self.__current_selection)!= 4):
                self.__PrintRefineMenu()
                result = self.__HeurAux.ExecuteMethods(int(self.__current_selection))  
                if (result != False and self.__current_selection <3):
                    print("Solution Cost: ",result[0][0])
                    print("The Solution : ",result[0][1])
                    print("Execution Time : ",result[1])
                    resultRaux = [result[0][0],result[0][1]]
                    if(int(self.__current_refine_selection!=0) and (int(self.__current_refine_selection) in self.__HeurAux.RefineOptions)):
                        resultRf = self.__HeurAux.ExecuteRefineMethods(int(self.__current_refine_selection), resultRaux)
                        print("Solution Cost after refine: ", resultRf[0][0])
                        print("The Solution after refine: ", resultRf[0][1])
                        print("Execution Time after refine : ", resultRf[1])



