import random
import sys
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
        super(AIPlayer, self).__init__(inputPlayerId, "HW2")
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
        
            

        #if (self.avgDistToFoodPoint == None and self.bestFood != None):
        #   for worker in workerAnts:
        #       print("this loop ran once!\n")
        #       foodToTunnelDist = stepsToReach(currentState, bestFood[0].coords,
        #       bestFood[1])


        

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

def heuristicStepsToGoal(currentState):
    #test value
    me = currentState.whoseTurn
    myQueen = getAntList(currentState, me, (QUEEN,))[0]

    #if a state has a dead queen, it should be avoided!!!
    if (myQueen.health == 0):
        return 99999999

    stepsToGoal = stepsToFoodGoal(currentState)
    
    stepsToGoal += getTotalEnemyHealth(currentState)
    #print("total steps to goal: " + str(stepsToGoal) + "\n")
    return stepsToGoal
        
        
        #returns a heuristic guess of how many moves it will take the agent to
        #win the game starting from the given state
    #divide steps to goal into steps to each type of win
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

    if (len(workerAnts) == 0):
        return 99999999

    stepsToFoodGoal = 0
    for i in range(11-foodScore):
        stepsToFoodGoal += avgDistToFoodPoint
    
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
        #dist = distance(workerAnt.coords, bestFood[1])
    #Otherwise, calculate the entire cycle the ant would need to complete to get +1 food point
    else:
        dist = stepsToReach(currentState, workerAnt.coords, bestFood[0].coords) + stepsToReach(currentState, bestFood[0].coords, bestFood[1])
        #dist = distance(workerAnt.coords, bestFood[0].coords) + distance(bestFood[0].coords, bestFood[1])
        
   # print("Distance to next step in food goal: " + str(dist))
    return dist
    #Should never happen.
    print("Something went wrong in stepsToFoodPoint.\n")
    return None

def stepsToQueenGoal(currentState):
    pass
    
def stepsToAntHillGoal(currentState):
    pass
    
def getMove(currentState):
    moves = listAllLegalMoves(currentState)
    
    moveNodes = []
    
    #print("==============considering next move==============")
    #print(bestFood[0].coords)

    for move in moves:
        nextState = getNextState(currentState, move)
        
        stateUtility = heuristicStepsToGoal(nextState)
        node = MoveNode(move, nextState)
        node.setUtility(stateUtility)
        moveNodes.append(node)
        
    #print(len(moveNodes))
    bestMoveFromNodeList = bestMove(moveNodes).move
            
    return bestMoveFromNodeList

def bestMove(moveNodes):
    bestNodeUtility = 99999999
    bestNode = None
    for moveNode in moveNodes:
        if (moveNode.utility < bestNodeUtility):
            bestNode = moveNode
            bestNodeUtility = moveNode.utility
    
    return bestNode

def assignGlobalVars(currentState, myTunnel, myHill):
    
    global bestFood
    global avgDistToFoodPoint

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

    for worker in workerAnts:
        print("this loop ran once!\n")
        foodToTunnelDist = stepsToReach(currentState, bestFood[0].coords, bestFood[1])
        print("steps between hill and food: " + str(foodToTunnelDist))
        marginalFoodPointCost = foodToTunnelDist * 2
    avgDistToFoodPoint = marginalFoodPointCost
    
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

class MoveNode():
    
    def __init__(self, move, state):
        self.move = move
        self.state = state
        self.depth = 1
        self.utility = None
        self.parent = None
        
    def setUtility(self, newUtility):
        self.utility = newUtility + self.depth
"""     
##
#TEST CODE FOLLOWS
##
print("Test code is being run")

testState = GameState.getBasicState()
        
#getMove() test
move = getMove(testState)
if (move == None):
    print("Error in getMove(). Null move returned.\n")
        
        
        
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
else:
    if (bestNode.utility == None):
        print("Error in bestMove(). Utility was not set.\n")
        
print("Test code has been run")
"""



        
            
        
            