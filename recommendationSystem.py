import numpy as np


class RecommendationSystem:
  
  # Constructor de la clase
  def __init__(self, file):
    self.matrix = np.loadtxt(file, dtype=str)
    
    self.utilityMatrix = None
    self.matrixConverter()
    
    print(self.utilityMatrix)
  
  
  def pearson(self):
    print("Pearson")
    
  # Convertir la matrix generada por loadtxt en una matrix con la que 
  # se pueda trabajas, es decir todos los datos de un mismo tipo
  def matrixConverter(self):
    
    matrix = np.zeros((len(self.matrix), len(self.matrix[0])), dtype=int)
    
    # print(matrix)
    
    for i in range(len(self.matrix)):
      for j in range(len(self.matrix[i])):
        if (self.matrix[i][j].isdigit()):
          matrix[i][j]= int(self.matrix[i][j])
        else:
          matrix[i][j] = -1
          
    self.utilityMatrix = matrix