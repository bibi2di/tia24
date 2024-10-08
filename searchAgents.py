# searchAgents.py
# ---------------
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

# PositionSearchProblem --> linea 140

"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""

import time

import search
import util
from game import Actions
from game import Agent
from game import Directions


class GoWestAgent(Agent):
    """An agent that goes West until it can't."""

    def getAction(self, state):
        """The agent receives a GameState (defined in pacman.py)."""
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP


#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems
        super().__init__()
        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print(f'[SearchAgent] using function {fn} and heuristic {heuristic}')
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction is None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state)  # Makes a new search problem
        self.actions = self.searchFunction(problem)  # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print(f'Path found with total cost of {totalCost} in {time.time() - starttime:.1f} seconds')
        if '_expanded' in dir(problem): print(f'Search nodes expanded: {problem._expanded}')

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP


class PositionSearchProblem(search.SearchProblem): 
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn=lambda x: 1, goal=(1, 1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start is not None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display):  # @UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist)  # @UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors # Devuelve un array --> siguienteEstado, accion (norte,sur,este,oeste), coste

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions is None: return 999999
        x, y = self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x, y))
        return cost


class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """

    def __init__(self):
        super().__init__()
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)


class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """

    def __init__(self):
        super().__init__()
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)


def manhattanHeuristic(position, problem, info={}):
    """The Manhattan distance heuristic for a PositionSearchProblem"""
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def euclideanHeuristic(position, problem, info={}):
    """The Euclidean distance heuristic for a PositionSearchProblem"""
    xy1 = position
    xy2 = problem.goal
    return ((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2) ** 0.5


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):

    # SUBIR VERSIÓN 1
    # Es necesario guardar en el estado las esquinas por las que pasa el pacman, sino no se sabe porque esquinas pasa
    # Se han cambiado todos los métodos

    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height - 2, self.walls.width - 2
        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0  # DO NOT CHANGE; Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"

        esquinasVis = [False, False, False, False]

        if self.startingPosition == self.corners[0]:
            esquinasVis[0] = True
        elif self.startingPosition == self.corners[1]:
            esquinasVis[1] = True
        elif self.startingPosition == self.corners[2]:
            esquinasVis[2] = True
        elif self.startingPosition == self.corners[3]:
            esquinasVis[3] = True
        
        self.startState = (self.startingPosition, tuple(esquinasVis))

        #VERSIÓN 1
        """Mismo código sin esta línea
        self.startState = (self.startingPosition, tuple(self.esquinasVis))
        y con el self de esquinasVis"""


    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        return self.startState

    # VERSIÓN 1 
    """def getStartState(self):
            No está bien porque para conocer el estado se necesita la posición inicial del pacman y el número de esquinas visitadas
            Sino el pacman no conoce que esquinas se han visitado y no puede llegar al objetivo
            return self.startingPosition
    """


    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        
        for esquinaVis in state[1]:
            if not esquinaVis:
                return False
        
        return True

        ### Se puede poner return all(state[1])

        # VERSIÓN 1
        """Lo mismo pero for esquinaVis in self.esquinasVis"""

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """

        successors = []
        posAct = state[0]
        esquinasVis = list(state[1])

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            # state contiene --> Una tupla con la posición del pacman (x, y) y la lista de las esquinas visitadas
            x, y = posAct
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                nuevasEsquinasVis = list(esquinasVis)
                if nextState ==self.corners[0]:
                    nuevasEsquinasVis[0] = True
                elif nextState ==self.corners[1]:
                    nuevasEsquinasVis[1] = True
                elif nextState ==self.corners[2]:
                    nuevasEsquinasVis[2] = True
                elif nextState ==self.corners[3]:
                    nuevasEsquinasVis[3] = True

                successors.append(((nextState, tuple(nuevasEsquinasVis)), action, 1))

        self._expanded += 1  # DO NOT CHANGE
        return successors # Devuelve un array --> siguienteEstado, esquinasVisitadas accion (norte,sur,este,oeste), coste

        """Lo mismo pero con self.esquinasVis en vez de state[1]"""

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions is None: return 999999
        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)


def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """

    corners = problem.corners  # These are the corner coordinates
    walls = problem.walls  # These are the walls of the maze, as a Grid

    posAgente = state[0]

    # List of unvisited corners and boolean of visited
    esquinasNoVis = []
    esquinasVis = list(state[1])

    # distances
    distancias = {}
    heuristico = 0

    # rellenamos lista de esquinas no visitadas:
    for i in range(len(corners)):
        if not esquinasVis[i]:
            esquinasNoVis.append(corners[i])

    if not esquinasNoVis:
        return 0  # If all corners are visited, return 0
    # Manhattan distance function
    def manhattan(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    #distancias de la posición a todas las esquinas
    for esquina in esquinasNoVis:
        distancia = manhattan(posAgente, esquina)
        distancias[esquina] = distancia

    #esquina más cercana:
    esquina_mas_cercana = min(distancias, key=distancias.get)
    heuristico += distancias[esquina_mas_cercana]
    
    #sacamos la esquina de las no visitadas:
    act = esquina_mas_cercana
    esquinasNoVis.remove(act)
    posicion = corners.index(act)
    esquinasVis[posicion] = True

    while esquinasNoVis:
        distanciasEsqActual = {}

        for esquina in esquinasNoVis:
            distanciasEsqActual[esquina] = manhattan(act, esquina)

        siguiente_esquina = min(distanciasEsqActual, key=distanciasEsqActual.get) 
        heuristico += distanciasEsqActual[siguiente_esquina] 

        act = siguiente_esquina
        esquinasNoVis.remove(siguiente_esquina)
        posicion = corners.index(siguiente_esquina)
        esquinasVis[posicion] = True  
    
    return(heuristico)

"""V1 - heurístico Corner:
 posAgente, esquinasVis = state
    
    esquinasNoVis = []
    for esquina in corners: # Genera una lista con las esquinas no visitadas
        if esquina not in esquinasVis:
            esquinasNoVis.append(esquina)

    heuristico = 0
    posAct = posAgente

    if esquinasNoVis.isEmpty: #Si ya se han visitado todas las esquinas, se ha alcanzado el objetivo
        return 0

    for esquina in esquinasNoVis:
        distancias = {} # Tenemos un diccionario que guarda todas las distancias
        for esquina in esquinasNoVis: # Hay que recalcular las distancias, dado que, la posición del agente va cambiando
            # La posición actual en cada caso será las esquina más cercana
            distancias[esquina] = abs(posAct[0] - esquina[0]) + abs(posAct[1] - esquina[1])
        
        esquina_cercana = min(distancias, key=distancias.get)
        distancia_minima = distancias[esquina_cercana]
        
        heuristico = heuristico + distancia_minima
        
        posAct = esquina_cercana
        
        esquinasNoVis.remove(esquina_cercana) # Lo elimina porque se supone que el pacman va a alcanzar esa esquina
        
    return heuristico"""


class AStarCornersAgent(SearchAgent):
    """A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"""

    def __init__(self):
        super().__init__()
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem


class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """

    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0  # DO NOT CHANGE
        self.heuristicInfo = {}  # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        """Returns successor states, the actions they require, and a cost of 1."""
        successors = []
        self._expanded += 1  # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append((((nextx, nexty), nextFood), direction, 1))
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x, y = self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost


class AStarFoodSearchAgent(SearchAgent):
    """A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"""

    def __init__(self):
        super().__init__()
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem


def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    #listaHeur = [0]
    estado_ini = problem.startingGameState
    #guardamos la información de la comida como una lista
    comida_coord = foodGrid.asList()

    if not comida_coord:
        return 0
    
    if 'distancias' not in problem.heuristicInfo:
        problem.heuristicInfo['distancias'] = {}

    max_dist = 0

    priorQueue = util.PriorityQueue()

    #para cada punto de comida dentro de las coordenadas
    for comida in comida_coord:
        if (position, comida) not in problem.heuristicInfo['distancias']:
        #calculamos la distancia entre la posicion (estado), la comida y el estado inicial
            distancia = mazeDistance(position, comida, estado_ini)
            problem.heuristicInfo['distancias'][(position, comida)] = distancia
        else:
            distancia = problem.heuristicInfo['distancias'][(position, comida)]
        #añadimos a la lista la distancia.
        priorQueue.push(comida, -distancia)
    
    comida_mas_lejana= priorQueue.pop()
    max_dist = problem.heuristicInfo['distancias'][(position, comida_mas_lejana)]
    return max_dist
    """codigo V1 
    comida_coord = foodGrid.asList()

    if not comida_coord:
        return 0
    listaHeur = [0]

    # manhattan desde posicion actual hasta cada comida.
    for comida in comida_coord:
        distancia = abs(position[0] - comida[0]) + abs(position[1] - comida[1])
        listaHeur.append(distancia)
    
    # la mayor de estas distancias:
    max_heur = max(listaHeur)
    return max_heur"""


class ClosestDotSearchAgent(SearchAgent):
    """Search for all food using a sequence of searches"""

    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while currentState.getFood().count() > 0:
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception(f'findPathToClosestDot returned an illegal move: {action}!\n{currentState}')
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print(f'Path found with cost {len(self.actions)}.')

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        return search.breadthFirstSearch(problem) 

        # util.raiseNotDefined()


class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState):
        """Stores information from the gameState.  You don't need to change this."""
        # Store the food for later reference
        super().__init__(gameState)
        self.food = gameState.getFood() #Contiene una matriz de boolean que indica en que posiciones hay comida

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x, y = state

        "*** YOUR CODE HERE ***"
        hayComida = self.food[x][y]
        return hayComida
        #util.raiseNotDefined()


def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
