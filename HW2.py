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


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#	playerId - The id of the player.
##
class AIPlayer(Player):
	def __init__(self, inputPlayerId):
		super(AIPlayer, self).__init__(inputPlayerId, "HW2")
		self.resetPlayerData()
		
	def resetPlayerData(self):
		self.bestFood = None
		self.myTunnel = None
		self.myHill = None
		self.avgDistToFoodPoint = None

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
					(5,2), (6,2) ];
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
	#	currentState - The state of the current game waiting for the player's move (GameState)
	#
	#Return: The Move to be made
	##
	def getMove(self, currentState):
		me = currentState.whoseTurn
		workerAnts = getAntList(currentState, me, (WORKER,))
		if (me == PLAYER_ONE):
			enemy = PLAYER_TWO
		else :
			enemy = PLAYER_ONE
		
		if (self.myTunnel == None):
			self.myTunnel = getConstrList(currentState, me, (TUNNEL,))[0].coords
			
		if (self.myHill == None):
			self.myHill = getConstrList(currentState, me, (ANTHILL,))[0].coords
		
		if (self.bestFood == None):
			foods = getConstrList(currentState, None, (FOOD,))
			bestTunnelDist = 50
			bestHillDist = 50
			bestTunnelFood = None
			bestHillFood = None
			
			for food in foods:
				dist = stepsToReach(currentState, self.myTunnel, food.coords)
				if (dist < bestTunnelDist) :
					bestTunnelFood = food
					bestTunnelDist = dist
				dist = stepsToReach(currentState, self.myHill, food.coords)
				if (dist < bestHillDist) :
					bestHillFood = food
					bestHillDist = dist
			
			if (bestHillDist < bestTunnelDist):
				self.bestFood = (bestHillFood, self.myHill)
			else :
				self.bestFood = (bestTunnelFood, self.myTunnel)
		#if (self.avgDistToFoodPoint == None and self.bestFood != None):
		#	for worker in workerAnts:
		#		print("this loop ran once!\n")
		#		foodToTunnelDist = stepsToReach(currentState, bestFood[0].coords, bestFood[1])

		

		selectedMove = getMove(currentState)
			
		return selectedMove
	
	##
	#getAttack
	#Description: Gets the attack to be made from the Player
	#
	#Parameters:
	#	currentState - A clone of the current state (GameState)
	#	attackingAnt - The ant currently making the attack (Ant)
	#	enemyLocation - The Locations of the Enemies that can be attacked (Location[])
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
	return 999999
        
		
        #returns a heuristic guess of how many moves it will take the agent to win the game starting from the given state
	#divide steps to goal into steps to each type of win
def stepsToFoodGoal(currentState):
    #get the board
    # fastClone(currentState)
		
    #get numWorkers
	workerList = getAntList(currentState, me, (WORKER,))
    numWorkers = len(workerList)

	#foodScore
    myInv = getCurrPlayerInventory(currentState)
    numFood = myInv.foodCount
    foodLoc = self.myFood.coords
    anthillLoc = myInv.getAnthill().coords
		
    toFood = 0
    toHill = 0
	
    #avgStepsToFoodPoint
    for ant in workerList:
        toFood += stepsToFoodPoint(currentState, ant, foodLoc)
        toHill += stepsToReach(currentState, foodLoc, anthillLoc)
        cycle = toFood + toHill
        # save in external variable? like ant1, ant2, etc?
        
        
	
def stepsToFoodPoint(currentState, workerAnt, foodLocation):
	steps = stepsToReach(currentState, workerAnt.coords, foodLocation)
    return steps

def stepsToQueenGoal(currentState):
	pass
	
def stepsToAntHillGoal(currentState):
	pass
	
def getMove(currentState):
	moves = listAllLegalMoves(currentState)
	
	moveNodes = []
	
	for move in moves:
		nextState = getNextState(currentState, move)
		stateUtility = heuristicStepsToGoal(nextState)
		node = MoveNode(move, nextState)
		node.setUtility(stateUtility)
		moveNodes.append(node)
		
	bestMoveFromNodeList = bestMove(moveNodes).move
			
	return bestMoveFromNodeList

def bestMove(moveNodes):
	bestNodeUtility = 999999999
	bestNode = None
	for moveNode in moveNodes:
		if (moveNode.utility < bestNodeUtility):
			bestNode = moveNode
			bestNodeUtility = moveNode.utility
	
	return bestNode
			

class MoveNode():
	
	def __init__(self, move, state):
		self.move = move
		self.state = state
		self.depth = 1
		self.utility = None
		self.parent = None
		
	def setUtility(self, newUtility):
		self.utility = newUtility + self.depth
		
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




		
			
		
			