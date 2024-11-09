# perceptron_pacman.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation for apprenticeship learning
import util
from perceptron import PerceptronClassifier
from pacman import GameState

PRINT = True


class PerceptronClassifierPacman(PerceptronClassifier):
    def __init__(self, legalLabels, maxIterations):
        PerceptronClassifier.__init__(self, legalLabels, maxIterations)
        self.weights = util.Counter()

    def classify(self, data):
        """
        Data contains a list of (datum, legal moves)
        
        Datum is a Counter representing the features of each GameState.
        legalMoves is a list of legal moves for that GameState.
        """
        guesses = []
        for datum, legalMoves in data:
            vectors = util.Counter()
            for move in legalMoves:
                vectors[move] = self.weights * datum[move]  # changed from datum to datum[l]
            guesses.append(vectors.argMax())
        return guesses

        # El vector de pesos tiene un valor por cada una de las caracteristicas y datum contiene por cada movimiento un valor para cada caracteristica
        # Obtiene la clase o las clases con mayor producto escalar

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        self.features = trainingData[0][0]['Stop'].keys()  # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.

        for iteration in range(self.max_iterations):
            print("Starting iteration ", iteration, "...")
            for i in range(len(trainingData)):

                "*** YOUR CODE HERE ***"

                # VERSION 1
                """for i in range(len(trainingData)):  # Recorre cada instancia de entrenamiento
                    for j in range(len(trainingData[i][1])):  # Recorre los movimientos legales para cada estado
                        realLabel = trainingLabels[i]
                        predictedLabel = self.classify([trainingData[i]])[0] # Clasifica el estado actual usando el modelo para obtener la etiqueta predicha
                        
                        # Si la predicción no coincide con la etiqueta real, ajustamos los pesos
                        if realLabel != predictedLabel:
                            self.weights += trainingData[i][0][trainingData[i][1][j]]
                            self.weights -= trainingData[i][0][predictedLabel]"""

                stateFeatures = trainingData[i][0]
                legalMoves = trainingData[i][1]

                # Etiqueta correcta y predicción
                realLabel = trainingLabels[i]
                predictedLabel = self.classify([trainingData[i]])[0] #Devuelve las clases con mayor producto escalar (se coge la primera)

                # Ajuste de pesos si la predicción es incorrecta
                if realLabel != predictedLabel:
                    featureValue = stateFeatures[realLabel]
                    self.weights += featureValue

                    predictedFeatureValue = stateFeatures[predictedLabel]
                    self.weights -= predictedFeatureValue
