import sys
import math

import game
from board import Board
from board import Direction

Directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]

class Player:
	"""
	Enum of Players
	"""
	USER = 1
	COMPUTER = 2

class AI(object):

	def __init__(self, goal, depth = 3, searchMethod = 'alphaBeta'):
		self._goal = goal
		self.searchMethod = searchMethod
		self._depth = depth


	def findBestMove(self, theBoard):
		result = {}
		if self.searchMethod == 'alphaBeta':
			result = self.alphaBeta(theBoard, self._depth, -sys.maxint - 1, sys.maxint, Player.USER)
		else:
			result = self.minimax(theBoard, self._depth, Player.USER)

		return result['Direction']

	def minimax(self, theBoard, depth, player):
		result = {}
		bestDirection = None
		bestScore = None

		if depth == 0 or game.Game.isOver(theBoard, self._goal):
			bestScore = self.evaluationFunction(theBoard)
		else:
			if player == Player.USER:
				bestScore = -sys.maxint - 1

				for direction in Directions:
					newBoard = theBoard.clone()

					newBoard.move(direction, False)

					if newBoard.getScore() == theBoard.getScore() and newBoard == theBoard:
						continue

					curResult = self.minimax(newBoard, depth-1, Player.COMPUTER)
					curScore = curResult['Score']

					if curScore > bestScore:
						bestScore = curScore
						bestDirection = direction
			else:
				bestScore = sys.maxint

				moves = theBoard.getEmptyTiles()
				if len(moves) == 0:
					bestScore = 0

				possibleValues = [2, 4]

				for rowIndex, colIndex in moves:
					for value in possibleValues:
						newBoard = theBoard.clone()

						newBoard.setTile(rowIndex, colIndex, value)

						curResult = self.minimax(newBoard, depth-1, Player.USER)
						curScore = curResult['Score']

						if curScore < bestScore:
							bestScore = curScore

		result['Score'] = bestScore
		result['Direction'] = bestDirection

		return result

	def alphaBeta(self, theBoard, depth, alpha, beta, player):
		result = {}
		bestDirection = None
		bestScore = None

		if game.Game.isOver(theBoard, self._goal):
			if game.Game.isWin(theBoard, self._goal):
				bestScore = sys.maxint
			else:
				bestScore = min(theBoard.getScore(), 1)

		elif depth == 0:
			bestScore = self.evaluationFunction(theBoard)
		else:
			if player == Player.USER:
				for direction in Directions:
					newBoard = theBoard.clone()

					newBoard.move(direction, False)

					if newBoard.getScore() == theBoard.getScore() and newBoard == theBoard:
						continue

					curResult = self.alphaBeta(newBoard, depth-1, alpha, beta, Player.COMPUTER)
					curScore = curResult['Score']

					if curScore > alpha:
						alpha = curScore
						bestDirection = direction

					if alpha >= beta:
						break;

				bestScore = alpha
			else:
				moves = theBoard.getEmptyTiles()
				possibleValues = [2, 4]
				
				newBoard = theBoard.clone()
				nextStepScore = {2: {}, 4 : {}}
				
				for rowIndex, colIndex in moves:
					for value in possibleValues:
						newBoard.setTile(rowIndex, colIndex, value)
						nextStepScore[value][(rowIndex, colIndex)] = self.evaluationFunction(newBoard)
						newBoard.setTile(rowIndex, colIndex, 0)
						
				minScore =  min(min(nextStepScore[2].values()) if nextStepScore[2] != {} else -sys.maxint-1, \
									min(nextStepScore[4].values()) if nextStepScore[4] != {} else -sys.maxint-1)

				candidates = []

				for value, dic in  nextStepScore.iteritems():
					for cell, score in dic.iteritems():
						if score == minScore:
							candidates.append((cell[0], cell[1], value))
				#print "nextStepScore: ", nextStepScore
				#print "candidates: ", candidates
				
				"""
				candidates = []

				for rowIndex, colIndex in moves:
					for value in possibleValues:
						candidates.append((rowIndex, colIndex, value))
				"""
				
				for candidate in candidates:
					newBoard = theBoard.clone()
					newBoard.setTile(candidate[0], candidate[1], candidate[2])

					curResult = self.alphaBeta(newBoard, depth-1, alpha, beta, Player.USER)
					curScore = curResult['Score']

					if curScore < beta:
						beta = curScore

					if alpha >= beta:
						break

				bestScore = beta
				
				"""
				for rowIndex, colIndex in moves:
					outbreak = False
					for value in possibleValues:
						newBoard = theBoard.clone()
						newBoard.setTile(rowIndex, colIndex, value)
						curResult= self.alphaBeta(newBoard, depth-1, alpha, beta, Player.USER)
						curScore = curResult['Score']

						if curScore < beta:
							beta = curScore

						if alpha >= beta:
							outbreak = True
							break
					if outbreak:
						break

				bestScore = beta
				"""	
				if len(moves) == 0:
					bestScore = 0

		result['Score'] = bestScore
		result['Direction'] = bestDirection
		#print result, 'Player ', player, ' a: ', alpha, ' b: ', beta, ' depth: ', depth
		return result


	def evaluationFunction(self, theBoard, heuristic = 'clustering'):
		if heuristic == 'clustering':
			return self.clusteringHeuristic(theBoard)

	def clusteringScore(self, theBoard):
		clustering = 0
		neighbor = [-1, 0, 1]

		for rowIndex in range(theBoard._size):
			for colIndex in range(theBoard._size):
				if theBoard._boardArray[rowIndex][colIndex] == 0:
					continue

				score = 0
				numOfNeighbor = 0

				for i in neighbor:
					x = rowIndex + i

					if x < 0 or x >= theBoard._size:
						continue

					for j in neighbor:
						y = colIndex + j

						if y < 0 or y >= theBoard._size:
							continue

						if theBoard._boardArray[x][y] > 0:
							numOfNeighbor += 1
							#score += abs(math.log(theBoard._boardArray[rowIndex][colIndex])/ math.log(2) - math.log(theBoard._boardArray[x][y])/math.log(2))
							score += abs(theBoard._boardArray[rowIndex][colIndex] - theBoard._boardArray[x][y])

				clustering += score / numOfNeighbor

		return clustering

	@staticmethod
	def monoArray(array):
		sum1 = 0
		sum2 = 0

		arrayNew = filter(lambda x: x != 0, array)

		for i in range(len(arrayNew) - 1):
			j = i+1
			#cur = math.log(arrayNew[i])/math.log(2)
			#nex = math.log(arrayNew[j])/math.log(2)
			cur = arrayNew[i]
			nex = arrayNew[j]
			if cur > nex:
				sum1 += (cur - nex)
			else:
				sum2 += (nex - cur)

		return [int(sum1), int(sum2)]

	def monoScore(self, theBoard):
		upToDown = 0
		downToUp = 0
		leftToRight = 0
		rightToLeft = 0

		for row in theBoard._boardArray:
			result = AI.monoArray(row)
			leftToRight += result[0]
			rightToLeft += result[1]

		newBoard = [[row[i] for row in theBoard._boardArray] for i in range(theBoard._size)]

		for row in newBoard:
			result = AI.monoArray(row)
			upToDown += result[0]
			downToUp += result[1]

		return max(leftToRight, rightToLeft) + max(upToDown, downToUp)


	def clusteringHeuristic(self, theBoard):
		actualScore = theBoard.getScore()
		numOfEmpty = len(theBoard.getEmptyTiles())
		maxValue = theBoard.getMax() if theBoard.getMax() > 0 else 1
		sumBoard = theBoard.getSum()
		
		if actualScore == 0:
			actualScoreTemp = 1
		else:
			actualScoreTemp = actualScore
		clusteringMono = 1.1*(-2*self.clusteringScore(theBoard) -  1*self.monoScore(theBoard))
		score = int(actualScore + math.log(actualScoreTemp) * numOfEmpty +  0.5*sumBoard  + clusteringMono)
		#return max(score, min(actualScore, 1))
		#print score, actualScore, clusteringMono
		return score
		'''
		if score == 0 and actualScore == 0:
			return score
		else:
			return max(score, 1)
		'''
		
