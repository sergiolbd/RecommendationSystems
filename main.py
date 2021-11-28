import os
import argparse
from recommendationSystem import RecommendationSystem as RS

# Paso de parámetros por línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="input file utility matrix")
parser.add_argument("metrics", type=str, choices=["Pearson", "Coseno", "Euclidea"], help="input selected metric")
parser.add_argument("neighbors", type=int, default=3, help="input number of neighbors")
parser.add_argument("prediction", type=str, choices=["Simple", "Media"], help="input type of prediction")
args = parser.parse_args()

if (os.path.exists('./utilityMatrix/' + args.file) and  args.neighbors > 2):
  file = './utilityMatrix/' + args.file
  A = RS(file, args.neighbors)
  if (args.metrics == "Pearson"):
    A.pearson()
  elif (args.metrics == "Coseno"):
    A.cosineDistance()
  else:
    A.euclideanDistance()
  
  if (args.prediction == "Media"):
    A.predictionDifferenceMean()
  else:
    A.predictionSimple()
  
  
  
  print("------------Matrix Utilidad----------------")
  print(A.getUtilityMatrix())
  print("------------Matrix Similitud----------------")
  print(A.getSimilarityMatrix())
  print("------------Matrix Ordenada----------------")
  print(A.getSimOrder())
  print("------------Matrix utilidad con predicciones----------------")
  # A.predictionSimple()
  # A.predictionDifferenceMean()
  print(A.getPredictionMatrix())
else: 
  print("File not found or num of neighbors is less than three")
