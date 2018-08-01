import copy
import random

class Direction:
	LEFT = 1
	RIGHT = 2
	UP = 3
	DOWN = 4

class printColor:
	BLACK = '\033[0m'
	GREEN = '\033[92m'
	PINK = '\033[95m'
	PURPLE = '\033[94m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	

class Board(object):
	colors = [printColor.BLACK, printColor.GREEN, printColor.PINK, printColor.PURPLE, printColor.YELLOW, printColor.RED]
	validNum = [0] + [2** i for i in range(1, 20)]

	def __init__(self, size, prob4 = 0.1) :
		self._size = size
		self._prob4 = prob4
		self._boardArray = [[0 for i in range(size)] for i in range(size)]
		self._score = 0

	def getSize(self):
		return self._size

	def getBoardArray(self):
		return copy.deepcopy(self._boardArray)

	def getMax(self):
		result = 0
		for i in range(self._size):
			for j in range(self._size):
				if self._boardArray[i][j] > result:
					result = self._boardArray[i][j]

		return result

	def getSum(self):
		result = 0
		for i in range(self._size):
			for j in range(self._size):
					result += self._boardArray[i][j]

		return result

	def clone(self):
		"""
		Return a clone of this board object

		return: (Board)
		"""
		return copy.deepcopy(self)

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False

	def __ne__(self, other):
    		return not self.__eq__(other)

	def printBoard(self):
		"""
		Print current board configuration

		return: None
		"""
		for i in range(self._size):
			for j in range(self._size):
				print self.colors[(self.validNum.index(self._boardArray[i][j]) ) % len(self.colors)] + '{:<5}'.format(self._boardArray[i][j]),
			if i == self._size / 2:
				print printColor.BLACK + '\tScore: %s' %(self.getScore()),
			print '\n'

	def getEmptyTiles(self):
		"""
		Get a list of empty tiles' coordinates

		return: (list) [(x1, y1), ..., (xn, yn)]
		"""
		result = []

		for i in range(self._size):
			for j in range(self._size):
				if self._boardArray[i][j] == 0:
					result.append((i, j))
		return result

	def getScore(self):
		"""
		Get the current score of the board configuration

		return: (int)
		"""
		return self._score

	def contains(self, num):
		for row in self._boardArray:
			if num in row:
				return True
		return False

	def addTile(self):
		"""
		Add a tile to the board with prob4 probability of putting a 4

		return: True if add a tile
		"""
		emptyTiles = self.getEmptyTiles()
		if len(emptyTiles) > 0:
			rowIndex, colIndex = random.choice(emptyTiles)
			num = 2 if random.random() > self._prob4 else 4
			self._boardArray[rowIndex][colIndex] = num
			return True
		else:
			return False

	def setTile(self, rowIndex, colIndex, value):
		self._boardArray[rowIndex][colIndex] = value


	def shiftLeft(self):
		newBoard = [filter(lambda x: x != 0, row) for row in self._boardArray]
		for row in newBoard:
			while len(row) < self._size:
				row.append(0)

		self._boardArray = newBoard

	def shiftRight(self):
		newBoard = [filter(lambda x: x != 0, row) for row in self._boardArray]
		for row in newBoard:
			while len(row) < self._size:
				row.insert(0, 0)

		self._boardArray = newBoard

	def mergeLeft(self):
		for row in self._boardArray:
			for i in range(self._size - 1):
				if row[i] == row[i + 1]:
					row[i] *= 2
					row[i + 1] = 0
					self._score += row[i]

	def mergeRight(self):
		for row in self._boardArray:
			for i in range(self._size - 1, 0, -1):
				if row[i - 1] == row[i]:
					row[i] *= 2
					row[i - 1] = 0
					self._score += row[i]

	def rotateRight(self):
		"""
		Swap the tile (x, y) in boardArray with tile (y, x) so that we can 
		apply he existing move for left an right to the move of up and down

		return: None
		"""
		newBoard = [[row[i] for row in self._boardArray] for i in range(self._size)]
		self._boardArray = newBoard

	def move(self, direction, addtile = True):
		# Todo enum is better
		oldBoard = self.clone()
		if direction == Direction.LEFT:
			self.shiftLeft()
			self.mergeLeft()
			self.shiftLeft()
		elif direction == Direction.RIGHT:
			self.shiftRight()
			self.mergeRight()
			self.shiftRight()
		elif direction == Direction.UP:
			self.rotateRight()
			self.shiftLeft()
			self.mergeLeft()
			self.shiftLeft()
			self.rotateRight()
		elif direction == Direction.DOWN:
			self.rotateRight()
			self.shiftRight()
			self.mergeRight()
			self.shiftRight()
			self.rotateRight()

		if addtile and oldBoard != self:
			self.addTile()

		return self