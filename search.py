# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from abc import ABC, abstractmethod

import util


class SearchProblem(ABC):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    @abstractmethod
    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    @abstractmethod
    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    @abstractmethod
    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    @abstractmethod
    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    
    "*** YOUR CODE HERE ***"
    estadoIni = problem.getStartState()
    sucesores = util.Stack()
    setPosicionesVisitadas = set()
    direcciones = []
    posAct = estadoIni

    """Esto se podría eliminar"""
    """for sucesor in problem.getSuccessors(posAct):
        direccion = sucesor[1]
        hastaLlegar =  direcciones + [direccion]
        sucesores.push((sucesor[0], hastaLlegar))"""
    
    # y ponerlo así
    sucesores.push((posAct, []))

    while not sucesores.isEmpty(): 
        posAct, direcciones = sucesores.pop() # siguiente estado, accion (norte, sur, este, oeste)

        if problem.isGoalState(posAct):
            return direcciones

        setPosicionesVisitadas.add(posAct) # Añadimos al conjunto las casillas visitadas

        for sucesor in problem.getSuccessors(posAct):
            if sucesor[0] not in setPosicionesVisitadas:
                direccion = sucesor[1]
                hastaLlegar =  direcciones + [direccion]
                sucesores.push((sucesor[0], hastaLlegar))

    return None

"""
    # Estado inicial de pacman
    estadoIni = problem.getStartState()
    print("Start:", estadoIni)
    print("Is the start a goal?", problem.isGoalState(estadoIni))
    # Pila sucesores
    sucesores = util.Stack()
    # set de posiciones visitadas
    setPosicionesVisitadas = set()
    direcciones = []

    sucesores.push((estadoIni, []))

    # control:

    while not sucesores.isEmpty():
        # sacamos el nodo actual de la pila
        
        nodoAct, direcciones = sucesores.pop()
        #print(f"\nPosición actual: {nodoAct}, Camino recorrido: {direcciones}")

        # si la posicion es goal, devuelve direcciones
        if problem.isGoalState(nodoAct):
         #   print(f"Meta encontrada en {nodoAct}, direcciones: {direcciones}")
            return direcciones
        
        if nodoAct not in setPosicionesVisitadas:
            setPosicionesVisitadas.add(nodoAct)
          #  print(f"Visitados: {setPosicionesVisitadas}")

            for sucesor in problem.getSuccessors(nodoAct):
                posSucesor, direccion, _ = sucesor

                if posSucesor not in setPosicionesVisitadas:
                    sucesores.push((posSucesor, direcciones + [direccion]))
           #         print(f"Agregando sucesor {posSucesor} a la pila con dirección {direccion}")

    if sucesores.isEmpty() and not problem.isGoalState(nodoAct):
        direcciones = None
    
    return direcciones"""



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    estadoIni = problem.getStartState()
    sucesores = util.Queue()
    setPosicionesVisitadas = set()
    direcciones = []
    posAct = estadoIni

    """Esto se podría eliminar"""
    """for sucesor in problem.getSuccessors(posAct):
        direccion = sucesor[1]
        hastaLlegar =  direcciones + [direccion]
        sucesores.push((sucesor[0], hastaLlegar))"""
    
    # y ponerlo así
    sucesores.push((posAct, []))

    while not sucesores.isEmpty(): 
        posAct, direcciones = sucesores.pop() # siguiente estado, accion (norte, sur, este, oeste)

        if problem.isGoalState(posAct):
            return direcciones

        setPosicionesVisitadas.add(posAct) # Añadimos al conjunto las casillas visitadas

        for sucesor in problem.getSuccessors(posAct):
            if sucesor[0] not in setPosicionesVisitadas:
                setPosicionesVisitadas.add(sucesor[0]) # Si no introducimos esta sentencia al recorre por nivel puede que algunos elementos se añadan dos veces a la cola 
                # Esto sucede porque la cola es una estructura FIFO y al tener varios caminos puede que haya elementos que tienen los mismos sucesores 
                direccion = sucesor[1]
                hastaLlegar =  direcciones + [direccion]
                sucesores.push((sucesor[0], hastaLlegar))

    return None


def uniformCostSearch(problem): 
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    estadoIni = problem.getStartState()
    sucesores = util.PriorityQueue()
    setPosicionesVisitadas = set()
    direcciones = []
    posAct = estadoIni

    # y ponerlo así
    sucesores.push((posAct, []), 0)

    while not sucesores.isEmpty(): 
        posAct, direcciones = sucesores.pop() # siguiente estado, accion (norte, sur, este, oeste)

        if problem.isGoalState(posAct):
            return direcciones

        setPosicionesVisitadas.add(posAct) # Añadimos al conjunto las casillas visitadas

        for sucesor in problem.getSuccessors(posAct):
            if sucesor[0] not in setPosicionesVisitadas:
                direccion = sucesor[1]
                hastaLlegar =  direcciones + [direccion]
                coste = problem.getCostOfActions(hastaLlegar)
                sucesores.push((sucesor[0], hastaLlegar), coste) # El error está en que cada vez
    return None


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
