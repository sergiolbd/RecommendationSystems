import numpy as np
import math


class RecommendationSystem:
  
  # Constructor de la clase
  def __init__(self, file):
    self.matrix = np.loadtxt(file, dtype=str) # Matriz leida del fichero
    
    self.utilityMatrix = None # Matriz de utilidad Números enteros
    self.matrixConverter()
    
    self.sim = np.zeros((len(self.utilityMatrix), len(self.utilityMatrix)), dtype=float)
    
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
    
    
    
  def euclideanDistance(self):
    print("Euclidean")
    
    
  def getSimilarityMatrix(self):
    return self.sim
    
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