import numpy as np
import math

# Clase que almacena los atributos y métodos necesarios de un sistema de recomendación
# siguiendo el método de filtrado colaborativo
class RecommendationSystem:
  
  # Constructor de la clase
  def __init__(self, file, neighbors):
    self.matrix = np.loadtxt(file, dtype=str) # Matriz leida del fichero
    
    self.utilityMatrix = None # Matriz de utilidad Números enteros
    self.matrixConverter()
    
    self.sim = np.zeros((len(self.utilityMatrix), len(self.utilityMatrix)), dtype=float)
    
    self.simOrderByProximity = np.zeros((len(self.utilityMatrix), len(self.utilityMatrix)))
    
    # Comprobar numero de vecinos
    if (neighbors < len(self.utilityMatrix)):
      self.numOfNeighbors = neighbors
    else: 
      self.numOfNeighbors = len(self.utilityMatrix) - 1
    
    self.predictionMatrix = np.zeros((len(self.utilityMatrix), len(self.utilityMatrix[0])))
  
    
  def pearson(self):
    print("Pearson")

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
          meanUserU = self.mean(u)
          meanUserV = self.mean(v)
                
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
                
          sim = round((sumOfDividend / divisor),2)
          # Normalizar los valores de similitud entre [0,1]
          sim = (sim-(-1)) / (1-(-1))
          self.sim[u][v] = sim
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
          # Encontrar los k vecinos más proximos a u
          k = self.nearNeighbors(u)
          dividend, divisor = 0, 0
          meanUserU = self.mean(u)
          count = 0
          for v in k:
             # Comprobar que solo se realizan los vecinos necesarios
            if (count < self.numOfNeighbors):
              sim = self.sim[u][v]
              r = self.utilityMatrix[v][i]
              if (r == -1):
                count += -1
              else:
                meanUserV = self.mean(v)

                dividend += sim * (r - meanUserV)
                divisor += abs(sim)
                count += 1
          
          x = round(meanUserU + (dividend/divisor),2)
          self.predictionMatrix[u][i] = x
          print("Valor predecido para User " + str(u) + " Item " + str(i) + " = " + str(x))
          
  
  def predictionSimple(self):
    
    for u in range(len(self.utilityMatrix)):
      for i in range(len(self.utilityMatrix[u])):
        if (self.utilityMatrix[u][i] != -1):
          self.predictionMatrix[u][i] = self.utilityMatrix[u][i]
        else:
          # Encontrar los k vecinos más proximos a u
          k = self.nearNeighbors(u)
          dividend, divisor = 0, 0
          count = 0
          for v in k:
            # Comprobar que solo se realizan los vecinos necesarios
            if (count < self.numOfNeighbors):
              sim = self.sim[u][v]
              r = self.utilityMatrix[v][i]
              # Si la calificación es desconocida entonces es -1 y no la cogemos sino pasamos al siguiente vecino
              if (r == -1):
                count += -1
              else: 
                dividend += sim * r
                divisor += abs(sim)
                count += 1

          x = round(dividend/divisor, 2)
          self.predictionMatrix[u][i] = x
          print("Valor predecido para User " + str(u) + " Item " + str(i) + " = " + str(x))
          
          
  def nearNeighbors(self, u):
    p = []
    for i in range(1, len(self.simOrderByProximity)):
      p.append(self.simOrderByProximity[u][i])
    
    indices = []
    for i in range(len(p)):
      for j in range(len(self.sim[u])):
        if (p[i] == self.sim[u][j] and j not in indices):
          indices.append(j)
          
    print("Vecinos más cercanos a " + str(u) + " = " + str(indices))
    return indices
  
  # Calcular la media de calificaciones de un determinado usuario
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