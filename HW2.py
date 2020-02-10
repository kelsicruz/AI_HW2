import random
import sys
import unittest
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *
import math

#global vars
bestFood = None
avgDistToFoodPoint = None
avgDistToEnemyHill = None
##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state.  This class has methods
#that
#will be implemented by students in Dr.  Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):
    def __init__(self, inputPlayerId):
        super(AIPlayer, self).__init__(inputPlayerId, "AStarAgent_gieseman21_cruzk20")
        self.resetPlayerData()
        
    def resetPlayerData(self):
        global bestFood
        global avgDistToFoodPoint
        bestFood = None
        avgDistToFoodPoint = None
        self.myTunnel = None
        self.myHill = None

    def getPlacement(self, currentState):
    
        me = currentState.whoseTurn
        
        if currentState.phase == SETUP_PHASE_1:
            #Hill, Tunnel, Grass
            self.resetPlayerData()
            self.myNest = (2,1)
            self.myTunnel = (7,1)
            return [(2,1), (7, 1), 
                    (0,3), (1,3), (2,3), (3,3), \
                    (4,3), (5,3), (6,3), \
                    (8,3), (9,3)]
        elif currentState.phase == SETUP_PHASE_2:
            moves = []
            for y in range(6, 10):
                for x in range(0,10):
                    if currentState.board[x][y].constr == None and len(moves) < 2:
                        moves.append((x,y))
            return moves
            
        else:            
            return None  #should never happen
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's
    #   move
    #   (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):
        me = currentState.whoseTurn
        workerAnts = getAntList(currentState, me, (WORKER,))
        global bestFood
        global avgDistToFoodPoint

        #starts by assigning some variables to improve evaluation of proximity to scoring 11 food
        if (me == PLAYER_ONE):
            enemy = PLAYER_TWO
        else :
            enemy = PLAYER_ONE
        
        if (self.myTunnel == None):
            self.myTunnel = getConstrList(currentState, me, (TUNNEL,))[0].coords
            
        if (self.myHill == None):
            self.myHill = getConstrList(currentState, me, (ANTHILL,))[0].coords
        
        if (bestFood == None and avgDistToFoodPoint == None):
            assignGlobalVars(currentState, self.myTunnel, self.myHill)

        selectedMove = getMove(currentState)
            
        return selectedMove
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked
    #   (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        return enemyLocations[0]

    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass

#in the current version, only evaluates proximity to winning via food collection
def heuristicStepsToGoal(currentState):
    me = currentState.whoseTurn
    if (me == PLAYER_ONE):
        enemy = PLAYER_TWO
    else :
        enemy = PLAYER_ONE
    myQueen = getAntList(currentState, me, (QUEEN,))[0]
    theirQueens = getAntList(currentState, enemy, (QUEEN,))
    if (len(theirQueens) == 0):
        return 0
    theirQueen = theirQueens[0]
    fightAnts = getAntList(currentState, me, (SOLDIER, R_SOLDIER, DRONE))

    #if a state has a dead queen, it should be avoided!!!
    if (myQueen.health == 0):
        return 99999999

    stepsToGoal = stepsToFoodGoal(currentState)
    
    #stepsToGoal += stepsToAntHillGoal(currentState)
    
    #add the enemy health to our heuristic measure in order to encourage attacks
    stepsToGoal += getTotalEnemyHealth(currentState)

    for ant in fightAnts:
        stepsToGoal += stepsToReach(currentState, ant.coords, theirQueen.coords)/3

    antCap = len(fightAnts) - 2
    for i in range(antCap):
        stepsToGoal = stepsToGoal * 2

    return stepsToGoal
        

#helper method for heuristicStepsToGoal, evaluates distance to win by food
def stepsToFoodGoal(currentState):
    #get the board
    # fastClone(currentState)
        
    #get numWorkers
    global avgDistToFoodPoint
    global bestFood

    myInv = getCurrPlayerInventory(currentState)
    foodScore = myInv.foodCount
    me = currentState.whoseTurn
    workerAnts = getAntList(currentState, me, (WORKER,))
    

    #cant collect food without workers
    if (len(workerAnts) != 1):
        return 99999999

    #in assignGlobalVars, we assigned avgDistToFoodPoint
    #we multiply that by the number of food points we need
    stepsToFoodGoal = 0
    for i in range(11-foodScore):
        stepsToFoodGoal += avgDistToFoodPoint
    
    #to that, we add the distance from scoring a food point of the ant that is closest to scoring one
    minStepsToFoodPoint = 99999999
    for worker in workerAnts:
        temp = stepsToFoodPoint(currentState, worker)
        if (temp < minStepsToFoodPoint):
            minStepsToFoodPoint = temp


    stepsToFoodGoal += minStepsToFoodPoint
    
    return stepsToFoodGoal
    
        
        
### Calculates the necessary steps to get +1 food point ###   
def stepsToFoodPoint(currentState, workerAnt):
    global bestFood
    #Check if the ant is carrying food, then we only need steps to nearest constr
    if (workerAnt.carrying):
        dist = stepsToReach(currentState, workerAnt.coords, bestFood[1])
    #Otherwise, calculate the entire cycle the ant would need to complete to get +1 food point
    else:
        dist = stepsToReach(currentState, workerAnt.coords, bestFood[0].coords) + stepsToReach(currentState, bestFood[0].coords, bestFood[1])
        
    return dist
    
    #Should never happen.
    print("Something went wrong in stepsToFoodPoint.\n")
    return None

#not yet implemented
def stepsToQueenGoal(currentState):
    pass

#not yet implemented   
def stepsToAntHillGoal(currentState):
    # Didn't use... do I need?
    global avgDistToEnemyHill

    myInv = getCurrPlayerInventory(currentState)
    enemyInv = getEnemyInv(self, currentState)
    me = currentState.whoseTurn
    foodPoints = myInv.foodCount

    #enemyAnthill (tuple) - Coordinates of enemy's anthill
    enemyAnthill = enemyInv.getAnthill().coords
    
    #allMyAnts (list) - List of all ants NOT including queen and worker.
    allMyAnts = getAntList(currentState, me, (DRONE, SOLDIER, R_SOLDIER)


    stepsToAnthillGoal = 0

    #Encourage making an ant if we don't have any
    if (len(allMyAnts) == 0 and foodPoints >=1):
        # how to handle no ants? dist would be infinite.. return a bogus number for now
        stepsToAntHillGoal = 9999999
    
    else:    
        #Add the distance between all my ants and the enemy's hill
        for ant in len(allMyAnts):
            stepsToAnthillGoal += stepsToReach(currentState, ant.coords, enemyAnthill)
    
        minStepsToEnemyHill = 99999999
        for ant in allMyAnts:
            temp = stepsToReach(currentState, ant.coords, enemyAnthill)
            if (temp < minStepsToEnemyHill):
                minStepsToEnemyHill = temp

        stepsToAntHillGoal += minStepsToEnemyHill
    
    return stepsToAntHillGoal
    
#uses MoveNode objects to represent the outcome of all possible moves
#returns the move associated with the MoveNode that has the lowest (best) utility
def getMove(currentState):
    
    frontierNodes = []
    expandedNodes = []

    rootNode = MoveNode(None, currentState)
    rootNode.depth = 0

    frontierNodes.append(rootNode)

    while ((len(frontierNodes) != 0) and (len(frontierNodes) < 60)):
        expandMe = frontierNodes.pop(0)
        expandedNodes.append(expandMe)
        newFrontiers = expandNode(expandMe)
        for node in newFrontiers:
            insert(node, frontierNodes)
        if (len(frontierNodes) == 1):
            return frontierNodes[0].move

    bestNode = frontierNodes.pop(0)

    while (bestNode.depth != 1):
        bestNode = bestNode.parent


    return bestNode.move


def insert(moveNode, moveNodeList):
    
    if (len(moveNodeList) == 0):
        moveNodeList.append(moveNode)

    else :
        for i in range(len(moveNodeList)):
            if (moveNode.utility < moveNodeList[i].utility):
                moveNodeList.insert(i, moveNode)
                return
        moveNodeList.append(moveNode)

    

#returns the MoveNode with the lowest (best) utility given a list of MoveNodes
def bestMove(moveNodes):
    bestNodeUtility = 99999999
    bestNode = moveNodes[0]
    for moveNode in moveNodes:
        if (moveNode.utility < bestNodeUtility):
            bestNode = moveNode
            bestNodeUtility = moveNode.utility
    
    return bestNode

#assign the vars bestFood and avgDistToFoodPoint, which are used in determining stepsToFoodGoal
def assignGlobalVars(currentState, myTunnel, myHill):
    
    global bestFood
    global avgDistToFoodPoint
    global avgDistToEnemyHill

    foods = getConstrList(currentState, None, (FOOD,))
    bestTunnelDist = 50
    bestHillDist = 50
    bestTunnelFood = None
    bestHillFood = None
            
    for food in foods:
        dist = stepsToReach(currentState, myTunnel, food.coords)
        if (dist < bestTunnelDist) :
            bestTunnelFood = food
            bestTunnelDist = dist
        dist = stepsToReach(currentState, myHill, food.coords)
        if (dist < bestHillDist) :
            bestHillFood = food
            bestHillDist = dist
            
    if (bestHillDist < bestTunnelDist):
        bestFood = (bestHillFood, myHill)
    else :
        bestFood = (bestTunnelFood, myTunnel)

    me = currentState.whoseTurn
    workerAnts = getAntList(currentState, me, (WORKER,))
    allAnts = getAntList(currentState, me, (WORKER, DRONE, SOLDIER, R_SOLDIER))

    totalDistToAnthill = 0
    if(len(allAnts) == 0):
        avgDistToEnemyHill = 999999999
    else:
        for ant in allAnts:
            totalDistToAnthill += stepsToReach(currentState, ant.coords, enemyAnthill)
        avgDistToEnemyHill = totalDistToAnthill/len(allAnts)

    for worker in workerAnts:
        foodToTunnelDist = stepsToReach(currentState, bestFood[0].coords, bestFood[1])
        marginalFoodPointCost = foodToTunnelDist * 2
    avgDistToFoodPoint = marginalFoodPointCost
    
#sums health of all enemy ants. Used to encourage attack moves
def getTotalEnemyHealth(currentState):
    me = currentState.whoseTurn
    if (me == PLAYER_ONE):
        enemy = PLAYER_TWO
    else :
        enemy = PLAYER_ONE
    
    enemyAnts = getAntList(currentState, enemy, (WORKER,QUEEN,DRONE,SOLDIER,R_SOLDIER))
    totalEnemyHealth = 0
    for ant in enemyAnts:
        totalEnemyHealth += ant.health
        
    return totalEnemyHealth

def expandNode(expandMe):
    moves = listAllLegalMoves(expandMe.state)

    moveNodes = []

    for move in moves:
        nextState = getNextState(expandMe.state, move)
        stateUtility = heuristicStepsToGoal(nextState)
        node = MoveNode(move, nextState)
        node.depth = expandMe.depth + 1
        node.parent = expandMe
        node.setUtility(stateUtility)
        moveNodes.append(node)

    return moveNodes;

class MoveNode():
    
    def __init__(self, move, state):
        self.move = move
        self.state = state
        self.depth = 1
        self.utility = None
        self.parent = None
        
    def setUtility(self, newUtility):
        self.utility = newUtility + self.depth

    def __str__(self):
        return "Move: " + str(self.move) + ", Utility: " + str(self.utility)
    
##
#TEST CODE FOLLOWS
##
print("Test code is being run")

#get all necessary values from gameState
testState = GameState.getBasicState()
me = testState.whoseTurn
myTunnel = getConstrList(testState, me, (TUNNEL,))[0].coords
myHill = getConstrList(testState, me, (ANTHILL,))[0].coords
        
#getMove() test
move = getMove(testState)
if (move == None):
    print("Error in getMove(). Null move returned.\n")
else:
    print("getMove() returned: " + str(move))
#end getMove() test     
        
        
#bestMove() test
possibleMoves = listAllLegalMoves(testState)

moveNodes = []
for move in possibleMoves:
    nextState = getNextState(testState, move)
    stateUtility = heuristicStepsToGoal(nextState)
    node = MoveNode(move, nextState)
    node.setUtility(stateUtility)
    moveNodes.append(node)

bestNode = bestMove(moveNodes)

if (bestNode == None):
    print("Error in bestMove(). Null node returned.\n")
elif (bestNode.utility == None):
    print("Error in bestMove(). Utility was not set.\n")
else:
    print("bestMove() returned this MoveNode: " + str(bestNode))
#end bestMove() test
        
print("Test code has been run")

### Kelsi's Unit Tests ###
# class TestHeuristicMethods(unittest.TestCase):
#     testState = GameState.getBasicState()
#     testAnt = ant(self, (0,0), 1, 2) #makes a basic worker ant located at 0,0

#     def test_stepsToAntHillGoal(testState):
#         global avgDistToFoodPoint
#         global bestFood

#         myInv = getCurrPlayerInventory(testState)
#         workerAnts = getAntList(testState, me, (WORKER,))
#         enemyInv = getEnemyInv(self, testState)
#         enemyAnthill = enemyInv.getAnthill().coords
#         allMyAnts = getAntList(currentState, me, (WORKER, DRONE, SOLDIER, R_SOLDIER)

#         # CASE 1: Make sure the fxn never returns null.
#         assert stepsToAntHillGoal(testState) is not None

#         # CASE 2: If we have no ants and food points are >= 1, return bogus num
#         allMyAnts.clear()
#         myInv.foodCount = 1
#         assertEqual(stepsToAntHillGoal(testState), 9999999)

#         # CASE 3: Fxn returns expected val w normal inputs
#         allMyAnts.appent(testAnt)
#         testAntDist = 2*(stepsToReach(testState, testAnt.coords, enemyAnthill))

#         assertEqual(stepsToAntHillGoal(testState), testAntDist)

#     def test_stepsToFoodPoint(testState, testAnt):
#         global bestFood
#         # CASE 1: If the ant is carrying food, get distance from ant to tunnel.
#         testAnt.carrying = True
#         expectedDistance1 = stepsToReach(testState, workerAnt.coords, bestFood[1])
#         assertEqual(stepsToFoodPoint(testState, testAnt), expectedDistance1)

#         # CASE 2: If the ant is not carrying food, get distance from ant -> food -> tunnel
#         testAnt.carrying = False
#         expectedDistance2 = stepsToReach(testState, workerAnt.coords, bestFood[0].coords) + stepsToReach(testState, bestFood[0].coords, bestFood[1])
#         assertEqual(stepsToFoodPoint(testState, testAnt), expectedDistance2)


#     def test_stepsToFoodGoal(testState, testAnt):
#         global avgDistToFoodPoint
#         global bestFood

#         myInv = getCurrPlayerInventory(testState)
#         workerAnts = getAntList(testState, me, (WORKER,))

#         # CASE 1: Make sure the fxn never returns null.
#         assert stepsToFoodGoal(testState) is not None

#         # CASE 2: Fxn returns bogus num if we have no ants
#         workerAnts.clear()
#         assertEqual(stepsToFoodGoal(testState), 99999999)

#         # CASE 3: Fxn returns proper num in normal case
#         workerAnts.append(testAnt)
#         myInv.foodCount = 10
#         avgDistToFoodPoint = 2
#         testAnt.carrying = True
#         expectedSteps = 2 + stepsToFoodPoint(testState, testAnt)

#         assertEqual(stepsToFoodGoal(testState), expectedSteps)





        
            
        
            
