#!/usr/bin/env python

# Michael Mullings
# mcm14n
# CIS4930 - Python Programming
# Assignment 5 - boggle_gui.py


from __future__ import print_function
from PyQt5 import QtWidgets, QtCore, QtGui
from time import ctime
import sys, random, enchant, enchant, shelve


# Check if the word has already been used
def wordCheck(word, scoreArray):
   for i in range(0, len(scoreArray)):
       if word in scoreArray[i]:
          return 1
   return 0

# Score the word 
def scoreWord(pWord):
    if len(pWord) == 3 or len(pWord) == 4:
        return 1
    elif len(pWord) == 5:
        return 2
    elif len(pWord) == 6:
        return 3
    elif len(pWord) == 7:
        return 5
    elif len(pWord) >= 8:
        return 11

# Check for a Valid Move
def movelist(pos, mlist):
    row = pos[0]
    col = pos[1]
    if row-1 > -1 and col-1 > -1:
        mlist.append([row-1, col-1])
    if row-1 > -1:
        mlist.append([row-1, col])
    if row-1 > -1 and col+1 < 4:
        mlist.append([row-1, col+1])
    if col-1 > -1:
        mlist.append([row, col-1])
    if col+1 < 4:
        mlist.append([row, col+1])
    if row+1 < 4 and col-1 > -1:
        mlist.append([row+1, col-1])
    if row+1 < 4:
        mlist.append([row+1, col])
    if row+1 < 4 and col+1 < 4:
        mlist.append([row+1, col+1])

# Recursive Call for Grid Search
def searchGrid(bogWord, pos, iter, pGrid, blist):
    mlist = list()
    tlist = list() + blist
    if iter >= len(bogWord)-1:
        return 1
    movelist(pos, mlist)
    for i in range(0, len(mlist)):
       if bogWord[iter+1] == pGrid[mlist[i][0]][mlist[i][1]]:
            if not ([mlist[i][0], mlist[i][1]] in tlist):
                blist.append([mlist[i][0], mlist[i][1]])
                if searchGrid(bogWord, [mlist[i][0], mlist[i][1]], iter+1, pGrid, blist):
                    return 1
                blist = tlist

    return 0

# Check if the Word is in the Grid
def checkGrid(bogWord, pGrid):
    tile = 0
    bogTiles, blist, firstTile = [], [], []
    bogWord = bogWord.upper()
    if 'QU' in bogWord:
        for i in range(0, len(bogWord)):
            if bogWord[i] == 'Q' and bogWord[i+1] == 'U':
                bogTiles.append('Qu')
            elif bogWord[i] == 'U' and bogWord[i-1] == 'Q':
                continue
            else:
                bogTiles.append(bogWord[i])
    else:
        bogTiles = list(bogWord)
    for i in range(0,4):
        for j in range(0,4):
            if bogTiles[0] == pGrid[i][j]:
                firstTile.append([i, j])
    for i in range(0, len(firstTile)):
      blist = list([firstTile[i]])
      if searchGrid(bogTiles, firstTile[i], tile, pGrid, blist):
         return 1
    return 0


d = enchant.Dict("en_US")
scoreboard = []
score, row, column, icount = 0, 0, 0, 0
dicelist = list()
boggleWord = "" 

dice = [['A','E','A','N','E','G'],\
        ['A','H','S','P','C','O'],\
        ['A','S','P','F','F','K'],\
        ['O','B','J','O','A','B'],\
        ['I','O','T','M','U','C'],\
        ['R','Y','V','D','E','L'],\
        ['L','R','E','I','X','D'],\
        ['E','I','U','N','E','S'],\
        ['W','N','G','E','E','H'],\
        ['L','N','H','N','R','Z'],\
        ['T','S','T','I','Y','D'],\
        ['O','W','T','O','A','T'],\
        ['E','R','T','T','Y','L'],\
        ['T','O','E','S','S','I'],\
        ['T','E','R','W','H','V'],\
        ['N','U','I','H','M','Qu']]

boggleGridDisplay = ['O','I','S','E',\
              'L','R','O','N',\
              'T','K','N','I',\
              'Y','N','J','I']

boggleGrid = [['O','I','S','E'],\
              ['L','R','O','N'],\
              ['T','K','N','I'],\
              ['Y','N','J','I']]

def setBoard():
	global icount, row, column, dicelist, boggleGrid, boggleGridDisplay
	icount, row, column = 0,0,0
	dicelist = list() 
	while icount < 16:
    		num = random.randint(0,15)
    		if not (num in dicelist):
        		icount += 1
        		dicelist.append(num)
	for i in range(0,16):
		boggleGridDisplay[i]=dice[dicelist[i]][random.randint(0,5)]
		if row < 4 and column < 4:
			boggleGrid[row][column]=boggleGridDisplay[i]
		column += 1
		if column == 4:
			column = 0
			row += 1	

class BoggleGame(QtWidgets.QWidget):
        def __init__(self):
                QtWidgets.QWidget.__init__(self)
                self.setFixedSize(1720,1300)
                self.setup()

        def setup(self):
                setBoard()
                self.BoggleGrid = BoggleGrid(self)
                self.BoggleText = BoggleTextBox(self)
                self.BoggleInput = BoggleInputField(self)
                self.BoggleScoreButton = BoggleScoreButton(self)
                self.grid = QtWidgets.QGridLayout()
                self.setLayout(self.grid)
                self.grid.addWidget(self.BoggleGrid, 1, 1, 1, 1)
                self.grid.addWidget(self.BoggleText, 1, 3, 1, 1)
                self.grid.addWidget(self.BoggleInput, 2, 1, 2, 4)
                self.grid.addWidget(self.BoggleScoreButton, 2, 3, 1, 1)

        def newGame(self):
                global score, boggleWord, scoreboard
                score = 0
                boggleWord = ''
                scoreboard = []
                self.BoggleText.clear()
                self.BoggleInput.clear()
                setBoard()	
                self.BoggleGrid.setBoggleBoard()
	
        def saveGame(self):
                global boggleGridDisplay, boggleGrid, scoreboard, score, boggleWord
                s = shelve.open('boggle_shelf.db')
                s[ctime()] = {'displayGrid': boggleGridDisplay, 'grid': boggleGrid, 'scoreboard': scoreboard, 'score': score, 'wordlist': boggleWord}
                s.close()	
	
        def loadGame(self):
                s = shelve.open('boggle_shelf.db')
                self.LoadScreen = BoggleLoadScreen(self, s.keys())
                self.LoadScreen.exec_()

class BoggleLoadScreen(QtWidgets.QDialog):
	def __init__(self, parent, savefiles):
                QtWidgets.QDialog.__init__(self)
                QtWidgets.QListWidget.__init__(self)
                self.savelist = list(savefiles)
                self.parent = parent
                self.move(700,700)
                self.resize(700,700)
                self.setWindowTitle(' Load Game')
                self.grid = QtWidgets.QGridLayout()
                self.setLayout(self.grid)
                self.saveList = BoggleSaveList(self)
                self.grid.addWidget(self.saveList, 1, 1, 5, 5)
                self.savelist.reverse()
                for i in range(0, len(self.savelist)):
                      self.saveList.addItem(self.savelist[i])
                self.saveList.itemClicked.connect(self.saveList.selected)		
                self.saveList.itemClicked.connect(self.saveList.close)	

class BoggleSaveList(QtWidgets.QListWidget):
	def __init__(self, parent):
		QtWidgets.QListWidget.__init__(self)
		self.parent = parent

	def selected(self, item):
		global boggleGridDisplay, boggleGrid, scoreboard, score, boggleWord
		self.select = item.text()
		s = shelve.open('boggle_shelf.db')
		boggleGridDisplay = s[self.select]['displayGrid']
		boggleGrid = s[self.select]['grid']
		scoreboard = s[self.select]['scoreboard']
		score = s[self.select]['score']
		boggleWord = s[self.select]['wordlist']	
		self.parent.parent.BoggleGrid.setBoggleBoard()				
		self.parent.parent.BoggleText.setText(boggleWord)	

	def close(self):
		self.parent.close()

class BoggleDisplayButton(QtWidgets.QLabel):
	def __init__(self, letter):
		QtWidgets.QLabel.__init__(self)
		self.letter = letter
		self.setup()

	def setup(self):
		p = self.palette()
		p.setColor(self.backgroundRole(), QtGui.QColor(205,192,146))
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.setText(self.letter)
		self.setFrameStyle(QtWidgets.QFrame.Panel)
		self.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)		
		self.setFont(QtGui.QFont('Times', 14, QtGui.QFont.Bold))
		self.setFixedSize(250,270)		

class BoggleTextBox(QtWidgets.QTextEdit):
        def __init__(self, parent):
                QtWidgets.QTextEdit.__init__(self)
                self.setup()

        def setup(self):
                self.setReadOnly(True)
                self.setFixedSize(500, 1050)

class BoggleInputField(QtWidgets.QLineEdit):
	def __init__(self, parent):
		QtWidgets.QLineEdit.__init__(self)
		self.boggleText = parent.BoggleText
		self.setup()

	def setup(self):
		self.setPlaceholderText(' Enter A Word!')
		self.setFixedSize(1100, 75)
		self.returnPressed.connect(self.checkWord)

	@QtCore.pyqtSlot()
	def checkWord(self):
		self.word = self.text()
		global score, boggleWord, scoreboard, boggleGrid, d
		boggleWord = boggleWord + self.word + '\n'
		if not wordCheck(self.word.upper(), scoreboard):
			if len(self.word) > 2:
				if d.check(self.word):
					if checkGrid(self.word, boggleGrid):
						scoreboard.append([self.word, scoreWord(self.word), 0])
						score = score + scoreWord(self.word)
		self.boggleText.setText(boggleWord)
		self.clear()

class BoggleScoreButton(QtWidgets.QPushButton):
	def __init__(self, parent):
		QtWidgets.QPushButton.__init__(self, parent)
		self.setText('Score')
		p = self.palette()
		p.setColor(self.backgroundRole(), QtGui.QColor(205,192,146))
		self.setPalette(p)
		self.parent = parent
		self.clicked.connect(self.display)
		self.setup()

	def setup(self):
		self.setFixedSize(400, 75)
		self.move(400, 10)

	def display(self):
		self.scoreboard = BoggleScoreDisplay()
		response = self.scoreboard.exec_()
		if response == QtWidgets.QMessageBox.No:
			QtCore.QCoreApplication.instance().quit()
		elif response == QtWidgets.QMessageBox.Yes:
			self.parent.newGame()

class BoggleScoreDisplay(QtWidgets.QMessageBox):
	def __init__(self):
		QtWidgets.QMessageBox.__init__(self)
		self.move(700,700)
		self.setWindowTitle(' Play Boggle!')
		global score
		self.setText('      Your Score: '+str(score)+'\nWould you like to play again?')
		no = self.addButton(self.No)
		yes = self.addButton(self.Yes)
		self.setDefaultButton(yes)

class BoggleGrid(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self,parent)
		self.setup()

	def setup(self):
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.setBoggleBoard()

	def setBoggleBoard(self):
		pos = [(i,j) for i in range(5) for j in range(4)]
		for p, letter in zip(pos, boggleGridDisplay):
			label = BoggleDisplayButton(letter)
			self.grid.addWidget(label, *p)	

class BoggleGameWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setGeometry(200, 200, 1720, 1300)
		self.setup()

	def setup(self):
		p = self.palette()
		p.setColor(self.backgroundRole(), QtGui.QColor(84,1,21))
		self.setPalette(p)
		self.setAutoFillBackground(True)


		self.boggle_game = BoggleGame() 
		self.setCentralWidget(self.boggle_game)
		self.setWindowTitle("Play Boggle!")
	
		new_action = QtWidgets.QAction('New', self)
		save_action = QtWidgets.QAction('Save', self)
		load_action = QtWidgets.QAction('Load', self)
	
		menu_bar = self.menuBar()
		menu_bar.setNativeMenuBar(False)
		game_menu = menu_bar.addMenu('Game')

		game_menu.addAction(new_action)	
		game_menu.addAction(save_action)
		game_menu.addAction(load_action)

		new_action.triggered.connect(lambda: self.boggle_game.newGame())
		save_action.triggered.connect(lambda: self.boggle_game.saveGame())
		load_action.triggered.connect(lambda: self.boggle_game.loadGame())

		self.show()	
		

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	main_window = BoggleGameWindow()
	app.exec_()	

