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

	#__init__
	#Description: Creates a new Player
	#
	#Parameters:
	#	inputPlayerId - The id to give the new player (int)
	#	cpy			  - whether the player is a copy (when playing itself)
	##
	def __init__(self, inputPlayerId):
		super(AIPlayer,self).__init__(inputPlayerId, "HW2")
	
	##
	#getPlacement
	#
	#Description: called during setup phase for each Construction that
	#	must be placed by the player.  These items are: 1 Anthill on
	#	the player's side; 1 tunnel on player's side; 9 grass on the
	#	player's side; and 2 food on the enemy's side.
	#
	#Parameters:
	#	construction - the Construction to be placed.
	#	currentState - the state of the game at this point in time.
	#
	#Return: The coordinates of where the construction is to be placed
	##
	def getPlacement(self, currentState):
		numToPlace = 0
		#implemented by students to return their next move
		if currentState.phase == SETUP_PHASE_1:	   #stuff on my side
			numToPlace = 11
			moves = []
			for i in range(0, numToPlace):
				move = None
				while move == None:
					#Choose any x location
					x = random.randint(0, 9)
					#Choose any y location on your side of the board
					y = random.randint(0, 3)
					#Set the move if this space is empty
					if currentState.board[x][y].constr == None and (x, y) not in moves:
						move = (x, y)
						#Just need to make the space non-empty. So I threw whatever I felt like in there.
						currentState.board[x][y].constr == True
				moves.append(move)
			return moves
		elif currentState.phase == SETUP_PHASE_2:	#stuff on foe's side
			numToPlace = 2
			moves = []
			for i in range(0, numToPlace):
				move = None
				while move == None:
					#Choose any x location
					x = random.randint(0, 9)
					#Choose any y location on enemy side of the board
					y = random.randint(6, 9)
					#Set the move if this space is empty
					if currentState.board[x][y].constr == None and (x, y) not in moves:
						move = (x, y)
						#Just need to make the space non-empty. So I threw whatever I felt like in there.
						currentState.board[x][y].constr == True
				moves.append(move)
			return moves
		else:
			return [(0, 0)]
	
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
		moves = listAllLegalMoves(currentState)
		selectedMove = moves[random.randint(0,len(moves) - 1)];

		#don't do a build move if there are already 3+ ants
		numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
		while (selectedMove.moveType == BUILD and numAnts >= 3):
			selectedMove = moves[random.randint(0,len(moves) - 1)];
			
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
		#Attack a random enemy.
		return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

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
	return 3
	
	
	#returns a heuristic guess of how many moves it will take the agent to win the game starting from the given state
#divide steps to goal into steps to each type of win
def stepsToFoodGoal(currentState):
	pass
	#numWorkers
	
	#foodScore
	
	#avgStepsToFoodPoint

#added comment

def stepsToFoodPoint(currentState, workerAnt):
	pass

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




		
			
		
			