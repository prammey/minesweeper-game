#CHANGE DIFFICULTY AT THE BOTTOM!!!!!!!!!
#RIGHT CLICK TO SELECT BOX; LEFT CLICK TO FLAG
from tkinter import *
import random
from tkinter import messagebox

colormap = ['', 'blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray'] # I'm putting color map here so I don't have to keep putting this in the functions

class MineCell(Label):
  '''The class for every cell on the grid'''
  def __init__(self, master, rowNumber, columnNumber, isMine):
    Label.__init__(self, master, height = 1, width = 2, bg = 'white', relief = 'raised', font = ('Arial', 24), borderwidth = 3) # formating for the squares
    # initializing
    self.rowNumber = rowNumber
    self.columnNumber = columnNumber
    self.isMine = isMine
    # turn the squares into buttons
    self.bind('<Button-1>', self.check)
    self.bind('<Button-2>', self.flag)
    self.bind('<Button-3>', self.flag)
    
    if self.isMine: # If the square is a mine, distinguish it with *
      self.number = '*'
      
  def check(self, event):
    '''the square checks what is happening to itself'''
    if self.number == 0 and self['text'] != '!': # if square is safe with no value and not flagged
      # change square appearence
      self['text'] = ''
      self['bg'] = 'gainsboro'
      self['relief']  = 'sunken'
      for i in range(len(self.master.squares)):
        self.master.reveal_surrounding(i)
      for i in range(len(self.master.squares)-1, 0, -1):
        self.master.reveal_surrounding(i)
    elif self.number == '*' and self['text'] != '!': # if square is mine and not flagged
      # change square appearence
      self['text'] = self.number
      self['bg'] = 'red'
      self['relief']  = 'sunken'
      self.master.lose() # lose
    elif self['text'] != '!': # if the square is safe with number and not flagged
      # change square appearence
      self['text'] = self.number
      self['bg'] = 'gainsboro'
      self['fg'] = colormap[self.number] 
      self['relief']  = 'sunken'
    self.master.win() # check if player wins or not
  
  def reveal(self):
    if self.number == 0 and self['text'] != '!':
      # change square appearence
      self['text'] = ''
      self['bg'] = 'gainsboro'
      self['relief']  = 'sunken'
    elif self.number == '!' and self['text'] != '!':
      # change square appearence
      self['text'] = self.number
      self['bg'] = 'red'
      self['relief']  = 'sunken'
    elif self['text'] != '!':
      # change square appearence
      self['text'] = self.number
      self['bg'] = 'gainsboro'
      self['fg'] = colormap[self.number] 
      self['relief']  = 'sunken'

  def flag(self, event):
    '''deals with flags being placed'''
    if self['text'] == '!' and self['relief'] != 'sunken':
      # change square appearence
      self['text'] = ''
      self.master.canPlaceFlag = True # let player put flags
      self.master.update_flag() # flags left label
    elif self.master.canPlaceFlag:
      if self['relief'] != 'sunken':
        # change square appearence
        self['text'] = '!'
        self['fg'] = 'black'
        self.master.update_flag() # update flags left label
      
  def get_number(self):
    '''return square's number'''
    return self.number
  
  def set_number(self, setting):
    '''assigns the square a number'''
    self.number = setting

  def get_mine(self):
    '''return True if square is a mine'''
    return self.isMine

  def set_mine(self, setting):
    '''makes a square a mine'''
    self.isMine = setting
    self.number = '*'

class MineFrame(Frame):
  '''The class for the whole board'''
  def __init__(self, master, width, height, numBombs):
    # initializing    
    Frame.__init__(self, master)
    self.numBombs = numBombs
    self.width = width
    self.height = height
    self.mines = []
    self.squares = []
    self.canPlaceFlag = True
    self.flagLabel = Label(self, text = "Flags Left: " + str(self.numBombs), font = ('Arial', 18)) # set up label that counts flags left to use
    self.flagLabel.grid(columnspan = 4, row = height + 1) # put it at the bottom of the board
    self.grid()
    for rows in range(self.height): # make grid of cells
      for columns in range(self.width):
        cell = MineCell(self, rows, columns, False)
        cell.grid(row = rows, column = columns)
        self.squares.append(cell) # add the cell to the list of cells
    for i in range(self.numBombs): # for the number of bombs the player chose to play with, randomly set some squares as mines
      x = random.randrange(0, len(self.squares))
      while self.squares[x].get_mine():
        x = random.randrange(0, len(self.squares))
      self.squares[x].set_mine(True)
      self.mines.append(self.squares[x])
    for num in range(len(self.squares)): # assigns numbers to cells
      self.check_surrounding(num) 

  def check_surrounding(self, squareNum):
    '''check surroundings of squares'''
    
    self.counter = 0 # initialize
    
    # there are different if/else/elif statements to cover the different types of places the squares can be (corners, top side, middle, etc.)
    if self.squares[squareNum].get_mine():
      pass

    elif squareNum == 0:
      if self.squares[1].get_mine():
        self.counter += 1
      if self.squares[self.width].get_mine():
        self.counter += 1
      if self.squares[self.width + 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)
 
    elif squareNum == self.width - 1:
      if self.squares[squareNum - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width - 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)
  
    elif squareNum == (self.width * self.height) - self.width:
      if self.squares[squareNum + 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width + 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)

    elif squareNum == (self.width * self.height) - 1:
      if self.squares[squareNum - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width - 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)

    elif squareNum < self.width:
      if self.squares[squareNum - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width + 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)

    elif squareNum % self.width == 0:
      if self.squares[squareNum + 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width + 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width + 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)

    elif squareNum % self.width == self.width - 1:
      if self.squares[squareNum - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width - 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)

    elif squareNum > (self.width * self.height) - self.width:
      if self.squares[squareNum + 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width + 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)

    else:
      if self.squares[squareNum + 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum - self.width + 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width - 1].get_mine():
        self.counter += 1
      if self.squares[squareNum + self.width + 1].get_mine():
        self.counter += 1
      self.squares[squareNum].set_number(self.counter)

  def reveal_surrounding(self, squareNum):
    '''reveals surrounding when a blank square is clicked on'''

    # this is also a bunch of if/elif/else statements to cover the different places the squares can be
    if self.squares[squareNum]['relief'] == 'sunken': 
      if self.squares[squareNum].get_number() == 0:
        if squareNum == 0:
          self.squares[1].reveal()
          self.squares[self.width].reveal()
          self.squares[self.width + 1].reveal()
        elif squareNum == self.width - 1:
          self.squares[squareNum - 1].reveal()
          self.squares[squareNum + self.width].reveal()
          self.squares[squareNum + self.width - 1].reveal()
        elif squareNum == (self.width * self.height) - self.width:
          self.squares[squareNum + 1].reveal()
          self.squares[squareNum - self.width].reveal()
          self.squares[squareNum-self.width + 1].reveal()
        elif squareNum == (self.width * self.height) - 1:
          self.squares[squareNum - 1].reveal()
          self.squares[squareNum - self.width].reveal()
          self.squares[squareNum - self.width - 1].reveal()
        elif squareNum < self.width:
          self.squares[squareNum - 1].reveal()
          self.squares[squareNum + 1].reveal()
          self.squares[squareNum + self.width].reveal()
          self.squares[squareNum + self.width - 1].reveal()
          self.squares[squareNum + self.width + 1].reveal()
        elif squareNum % self.width == 0:
          self.squares[squareNum + 1].reveal()
          self.squares[squareNum + self.width].reveal()
          self.squares[squareNum - self.width].reveal()
          self.squares[squareNum - self.width + 1].reveal()
          self.squares[squareNum + self.width + 1].reveal()
        elif squareNum % self.width == self.width - 1:
          self.squares[squareNum - 1].reveal()
          self.squares[squareNum - self.width].reveal()
          self.squares[squareNum + self.width].reveal()
          self.squares[squareNum - self.width - 1].reveal()
          self.squares[squareNum + self.width - 1].reveal()
        elif squareNum > (self.width * self.height) - self.width:
          self.squares[squareNum + 1].reveal()
          self.squares[squareNum - 1].reveal()
          self.squares[squareNum - self.width].reveal()
          self.squares[squareNum - self.width - 1].reveal()
          self.squares[squareNum - self.width + 1].reveal()
        else:
          self.squares[squareNum + 1].reveal()
          self.squares[squareNum - 1].reveal()
          self.squares[squareNum - self.width].reveal()
          self.squares[squareNum - self.width - 1].reveal()
          self.squares[squareNum - self.width + 1].reveal()
          self.squares[squareNum + self.width].reveal()
          self.squares[squareNum + self.width - 1].reveal()
          self.squares[squareNum + self.width + 1].reveal()
      
  def lose(self):
    '''this happens when the player loses'''
    messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent = self) # show lose message
    
    # expose the rest of the mines
    for mine in self.mines:
      if mine['bg'] == 'red':
        for mine in self.mines:
          if mine['text'] != '*':
            mine['text'] = '*'
            mine['bg'] = 'red'
            mine['relief'] ='sunken'

  def win(self):
    '''checks if the player wins or not and performs accordingly'''
    uncoveredSquares = 0 # initialize
    
    # count winning squares
    for square in self.squares:
      if square.get_mine() == False and square['relief'] == 'sunken':
        uncoveredSquares += 1
      
      # if player won
      if uncoveredSquares == len(self.squares) - len(self.mines):
        messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent = self) # show winning message
        self.master.destroy() # stop all
        break

  def update_flag(self):
    '''counts flags and updates flag label'''
    flags = 0 # initialize

    # count flags used
    for square in self.squares:
      if square['text'] == '!':
        flags += 1
    flagsLeft = self.numBombs - flags # calculate flags left
    self.flagLabel['text'] = "Flags Left: " + str(flagsLeft) # change label
    if flagsLeft == 0: # if player can't place more flags
      self.canPlaceFlag = False # don't let them place anymore

def playMinesweeper(width, height, bombs):
  '''start game'''
  root = Tk()  
  root.title('Minesweeper')
  game = MineFrame(root, width, height, bombs) # makes game
  game.mainloop()

playMinesweeper(12, 10, 15) #(columns, rows, bombs)
