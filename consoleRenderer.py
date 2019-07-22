import os
import gameboard
import curses

from colours import Colours

class ConsoleRenderer:

    buffer = ''
    borderWidth = 1
    verticalBorderStyle = '░'
    topBorderStyle = '░'
    bottomBorderStyle = '░'

    gamePieceStyle = u'██'
    stdsrc = None
    # .newwin(ConsoleRenderer.height,ConsoleRenderer.width,0,0)
    
    @staticmethod
    def start():
        os.system("mode con lines=40")
        ConsoleRenderer.stdsrc = curses.initscr()

        curses.start_color()

        #curses.init_color(curses.COLOR_BLACK, 255,201,14)
        curses.init_pair(Colours.AQUA.value, curses.COLOR_CYAN, curses.COLOR_MAGENTA)
        curses.init_pair(Colours.BLUE.value, curses.COLOR_BLUE, curses.COLOR_MAGENTA)
        curses.init_pair(Colours.ORANGE.value, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
        curses.init_pair(Colours.YELLOW.value, curses.COLOR_YELLOW, curses.COLOR_MAGENTA)
        curses.init_pair(Colours.GREEN.value, curses.COLOR_GREEN, curses.COLOR_MAGENTA)
        curses.init_pair(Colours.PURPLE.value, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(Colours.RED.value, curses.COLOR_RED, curses.COLOR_MAGENTA)

    @staticmethod
    def renderText(text, line=26, col = 0):
        ConsoleRenderer.stdsrc.addstr(line, col, text, 0)

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
        for row_index, row in enumerate(board):
            for cell_index, cell in enumerate(row):
                sign = ' '
                if cell >= 1:
                    sign = ConsoleRenderer.gamePieceStyle

                    ConsoleRenderer.stdsrc.addstr(
                    offsetY + row_index + ConsoleRenderer.borderWidth, 
                    offsetX + cell_index * 2 + ConsoleRenderer.borderWidth, 
                    sign, 
                    curses.color_pair(cell))

    @staticmethod
    def blit():
        ConsoleRenderer.stdsrc.refresh()

    @staticmethod
    def clrBuffer():
        ConsoleRenderer.stdsrc.clear()
