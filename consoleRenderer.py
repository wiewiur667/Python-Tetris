import os
import sys
import time
import gameboard
import keyboard
import curses


class ConsoleRenderer:

    buffer = ''
    borderWidth = 1
    verticalBorderStyle = '░'
    topBorderStyle = '░'
    bottomBorderStyle = '░'
    stdsrc = None
    # .newwin(ConsoleRenderer.height,ConsoleRenderer.width,0,0)
    
    @staticmethod
    def start():
        os.system("mode con lines=40")
        ConsoleRenderer.stdsrc = curses.initscr()

    @staticmethod
    def renderText(text, line=26):
        ConsoleRenderer.stdsrc.addstr(line, 0, text, 0)

    @staticmethod
    def renderBorder(gameBoard):
        ConsoleRenderer.stdsrc.addstr(
            0, 0, ConsoleRenderer.topBorderStyle * (gameBoard.width * 2 + ConsoleRenderer.borderWidth * 2))
        for rowIndex in range(gameBoard.height):
            ConsoleRenderer.stdsrc.addstr(
                rowIndex + ConsoleRenderer.borderWidth, 0, ConsoleRenderer.verticalBorderStyle, 0)
            ConsoleRenderer.stdsrc.addstr(
                rowIndex + ConsoleRenderer.borderWidth, gameBoard.width * 2 + 1, ConsoleRenderer.verticalBorderStyle, 0)
        ConsoleRenderer.stdsrc.addstr(
            gameBoard.height + 1, 0, ConsoleRenderer.bottomBorderStyle * (gameBoard.width * 2 + ConsoleRenderer.borderWidth * 2))

    @staticmethod
    def renderBoard(board, offsetX = 0, offsetY= 0):
        #if(isinstance(boards, list)):
        for row_index, row in enumerate(board):
            for cell_index, cell in enumerate(row):
                sign = ' '
                if cell == 1:
                    sign = u'██'
                ConsoleRenderer.stdsrc.addstr(
                    offsetY + row_index + ConsoleRenderer.borderWidth, 
                    offsetX + cell_index * 2 + ConsoleRenderer.borderWidth, 
                    sign, 
                    0)

    @staticmethod
    def blit():
        ConsoleRenderer.stdsrc.refresh()
        # sys.stdout.write(ConsoleRenderer.buffer)

    @staticmethod
    def clrBuffer():
        ConsoleRenderer.stdsrc.clear()
        #ConsoleRenderer.buffer = ''
