# multiAgents.py
# --------------
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


import random

import util
from game import Agent
from util import manhattanDistance


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition() #Posición del pacman
        newFood = successorGameState.getFood() #Matriz de booleanos comida
        newGhostStates = successorGameState.getGhostStates() #Posición fantasma y a donde se mueve
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # Tiempo que el fantasma está asustado


        "*** YOUR CODE HERE ***"

        """score = 0
        i = 1
        infoFantasmas = {}
        for ghostState in newGhostStates:
            posFantasma = ghostState.getPosition()
            distanciaAct = manhattanDistance(newPos, posFantasma)
            infoFantasmas['fantasma'] = i
            infoFantasmas['distancia'] = distanciaAct
            tiempoAsustado = newScaredTimes[i-1]
            infoFantasmas['asustado'] = tiempoAsustado != 0
            i = i+1

        distanciaComida = 0

        anchura = newFood.width  # Ancho (número de columnas)
        altura = newFood.height  # Alto (número de filas)

        for x in range (anchura):
            for y in range (altura):
                if newFood[x][y]:
                    posComida = tuple((x,y))
                    distanciaAct = manhattanDistance(newPos, posComida)
                    distanciaComida += distanciaAct

        
        distancia = infoFantasmas['distancia']
        
        if distancia == 0:
            score -= 1000  
        elif infoFantasmas['asustado']:
            score += (1 / (distancia + 1)) * 2  
        else:
            score -= (1 / (distancia + 1)) * 2 

        score += (1/(distanciaComida+1))
        print("Score: ", score)
        
        return score
        #return successorGameState.getScore()#Tendr�is que comentar esta linea y devolver el valor que calculeis"""

        """score = 0

        if successorGameState.isWin():
            puntuacion = 1000000
        
        else:
            infoFantasmas = []  

            for i, ghostState in enumerate(newGhostStates):
                posFantasma = ghostState.getPosition()
                distanciaAct = manhattanDistance(newPos, posFantasma)
                
                infoFantasmas.append({
                    'fantasma': i + 1,  # Identificador del fantasma
                    'distancia': distanciaAct,  # Distancia a Pac-Man
                    'asustado': newScaredTimes[i] != 0  # Si el fantasma está asustado
                })


            distanciaComida = float('inf')
            distanciaCrit = 5
            anchura = newFood.width  
            altura = newFood.height 

            for x in range(anchura):
                for y in range(altura):
                    if newFood[x][y]:  
                        posComida =tuple((x, y))
                        distanciaAct = manhattanDistance(newPos, posComida)
                        distanciaComida += distanciaAct

            numComidas = sum(sum(row) for row in newFood)

            for fantasma in infoFantasmas:
                distancia = fantasma['distancia']
                if fantasma['asustado']:
                    if distancia == 0:
                        score += 100000
                        print ("Score: ", score)
                        print ("Me he metido en el if 1")
                    else:  
                        score += (1 / (distancia + 1)) * 2  
                        print ("Score: ", score)
                        print ("Me he metido en el if 2")
                else:
                    if distancia == 0:
                        score -= 100000
                        print ("Score: ", score)
                        print ("Me he metido en el if 3")
                    else:
                        score -= (1 / (distancia + 1)) * 2  # Penalización por la distancia a un fantasma no asustado
                        print ("Score: ", score)
                        print ("Me he metido en el if 4")
                if not fantasma['asustado'] and distancia < distanciaCrit:
                    score += 1000 / (distanciaComida + 1)*numComidas  # Mayor puntuación cuanto más cerca esté la comida
                    print ("Score: ", score)
                    print ("Me he metido en el if 5")


            # Bonificación extra por menos comida restante
            score += (1 / (numComidas + 1)) * 1000  # Bonificación cuanto menos comida queda
            print ("Score final: ", score)

        return score  # Devuelve la puntuación calculada"""

        score = 0
        scoreSucesor = successorGameState.getScore()

        if successorGameState.isWin():
            puntuacion = float('inf')
        else:
            distComida = []
            distFant = []
            distComidaCerc = float('inf')
            distFantCerc = float('inf')
            fantAct = None
            distanciaCrit = 2
            listaCom = newFood.asList() 

            for ghostState in newGhostStates:
                posFantasma = ghostState.getPosition()
                distanciaFAct = manhattanDistance(newPos, posFantasma)
                distFant.append(distanciaFAct)
                if distanciaFAct < distFantCerc:
                    distFantCerc = distanciaFAct
                    fantAct = ghostState
            
            anchura = newFood.width  
            altura = newFood.height 
            for x in range (anchura):
                for y in range (altura):
                    if newFood[x][y]:
                        posAct = (x,y)
                        distanciaCAct = manhattanDistance(newPos, posAct)
                        distComida.append(distanciaCAct)
                        if distanciaCAct < distComidaCerc:
                            distComidaCerc = distanciaCAct
            
        
            if distFantCerc < distanciaCrit and ghostState.scaredTimer == 0:
                score =-float('inf')  
            
            numComidasRestantes = len(listaCom)  

            score -= numComidasRestantes * 10000  

            score += scoreSucesor + (1 / (distComidaCerc + 1))

        return score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        super().__init__()
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    pacman_pos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
