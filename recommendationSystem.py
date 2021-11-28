import numpy as np
import math


class RecommendationSystem:
  
  # Constructor de la clase
  def __init__(self, file, neighbors):
    self.matrix = np.loadtxt(file, dtype=str) # Matriz leida del fichero
    
    self.utilityMatrix = None # Matriz de utilidad Números enteros
    self.matrixConverter()
    
    self.sim = np.zeros((len(self.utilityMatrix), len(self.utilityMatrix[0])), dtype=float)
    
    self.simOrderByProximity = np.zeros((len(self.utilityMatrix), len(self.utilityMatrix)))
    
    self.numOfNeighbors = neighbors
    
    self.predictionMatrix = np.zeros((len(self.utilityMatrix), len(self.utilityMatrix[0])))
    
    # self.predictionDifferenceMean()
    # self.predictionSimple()
    
  def pearson(self):
    print("Pearson")
    # u y v usuarios
    numOfUsers = len(self.utilityMatrix)
    numOfItems = len(self.utilityMatrix[0])
    
    for u in range(numOfUsers):
      for v in range(numOfUsers):
        if (u == v):
          self.sim[u][v] = 1.0
        else: 
          # Suv = conjunto de items calificados por u y s
          # Creamos un array de 0's y marcamos con un 1 las calificaciones en las que u y v han calificado
          itemsCalificados = [0] * numOfItems
          numOfItemsCalificados = 0
          
          for i in range(numOfItems):
            if (self.utilityMatrix[u][i] != -1 and self.utilityMatrix[v][i] != -1):
              itemsCalificados[i] = 1
              numOfItemsCalificados += 1
             
          # Media de calificaciones de los usuarios (r(u))
          meanUserU = 0
          meanUserV = 0
          for i in range(numOfItems):
            if (itemsCalificados[i] == 1):
              meanUserU += self.utilityMatrix[u][i]  # Calificación del usuario u del item i
              meanUserV += self.utilityMatrix[v][i]
          
          meanUserU /= numOfItemsCalificados
          meanUserV /= numOfItemsCalificados
                
          sumOfDividend, divisor, sumOfx, sumOfy, x, y = 0, 0, 0, 0, 0, 0
      
          # Aplicamos fórmula para obtener la similitud entre usuarios
          for i in range(numOfItems):
            if (itemsCalificados[i] == 1): # Solo los que hayan sido calificados por ambos
              x = self.utilityMatrix[u][i] - meanUserU
              y = self.utilityMatrix[v][i] - meanUserV
              sumOfDividend += x * y
              sumOfx += x ** 2
              sumOfy += y ** 2
              
          x2 = math.sqrt(sumOfx)
          y2 = math.sqrt(sumOfy)
          divisor = x2 * y2
                
          self.sim[u][v] = round((sumOfDividend / divisor),2)
    self.orderByProximity(True)

  def cosineDistance(self):
    print("Coseno")
    
    # u y v usuarios
    numOfUsers = len(self.utilityMatrix)
    numOfItems = len(self.utilityMatrix[0])
    
    for u in range(numOfUsers):
      for v in range(numOfUsers):
        if (u == v):
          self.sim[u][v] = 1.0
        else: 
          # Suv = conjunto de items calificados por u y s
          # Creamos un array de 0's y marcamos con un 1 las calificaciones en las que u y v han calificado
          itemsCalificados = [0] * numOfItems
          
          for i in range(numOfItems):
            if (self.utilityMatrix[u][i] != -1 and self.utilityMatrix[v][i] != -1):
              itemsCalificados[i] = 1
             
          sumOfDividend, divisor, sumOfx, sumOfy, x, y = 0, 0, 0, 0, 0, 0
      
          # Aplicamos fórmula para obtener la similitud entre usuarios
          for i in range(numOfItems):
            if (itemsCalificados[i] == 1): # Solo los que hayan sido calificados por ambos
              x = self.utilityMatrix[u][i]
              y = self.utilityMatrix[v][i]
              sumOfDividend += x * y
              sumOfx += x ** 2
              sumOfy += y ** 2
              
          x2 = math.sqrt(sumOfx)
          y2 = math.sqrt(sumOfy)
          divisor = x2 * y2
                
          self.sim[u][v] = round((sumOfDividend / divisor),2)
    self.orderByProximity(True)
  
  def euclideanDistance(self):
    print("Euclidean")
    
    # u y v usuarios
    numOfUsers = len(self.utilityMatrix)
    numOfItems = len(self.utilityMatrix[0])
    
    for u in range(numOfUsers):
      for v in range(numOfUsers):
        if (u == v):
          self.sim[u][v] = 0.0 # Distancia entre dos puntos = 0
        else: 
          # Suv = conjunto de items calificados por u y s
          # Creamos un array de 0's y marcamos con un 1 las calificaciones en las que u y v han calificado
          itemsCalificados = [0] * numOfItems
          
          for i in range(numOfItems):
            if (self.utilityMatrix[u][i] != -1 and self.utilityMatrix[v][i] != -1):
              itemsCalificados[i] = 1
             
          dEuc, sum, x, y = 0, 0, 0, 0
      
          # Aplicamos fórmula para obtener la similitud entre usuarios
          for i in range(numOfItems):
            if (itemsCalificados[i] == 1): # Solo los que hayan sido calificados por ambos
              x = self.utilityMatrix[u][i]
              y = self.utilityMatrix[v][i]
              sum += (x - y) ** 2
              
          dEuc = math.sqrt(sum)
                
          self.sim[u][v] = round(dEuc,2)
    self.orderByProximity(False)
    
  def orderByProximity(self, flag):
    
    simOrderByProximity = np.zeros((len(self.utilityMatrix), len(self.utilityMatrix)))
    if (flag == True): # Ordenar de mayor a menor
      for u in range(len(self.sim)):
        simOrderByProximity[u] = sorted(self.sim[u], reverse=True)
    else: # Ordenar de menor a mayor
      for u in range(len(self.sim)):
        simOrderByProximity[u] = sorted(self.sim[u])
      
    self.simOrderByProximity = simOrderByProximity

  def getSimilarityMatrix(self):
    return self.sim
    
   
  def predictionDifferenceMean(self):
    
    for u in range(len(self.utilityMatrix)):
      for i in range(len(self.utilityMatrix[u])):
        if (self.utilityMatrix[u][i] != -1):
          self.predictionMatrix[u][i] = self.utilityMatrix[u][i]
        else:
          print("User " + str(u) + " Item " + str(i))
          # Encontrar los k vecinos más proximos a u
          simNeighbors, k = self.nearNeighbors(u)
          print(simNeighbors, k)
          dividend, divisor = 0, 0
          meanUserU = self.mean(u)
          for v in k:
            sim = self.sim[u][v]
            r = self.utilityMatrix[v][i]
            # print (sim, r)
        
            meanUserV = self.mean(v)
            print(meanUserU, meanUserV)
        
            
            dividend += sim * (r - meanUserV)
            divisor += abs(sim)
          
          self.predictionMatrix[u][i] = round(meanUserU + (dividend/divisor),2)
          
  def mean(self, u):
    numOfItems = len(self.utilityMatrix[u])
    itemsCalificadosU = [0] * numOfItems
    numOfItemsCalificadosU = 0
  
    for j in range(numOfItems):
      if (self.utilityMatrix[u][j] != -1):
        itemsCalificadosU[j] = 1
        numOfItemsCalificadosU += 1
      
    meanUserU = 0
    for j in range(numOfItems):
      if (itemsCalificadosU[j] == 1):
        meanUserU += self.utilityMatrix[u][j]
            
    meanUserU /= numOfItemsCalificadosU
    
    return meanUserU
          
  
  def predictionSimple(self):
    
    for u in range(len(self.utilityMatrix)):
      for i in range(len(self.utilityMatrix[u])):
        if (self.utilityMatrix[u][i] != -1):
          self.predictionMatrix[u][i] = self.utilityMatrix[u][i]
        else:
          print("User " + str(u) + " Item " + str(i))
          # Encontrar los k vecinos más proximos a u
          simNeighbors, k = self.nearNeighbors(u)
          dividend, divisor = 0, 0
          for v in k:
            sim = self.sim[u][v]
            r = self.utilityMatrix[v][i]
            
            dividend += sim * r
            
            divisor += abs(sim)
      
          self.predictionMatrix[u][i] = round(dividend/divisor, 2)
          
          
  def nearNeighbors(self, u):
    p = []
    for i in range(1, self.numOfNeighbors+1):
      p.append(self.simOrderByProximity[u][i])
    
    indices = np.where(np.isin(self.sim[u], p, assume_unique=True))[0]
        
    return p, indices
    
  def getSimOrder(self):
    return self.simOrderByProximity   
  
  def getUtilityMatrix(self):
    return self.matrix
  
  def getPredictionMatrix(self):
    return self.predictionMatrix
  
  # Convertir la matrix generada por loadtxt en una matrix con la que 
  # se pueda trabajas, es decir todos los datos de un mismo tipo
  def matrixConverter(self):
    matrix = np.zeros((len(self.matrix), len(self.matrix[0])), dtype=int)
        
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix[i])):
        if (self.matrix[i][j].isdigit()):
          matrix[i][j]= int(self.matrix[i][j])
        else:
          matrix[i][j] = -1 # Usamos -1 como puntuación no conocida para tener una matriz de enteros homogenea
          
    self.utilityMatrix = matrix