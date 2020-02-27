#coding: utf-8
import random
import time
import re
class Heuristic:

    def __init__(self, filepath):
        self.__path = filepath
        self.__CitiesMatrix=[[],[]] #matriz coordenadas
        self.__DistanceMatrix =[[]]
        self.__num_cities = 0
        self.__InitializeCities()
        self.__InitializeDistances()
        self.MethodsOptions = [1,2,3,4]
        self.RefineOptions = [1,2,3,4,5]

    def __InitializeCities(self):
        arq = open(self.__path, 'r') #le o arquivo txt para "arq" 
        cities = arq.readlines() #vetor de strings em que cada string é uma linha do arquivo
        arq.close #fecha o arquivo
        self.__num_cities = len(cities) #numero de cidades é dado pelo tamanho do vetor de strings "cities"
        for i in range(self.__num_cities): # for de i=0 até i=numero de cidades
            aux = re.findall(r'\d+', cities[i])
            self.__CitiesMatrix[0].append(float(aux[1]))
            self.__CitiesMatrix[1].append(float(aux[2]))#valor y vai para a segunda "" ""


    def __InitializeDistances(self):
        for i in range(self.__num_cities):
            self.__DistanceMatrix.append([]) #incrementa dinamicamente uma linha 
            for j in range(self.__num_cities): # for j de zero ate num de cid, dentro de for i de zero até num d cid
                if i != j: #se a distancia a ser calculada não for para a propria cidade
                    xA = self.__CitiesMatrix[0][i]
                    xB = self.__CitiesMatrix[0][j]
                    yA = self.__CitiesMatrix[1][i]
                    yB = self.__CitiesMatrix[1][j] #variaveis auxiliares para as componentes x e y de duas cidades
                    self.__DistanceMatrix[i].append((((xA-xB)**2) + ((yA-yB)**2))**(1/2))#preenchimento da matriz distancia
                else:
                    self.__DistanceMatrix[i].append(0) #valor pra diagonal principal
        self.__DistanceMatrix.pop() #exclusao de tupla vazia

    def __InsertionCost(self, indexI,indexJ,indexK):
        dik = self.__DistanceMatrix[indexI][indexK]
        dkj = self.__DistanceMatrix[indexK][indexJ]
        dij = self.__DistanceMatrix[indexI][indexJ]
        return dik + dkj - dij      #Calculo do custo da inserção de uma cidade de indexK entre as de index I e J

    def RandomHeuristic(self):#inclui todas as cidades em um vetor, embaralha, passa nas cidades referentes as posições do vetor em ordem crescente
        #self.testfunction()
        random_numbers = [] #vetor para as cidades aleatorias
        for i in range(self.__num_cities): random_numbers.append(i) # Insere numeros de 0 a Num_cities
        random.shuffle(random_numbers) #shuffle nos elementos, agora esse é o vetor de cidades a serem visitadas
        cost = 0
        for i in range(self.__num_cities):
            if(i==self.__num_cities-1):
                cost += self.__DistanceMatrix[random_numbers[i]][random_numbers[0]] 
                random_numbers.append(random_numbers[0]) #Na ultima iteração volta para a primeira cidade
            else:
                cost += self.__DistanceMatrix[random_numbers[i]][random_numbers[i+1]] #Calcula o custo
        result = cost, random_numbers
        return result
    
    def testfunction(self): #Função para testes do slide
        self.__DistanceMatrix = [[0,2,1,4,9,1],[2,0,5,9,7,2],[1,5,0,3,8,6],[4,9,3,0,2,6],[9,7,8,2,0,2],[1,2,6,6,2,0]]

    def __InsertionCostSelect(self,insertioncostvector,alpha,num_cities_visited):
        sortedvector = sorted(insertioncostvector,key=lambda x: x[0])
        lenght = int(1 + alpha*(self.__num_cities - num_cities_visited - 1))
        testesort2 = []
        for i in range(lenght):
            testesort2.append(sortedvector[i])
        testesort2 = random.choice(testesort2)
        number = []
        number.append(testesort2[2]) # cidade a ser inserida 
        number.append(testesort2[1]) #j+1
        return number
        
    def Cheapest_Insertion(self,tcities,alpha): 
        if(alpha==1):
            return self.RandomHeuristic()
        #self.testfunction() 
        if(len(tcities)!=3):
            return False
        visited_cities = []
        visited_cities.append(tcities[0])
        visited_cities.append(tcities[1])
        visited_cities.append(tcities[2])
        num_cities_visited = 0
        for k in range(self.__num_cities-num_cities_visited):
            haschanges = False
            min_value_aux = 9999999
            min_value_indexes= [-1,-1] # vetor de indices que indica na posicao 0 a posicao em que a cidade será inserida e na posicao 1 qual a cidade
            insertioncost = []
            insertioncost.append([])
            count =0 
            for i in range((self.__num_cities)):#tentar inserir todas as cidades no vetor de entre as cidades visitadas e pegar o melhor custo
                if(i not in visited_cities):
                    for j in range(len(visited_cities)-1):
                        insertioncost[count].append(self.__InsertionCost(visited_cities[j],visited_cities[j+1],i)) #Custo da inserção de i entre j e j+1
                        indextest = j
                        insertioncost[count].append(j+1) #posicao a ser inserida
                        insertioncost[count].append(i) #cidade
                        haschanges = True
                        insertioncost.append([])
                        count=count+1
                            #if(insertioncost < min_value_aux): 
                            #    min_value_aux = insertioncost 
                            #    min_value_indexes[0] = j+1 #posicao onde será inserida
                            #    min_value_indexes[1] = i #cidade a ser inserida
            insertioncost.pop()
            if(haschanges):
                    cityToUse = self.__InsertionCostSelect(insertioncost,alpha,num_cities_visited)
                    num_cities_visited = num_cities_visited + 1
                    min_value_indexes[1] = cityToUse[0] #cidade a ser inserida                    
                    min_value_indexes[0] = cityToUse[1] #posicao onde será inserida j+ 1
                    visited_cities.insert(min_value_indexes[0],min_value_indexes[1])
            cost=0
        visited_cities.append(visited_cities[0])
        for i in range(len(visited_cities)-1):
            cost += self.__DistanceMatrix[visited_cities[i]][visited_cities[i+1]] #calculo do custo de acordo com as cidades visitadas
        result = cost, visited_cities
        return result
    
    def CityToInsert(self,k,alfa,visited_cities,num_cities_visited): 
        #k - indice fixo da matriz de distancia, alfa - coeficiente de randomicidade
        lenght = int(1 + alfa*(self.__num_cities - num_cities_visited - 1)) #quantidade de cidades a serem randomizadas
        teste = []#custos de distancias para as cidades possibilidades
        for i in range(lenght) : teste.append(99999) #inicializa o vetor com valores de distancia absurdos
        indextest=[] #indexes das cidades a serem randomizadas 
        for  i in range (self.__num_cities):
            for j in range(lenght):
                if(self.__DistanceMatrix[k][i]==0): #ignorar a diagonal principal
                    break
                if(self.__DistanceMatrix[k][i]<=teste[j] and i not in visited_cities): #Verificar se a distancia atual é menor que as distancias existentes
                    teste.insert(j,self.__DistanceMatrix[k][i]) #insere o custo
                    indextest.insert(j,i) #insere a cidade
                    break
        testesort2=[]
        for i in range (lenght): # Para parsear apenas a quantidade de valores requeridos
            testesort2.append(indextest[i])
        number = random.choice(testesort2) #escolher aleatoriamente um numero
        return number

    def Nearest_neighborHeuristic(self,city,alfa):
        #self.testfunction()
        if(alfa==1):
            return self.RandomHeuristic() #funcao melhorada para totalmente randômico
        visited_cities = [] #inicializa o vetor cidades visitadas
        cost = 0   #inicializa custo
        visited_cities.append(city) #adiciona a cidade inicial
        atual_city_aux = city #utiliza a cidade inicial como auxiliar para as varreduras
        for i in range(self.__num_cities):
            min_value_aux = 9999999999
            min_value_index = -1
            if(i==self.__num_cities-1): # Para a volta da cidade inicial
                visited_cities.append(city)
                cost += self.__DistanceMatrix[city][visited_cities[i]]
            else:
                min_value_index = self.CityToInsert(atual_city_aux,alfa,visited_cities,i) #Insere a cidade  
                min_value_aux = self.__DistanceMatrix[atual_city_aux][min_value_index] #Insere o custo
                visited_cities.append(min_value_index) #insere no vetor de cidades ja visitadas
                cost += min_value_aux
                atual_city_aux = min_value_index #atualiza a cidade que define a iteração
        result = cost, visited_cities
        return result


    def Nearest_neighbor_DownHill_Refine(self, S0):
        cost = S0[0]

        currentSolution = S0[1]

        betterSol = True
        while(betterSol):
            Solutions = []
            l = 0 #usado para contar quantas vizinhos com custo menor foram achados
            i=0
            j=0
            for i in range(self.__num_cities-2):# numero de cidades menos 2 para chegar no penultimo elemento
                j=i
                for j in range(self.__num_cities-1):#nuero de cidades menos 1 para chegar no ultimo elemento
                    auxCost = 0
                    auxSolution = currentSolution.copy()

                    if((j != i) and i==0):#se for com o primeiro elemento lembrar de colocar o primeiro elemento na ultima posição tambem
                        aux1 = auxSolution[i]
                        aux2 = auxSolution[j]
                        auxSolution[i] = aux2
                        auxSolution[j] = aux1
                        auxSolution[self.__num_cities] = aux2  # troca o ultimo elemento que é igual ao primeiro elemento

                    elif(j != i):
                        aux1= auxSolution[i]
                        aux2= auxSolution[j]
                        auxSolution[i] = aux2
                        auxSolution[j] = aux1


                    auxCost = self.pathCost(auxSolution)
                    if(auxCost < cost):


                        Solutions.append((auxCost,auxSolution))
                        l+=1
            print("tamanho de l", l)
            if(int(l==0)):
                betterSol = False
            else:

                menores=[]
                caminhos = []


                for laux in range(l):
                    menores.append(Solutions[laux][0])
                    caminhos.append(Solutions[laux][1])
                cost = min(menores)
                indice = menores.index(min(menores))
                currentSolution= caminhos[indice]
            Solutions.clear()
        return [cost, currentSolution]


    def FirstBetter(self, S0):
        cost = S0[0]

        currentSolution = S0[1]

        betterSol = True
        while (betterSol):
            Solutions = []
            l = 0  # usado para contar quantas vizinhos com custo menor foram achados
            i = 0
            j = 0
            for i in range(self.__num_cities - 2):  # numero de cidades menos 2 para chegar no penultimo elemento
                j = i
                for j in range(self.__num_cities - 1):  # nuero de cidades menos 1 para chegar no ultimo elemento
                    auxCost = 0
                    auxSolution = currentSolution.copy()

                    if ((
                            j != i) and i == 0):  # se for com o primeiro elemento lembrar de colocar o primeiro elemento na ultima posição tambem
                        aux1 = auxSolution[i]
                        aux2 = auxSolution[j]
                        auxSolution[i] = aux2
                        auxSolution[j] = aux1
                        auxSolution[
                            self.__num_cities] = aux2  # troca o ultimo elemento que é igual ao primeiro elemento

                    elif (j != i):
                        aux1 = auxSolution[i]
                        aux2 = auxSolution[j]
                        auxSolution[i] = aux2
                        auxSolution[j] = aux1

                    auxCost = self.pathCost(auxSolution)
                    if (auxCost < cost):

                        l += 1
                        cost = auxCost
                        currentSolution = auxSolution
                        print("found an lower cost")
                        j = int(self.__num_cities)
                        i= int(self.__num_cities - 1)
                        #check if its right
            print("tamanho de l", l)
            if (int(l == 0)):
                betterSol = False
        return [cost, currentSolution]





    def RandomTravelerRefine(self, S0):
        maxIterations = int(input("Choose the maximum ramdom iterations for each new solution :")) #doesnt save the past ramdom selected numbers
        iterations = 0

        maxSolutionNumber = int(input("Choose the maximum number of solutions:"))  # sets the max solutions number
        solFound = 0
        cost = S0[0]

        currentSolution = S0[1]


        while ((iterations < maxIterations) and  (solFound < maxSolutionNumber)):


            auxSolution = currentSolution.copy()

            random_numbers = []  # vetor para as cidades aleatorias
            for i in range(self.__num_cities): random_numbers.append(i)  # Insere numeros de 0 a Num_cities
            random.shuffle(random_numbers) # usaremos o elemento 0 do vetor apos termos embaralhado como um numero sorteado

            if (random_numbers[0]==0):  # se a primeira posição do vetor solução foi o escolhido então temos que trocar a ultima posição tambem
                aux1 = auxSolution[0] #copia o primeiro elemento para troc
                aux2 = auxSolution[random_numbers[1]] #copia o segundo elemento para troc

                auxSolution[0] = aux2
                auxSolution[random_numbers[1]] = aux1
                auxSolution[self.__num_cities] = aux2  # troca o ultimo elemento que é igual ao primeiro elemento

            else:
                aux1 = auxSolution[random_numbers[0]]
                aux2 = auxSolution[random_numbers[1]]
                auxSolution[random_numbers[0]] = aux2
                auxSolution[random_numbers[1]] = aux1

            auxCost = self.pathCost(auxSolution)
            if (auxCost < cost):

                cost = auxCost
                currentSolution = auxSolution
                print("found an lower cost")
                solFound = solFound + 1
                iterations = 0
            iterations = iterations + 1

        return [cost, currentSolution]




    #trabalho final VND E VNS

    def VND(self,S0):
        S = S0
        k=1
        bestNeighK = []
        while (k<=6):
            if(k==1):
                bestNeighK =self.VNSNearestNb(S,0)
            elif(k==2):
                bestNeighK =self.VNS2opt(S,0)
            elif(k==3):
                bestNeighK =self.VNS3opt1(S,0)
            elif(k==4):
                bestNeighK =self.VNS3opt2(S,0)
            elif(k==5):
                bestNeighK =self.VNS3opt3(S,0)
            elif(k==6): 
                bestNeighK =self.VNS3opt4(S,0)
            if(bestNeighK!=False and bestNeighK[1]<S[1]):
                S = bestNeighK
                k=1
            else:
                k+=1
        return S

            

    def VNSNearestNb(self, S,option):

        currentSolution = S[1]
        cost = S[0]
        Solutions = []

        iaux = 0
        if (option == 1):
            iaux = random.randint(0, self.__num_cities - 1)
            jaux = random.randint(iaux + 1, self.__num_cities)
            while (iaux == jaux):
                iaux = random.randint(0, self.__num_cities - 1)

        l = 0
        for i in range(iaux,self.__num_cities - 2):  # numero de cidades menos 2 para chegar no penultimo elemento

            if(option == 0):
                jaux = i
            for j in range(jaux,self.__num_cities - 1):  # nuero de cidades menos 1 para chegar no ultimo elemento

                auxCost = 0
                auxSolution = currentSolution.copy()

                if (( j != i) and i == 0):  # se for com o primeiro elemento lembrar de colocar o primeiro elemento na ultima posição tambem

                    auxSolution[i] ,auxSolution[j] = auxSolution[j] ,auxSolution[i]


                    auxSolution[self.__num_cities] = auxSolution [i]  # troca o ultimo elemento que é igual ao primeiro elemento

                elif (j != i):
                    auxSolution[i], auxSolution[j] = auxSolution[j], auxSolution[i]

                auxCost = self.pathCost(auxSolution)
                if (option == 1):
                    return [auxCost, auxSolution]
                if (auxCost < cost):
                    Solutions.append((auxCost, auxSolution))
                    l += 1

        print("soluções com troca de 2:", l)

        if (int(l == 0)):
            return  False
        else:

            menores = []
            caminhos = []

            for laux in range(l):
                menores.append(Solutions[laux][0])
                caminhos.append(Solutions[laux][1])
            cost = min(menores)
            indice = menores.index(min(menores))
            currentSolution = caminhos[indice]
        Solutions.clear()
        return [cost, currentSolution]

    def VNS3opt1(self, S0,option):
        currentSolution = S0[1]
        cost = S0[0]
        Solutions = []
        iaux = 0
        if(option == 1):
            iaux = random.randint(0,self.__num_cities-6)
            jaux = random.randint(iaux+2,self.__num_cities-3)
            kaux = 48
            while(iaux==jaux):
                iaux = random.randint(0,self.__num_cities-6)
            while(jaux==kaux):
                kaux = random.randint(jaux+4,self.__num_cities-1)
        l = 0

        print(iaux )
        print(jaux)
        print(kaux)
        for i in range(iaux,self.__num_cities - 7):
            if(option==0):
                jaux = i+2
            print("entrou EM i")
            for j in range(jaux, self.__num_cities - 4):
                if(option==0):
                    kaux = j+4
                print("entrou em J")
                for k in range(kaux,self.__num_cities - 2):
                    print("entrou em k")

                    auxCost = 0
                    auxSolution = currentSolution.copy()
                    auxSolution[i+1] , auxSolution[k] = auxSolution[k],auxSolution[i+1]
                    auxSolution[j],auxSolution[j+1] = auxSolution[j+1],auxSolution[j]
                    auxSolution[j+1] , auxSolution[k] = auxSolution[k],auxSolution[j+1]

                    print(option)
                    auxCost = self.pathCost(auxSolution)

                    if(option == 1):
                        print("RETORNOUUU")
                        return [auxCost, auxSolution]
                    if (auxCost < cost):
                        Solutions.append((auxCost, auxSolution))
                        l += 1
        print("soluções com 3 opt1:", l)
        if (int(l == 0)):
            return False
        else:

            menores = []
            caminhos = []

            for laux in range(l):
                menores.append(Solutions[laux][0])
                caminhos.append(Solutions[laux][1])
            cost = min(menores)
            indice = menores.index(min(menores))
            currentSolution = caminhos[indice]
        Solutions.clear()
        return [cost, currentSolution]

    def VNS3opt2(self, S0,option):
        currentSolution = S0[1]
        cost = S0[0]
        Solutions = []
        iaux = 0
        if(option == 1):
            iaux = random.randint(0,self.__num_cities-6)
            jaux = random.randint(iaux+2,self.__num_cities-3)
            kaux = random.randint(jaux+4,self.__num_cities-1)
            while(iaux==jaux):
                iaux = random.randint(0,self.__num_cities-6)
            while(jaux==kaux):
                kaux = random.randint(jaux+4,self.__num_cities-1)
        l = 0

        for i in range(iaux,self.__num_cities - 7):
            if(option==0):
                jaux = i+2
            for j in range(jaux, self.__num_cities - 4):
                if(option==0):
                    kaux = j+4
                for k in range(kaux,self.__num_cities - 2):
                    auxCost = 0
                    auxSolution = currentSolution.copy()
                    auxSolution[i+1] , auxSolution[k] = auxSolution[k],auxSolution[i+1]
                    auxSolution[j],auxSolution[j+1] = auxSolution[j+1],auxSolution[j]
                    auxSolution[i+1] , auxSolution[j] = auxSolution[j],auxSolution[i+1]

                    auxCost = self.pathCost(auxSolution)
                    if(option==1):
                        return [auxCost,auxSolution]
                    if (auxCost < cost):
                        Solutions.append((auxCost, auxSolution))
                        l += 1
        print("soluções com 3 opt1:", l)
        if (int(l == 0)):
            return False
        else:

            menores = []
            caminhos = []

            for laux in range(l):
                menores.append(Solutions[laux][0])
                caminhos.append(Solutions[laux][1])
            cost = min(menores)
            indice = menores.index(min(menores))
            currentSolution = caminhos[indice]

        Solutions.clear()
        return [cost, currentSolution]

    def VNS3opt3(self, S0,option):
        currentSolution = S0[1]
        cost = S0[0]
        Solutions = []
        iaux = 0
        if(option == 1):
            iaux = random.randint(0,self.__num_cities-6)
            jaux = random.randint(iaux+2,self.__num_cities-3)
            kaux = random.randint(jaux+4,self.__num_cities-1)
            while(iaux==jaux):
                iaux = random.randint(0,self.__num_cities-6)
            while(jaux==kaux):
                kaux = random.randint(jaux+4,self.__num_cities-1)
        l = 0
        for i in range(iaux,self.__num_cities - 7):
            if(option==0):
                jaux = i+2
            for j in range(jaux, self.__num_cities - 4):
                if(option==0):
                    kaux = j+4
                for k in range(kaux,self.__num_cities - 2):
                    auxCost = 0
                    auxSolution = currentSolution.copy()
                    auxSolution[i+1] , auxSolution[j] = auxSolution[j],auxSolution[i+1]
                    auxSolution[j+1],auxSolution[k] = auxSolution[k],auxSolution[j+1]

                    auxCost = self.pathCost(auxSolution)
                    if(option==1):
                        return [auxCost,auxSolution]
                    if (auxCost < cost):
                        Solutions.append((auxCost, auxSolution))
                        l += 1
        print("soluções com 3 opt1:", l)
        if (int(l == 0)):
            return False
        else:

            menores = []
            caminhos = []

            for laux in range(l):
                menores.append(Solutions[laux][0])
                caminhos.append(Solutions[laux][1])
            cost = min(menores)
            indice = menores.index(min(menores))
            currentSolution = caminhos[indice]
        Solutions.clear()
        return [cost, currentSolution]

    def VNS3opt4(self, S0,option):
        currentSolution = S0[1]
        cost = S0[0]
        Solutions = []
        iaux = 0
        if(option == 1):
            iaux = random.randint(0,self.__num_cities-6)
            jaux = random.randint(iaux+2,self.__num_cities-3)
            kaux = random.randint(jaux+4,self.__num_cities-1)
            while(iaux==jaux):
                iaux = random.randint(0,self.__num_cities-6)
            while(jaux==kaux):
                kaux = random.randint(jaux+4,self.__num_cities-1)
        l = 0
        for i in range(iaux,self.__num_cities - 7):
            if(option==0):
                jaux = i+2
            for j in range(jaux, self.__num_cities - 4):
                if(option==0):
                    kaux = j+4
                for k in range(kaux,self.__num_cities - 2):
                    auxCost = 0
                    auxSolution = currentSolution.copy()
                    auxSolution[i+1] , auxSolution[j+1] = auxSolution[j+1],auxSolution[i+1]
                    auxSolution[j],auxSolution[k] = auxSolution[k],auxSolution[j]

                    auxCost = self.pathCost(auxSolution)
                    if(option==1):
                        return [auxCost,auxSolution]
                    if (auxCost < cost):
                        Solutions.append((auxCost, auxSolution))
                        l += 1
        print("soluções com 3 opt1:", l)
        if (int(l == 0)):
            return False
        else:

            menores = []
            caminhos = []

            for laux in range(l):
                menores.append(Solutions[laux][0])
                caminhos.append(Solutions[laux][1])
            cost = min(menores)
            indice = menores.index(min(menores))
            currentSolution = caminhos[indice]
        Solutions.clear()
        return [cost, currentSolution]
    # 2opt
    def VNS2opt (self, S0,option):

        currentSolution = S0[1]
        cost = S0[0]
        Solutions = []

        iaux = 0
        if (option == 1):
            iaux = random.randint(0, self.__num_cities - 1)
            jaux = random.randint(iaux + 2, self.__num_cities)

            while (iaux == jaux):
                iaux = random.randint(0, self.__num_cities - 1)

        l = 0
        for i in range(iaux, self.__num_cities - 5):
            if (option == 0):
                jaux = i + 2
            for j in range(jaux, self.__num_cities - 2):
                auxCost = 0
                auxSolution = currentSolution.copy()

                auxI = i
                auxJ = j

                while auxJ != auxI + 1:
                    auxSolution[auxI + 1], auxSolution[auxJ] = auxSolution[auxJ], auxSolution[auxI + 1]

                    if auxI + 2 == auxJ: auxJ = auxI + 1
                    else:
                        auxJ = auxJ -1
                        auxI = auxI + 1
                    if auxI == auxJ : auxJ = auxI + 1

                auxCost = self.pathCost(auxSolution)
                if (option == 1):
                    return [auxCost, auxSolution]
                if (auxCost < cost):
                    Solutions.append((auxCost, auxSolution))
                    l += 1

        print("soluções com 2 opt:", l)
        if (int(l == 0)):
            return False
        else:

            menores = []
            caminhos = []

            for laux in range(l):
                menores.append(Solutions[laux][0])
                caminhos.append(Solutions[laux][1])
            cost = min(menores)
            indice = menores.index(min(menores))
            currentSolution = caminhos[indice]
        Solutions.clear()
        return [cost, currentSolution]




    def VNS(self, S0):
        maxIterations = int(input("Choose the maximum number of iterations without result alowed :")) #doesnt save the past ramdom selected numbers

        iterations = 0

        currentSolution = S0

        kMax = 6   # mudar para o numero de movimentos


        while (iterations < maxIterations ):

            k = 3

            while k <= kMax:

                auxSolution = currentSolution.copy()
                neigborK = []
                if( k == 1 ):
                    neigborK = self.VNSNearestNb(auxSolution, 1)
                    print(neigborK)
                elif(k == 2 ):
                    neigborK = self.VNS2opt(auxSolution, 1)
                    print(neigborK)
                if (k == 3 ):
                    neigborK = self.VNS3opt1(auxSolution, 1)
                    print(neigborK)
                elif (k == 4 ):
                    neigborK = self.VNS3opt2(auxSolution, 1)
                    print(neigborK)
                elif (k == 5 ):
                    neigborK = self.VNS3opt3(auxSolution, 1)
                    print(neigborK)
                elif (k == 6 ):
                    neigborK = self.VNS3opt4(auxSolution, 1)
                    print(neigborK)

                neigborK = self.VNSNearestNb(neigborK,0)
                if(neigborK[0] < currentSolution[0]):
                    currentSolution = neigborK
                    k = 3
                    iterations = 0 # toda vez que um resultado melhor é achado em algum tipo de visinhança, resetar a variavel de controle de parada auxiliar
                else:
                    iterations = iterations + 1
                    k = k + 1
                if iterations >= maxIterations:
                    break

        return  currentSolution # return two values


    #fim do trabalho final VND E VNS



    def pathCost(self, s):
        cost = 0
        i=1
        for i in range(self.__num_cities):
            if (i != range):
                cost += self.__DistanceMatrix[s[i-1]][s[i]]
        cost += self.__DistanceMatrix[s[i-1]][s[0]]
        return int(cost)

    def ExecuteMethods(self,option):
        city = 0 #cidade inicial
        if option <3:
            alpha = float(input("Choose alpha for the heuristic: "))
        tcities = [] #vetor aux para inserção mais barata
        if(option==1): #Heuristica Vizinho Mais Próximo
            if(alpha!=1):
                print("In range [ 0 -",self.__num_cities-1,"]:")#printa o numero de cidades
                city = int(input("Choose the city for start :"))#entra com a cidade inicial
            if(city>self.__num_cities or city<0):#se a cidade inicial for invalida retorna falso
                print('Choose in range 0 - ',self.__num_cities)
                return False
            startTime = time.time()#começa contar o tempo
            result = self.Nearest_neighborHeuristic(city,alpha)#chama o methodo de construção propriamente dito
        elif(option==2): #Heuristica Inserção mais barata
            if(alpha!=1):
                print("In range [ 0 -",self.__num_cities-1,"]:")
                tcities.append(int(input("Choose the city for start: ")))
                tcities.append(int(input("Choose the next city: ")))
                tcities.append(int(input("Choose the city for the end: ")))
                if(tcities[0]>self.__num_cities or city<0):
                    print('Choose in range 0 - ',self.__num_cities)
                    return False
                if(tcities[1]>self.__num_cities or city<0):
                    print('Choose in range 0 - ',self.__num_cities)
                    return False
                if(tcities[2]>self.__num_cities or city<0):
                    print('Choose in range 0 - ',self.__num_cities)
                    return False
            startTime = time.time()
            result = self.Cheapest_Insertion(tcities,alpha)
        elif(option==3):  # Heuristica Inserção mais barata
            startTime = time.time()  # começa contar o tempo
            result = []
            for i in range(self.__num_cities):
                result.append( self.Nearest_neighborHeuristic(i, 0) ) # chama o methodo de construção propriamente dito
            endTime = time.time()
            custos = []
            for j in range(self.__num_cities):
                custos.append( result[j][0])
            print("max: ",max(custos))
            print("mix:",min(custos))
            file= open(self.__path+ "max e min","w+")
            file.write("Maior Custo: %f\r\n" % max(custos))
            file.write("cidades: %s \r\n" % result[custos.index(max(custos))][1])
            file.write("Menor Custo: %f\r\n" % min(custos))
            file.write("cidades: %s \r\n" % result[custos.index(min(custos))][1])
            file.close()


        endTime = time.time()
        endTime = endTime - startTime
        return result , endTime  #Retorna custo, solução e tempo

    def ExecuteRefineMethods(self, option, S0):
        if(int(option == 1)):
            startTime = time.time()
            result = self.Nearest_neighbor_DownHill_Refine(S0)
            endTime = time.time()
        elif(int(option == 2)):
            startTime = time.time()
            result = self.FirstBetter(S0)
            endTime = time.time()
        elif (int(option == 3)):
            startTime = time.time()
            result = self.RandomTravelerRefine(S0)
            endTime = time.time()
        elif (int(option == 4)):
            startTime = time.time()
            result = self.VNS(S0)
            endTime = time.time()
        elif (int(option == 5)):
            startTime = time.time()
            result = self.VND(S0)
            endTime = time.time()

        endTime = endTime - startTime
        return result, endTime


    def getDistanceMatrix(self):
        return self.__DistanceMatrix
    def getCitiesMatrix(self):
        return self.__CitiesMatrix
    def getNumCities(self):
        return self.__num_cities