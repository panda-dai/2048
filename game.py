import os

from board import Direction
from board import Board
from board import printColor
import ai


class Game(object):

	def __init__(self, size, prob4 = 0.1, goal = 2 ** 14, numOfStartTile = 2, depth = 4) :
		self._size = size
		self._prob4 = prob4
		self._goal = goal
		self._board = Board(size, prob4)
		self._ai = ai.AI(goal, depth)
		self._numOfStartTile = numOfStartTile
		for i in range(self._numOfStartTile):
			self._board.addTile()

	@staticmethod
	def isOver(theBoard, goal):
		"""
		Judge if the board configuration is game isOver

		return: (bool) True if cannot move and board full
		"""
		if  Game.isWin(theBoard, goal) or not Game.canMove(theBoard):
			return True
		return False

	@staticmethod
	def isWin(theBoard, goal):
		"""
		Judge if the board configuration is a win

		return: (bool) True if goal is reached
		"""
		return theBoard.contains(goal)

	def display(self):
		self._board.printBoard()
		print printColor.BLACK + 'w --- up\ts --- down\ta --- left\td --- right\tq --- exit\nh --- AI hint next step\tp --- AI autoplay'

	@staticmethod
	def canMove(theBoard):
		"""
		Judge if the board configuration can make one more move or not

		return: (bool) True if can make one more move
		"""
		newBoard = theBoard.clone()

		if len(theBoard.getEmptyTiles()) != 0:
			return True

		if newBoard.move(Direction.LEFT, False) == theBoard and \
		  newBoard.move(Direction.RIGHT, False) == theBoard and \
		  newBoard.move(Direction.UP, False) == theBoard and \
		  newBoard.move(Direction.DOWN, False) == theBoard:
			return False

		return True

	def reset(self):
		self._board = Board(self._size, self._prob4)
		for i in range(self._numOfStartTile):
			self._board.addTile()

	def main(self, autoplay = False):
		"""
		The main loop for the game
		"""
		#autoplay = False
		moveDict = {'w' : Direction.UP, 's' : Direction.DOWN, 'a' : Direction.LEFT, 'd' : Direction.RIGHT, 'q' : 'quit'}
		hintDict = {1 : 'left', 2 : 'right', 3 : 'up', 4 : 'down'}
		os.system('cls' if os.name == 'nt' else 'clear')
		if autoplay:
			print 'AI is autoplaying'
		else:
			print '2048 Interactive mode'
		self.display()

		while not Game.isOver(self._board, self._goal):
			if not autoplay:
				move  = raw_input(printColor.BLACK + 'Choose your move:').lower()
				if move in moveDict:
					if move == 'q':
						break
					else:
						self._board.move(moveDict[move])
						os.system('cls' if os.name == 'nt' else 'clear')
						print '2048 Interactive mode'
						self.display()
				elif move == 'p':
					autoplay = True
				elif move == 'h':
					move = self._ai.findBestMove(self._board)
					print "The best move is %s." %(hintDict[move])
			else:
				move = self._ai.findBestMove(self._board)
				self._board.move(move)
				os.system('cls' if os.name == 'nt' else 'clear')
				print 'AI is autoplaying\nBest move: %s' %(hintDict[move])
				self.display()

		if Game.isWin(self._board, self._goal):
			print printColor.BLACK + 'You win!'
		elif not Game.canMove(self._board):
			print printColor.BLACK + 'Game Over!'

		print printColor.BLACK + 'Final Score: %s' %(self._board.getScore())


if __name__ == '__main__':
	
	import time, sys
	argument = sys.argv
	if len(argument) > 3:
		print 'Error: game.py 0 or 1 or 2 argument!'
		sys.exit(2)
	elif len(argument) == 1:
		g = Game(4, depth = 6)
		g.main()
	else:
		if argument[1] == 'test':
			if len(argument) == 3:
				try:
					numOfTest = int(argument[2])
				except ValueError:
					raise ValueError, 'The numOfTestRun is not a valid number!'
			else:
				numOfTest = 1
			startTime = time.time()
			i = 0
			g = Game(4, depth = 6)
			score = []
			maxtile = []
			while i < numOfTest: 
				print '%s  test' %(i)
				print "ScoreArray: %s"  %(score)
				print "Maxtile: %s"  % (maxtile)
				g.main(autoplay=True)
				score.append(g._board.getScore())
				maxtile.append(g._board.getMax())
				g.reset()
				i += 1

			endTime = time.time()
			print "TIme used: %s seconds" % (endTime - startTime)
			print "ScoreArray: %s"  %(score)
			print "Maxtile: %s"  % (maxtile)
			print "Average Score: %s" % (sum(score) / float(len(score)))
			print "Win rate: %s %%" % (len([i for i in maxtile if i >=2048])/float(len(maxtile)) * 100)
		elif argument[1] == 'interactive':
			if len(argument) != 2:
				print 'Error: Interactive mode take exact 1 argument!'
				sys.exit(2)
			else:
				g = Game(4, depth = 6)
				g.main()
		else:
			print 'Error: Command not defined!!'
			sys.exit(2)