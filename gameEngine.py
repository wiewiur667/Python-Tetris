import os
import time
import gameboard
import random
import objects
import math
import config
from scoreManager import ScoreManager

class GameEngine:
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.nextObject = list()
        self.activeObject = list()
        self.activeObjectsize = [0, 0]
        self.activeObjectPosition = [0, 0]

        self.sideCollision = ''
        self.bottomCollision = False
        
        self.gameOver = False

        self.scoreManager = ScoreManager(config.multiplierTimeout)
        self.scoreManager.lineValue = config.initialLineValue
        
    def create_random_object(self):
        self.nextObject = random.choice(list(objects.gameObject.values()))

    def assign_next_object_to_current(self):
        self.activeObject = self.nextObject

    def initialize_object_top_center(self):
        self.bottomCollision = False
        self.gameBoard.activeObjectsBoard = list()
        self.assign_next_object_to_current()
        self.activeObjectPosition[0] = math.floor(self.gameBoard.width/2)
        self.activeObjectPosition[1] = -1
        self.move_object(0, 0)
        self.create_random_object()

    def move_object(self, x, y):
        self.gameOver = self.detect_game_over()

        if self.sideCollision == "left" and x > 0:
            self.activeObjectPosition[0] = self.activeObjectPosition[0] + x
        if self.sideCollision == "right" and x < 0:
            self.activeObjectPosition[0] = self.activeObjectPosition[0] + x
        if self.sideCollision == "":
            self.activeObjectPosition[0] = self.activeObjectPosition[0] + x

        if self.bottomCollision == True:
            self.gameBoard.staticObjectsBoard = self.merge_boards(
                self.gameBoard.activeObjectsBoard, self.gameBoard.staticObjectsBoard)
            self.initialize_object_top_center()

        self.activeObjectPosition[1] = self.activeObjectPosition[1] + y

        self.__move_object_x(self.activeObjectPosition[0])
        self.__move_object_y(self.activeObjectPosition[1])

        self.sideCollision = self.__detect_side_collision(self.gameBoard)
        self.bottomCollision = self.__detect_bottom_collision(self.gameBoard)

    def rotate_object(self):
        tempObject = self.activeObject[:]
        rotated = tempObject[::-1]
        rotated = list(map(list, zip(*rotated)))
        height = self.__update_object_height(rotated)
        width = self.__update_object_width(rotated)
        self.activeObject = rotated

        posDiff = self.gameBoard.width - \
            (self.activeObjectPosition[0] + self.activeObjectsize[0])
        if posDiff < 0:
            self.move_object(posDiff, 0)

    def merge_boards(self, board1, board2):
        len_diff = len(board1) - len(board2)
        temp_board_1 = board1[:]
        temp_board_2 = board2[:]

        if len_diff < 0:
            for x in range(abs(len_diff)):
                temp_board_1.append([0] * len(temp_board_2[0]))
        else:
            for x in range(abs(len_diff)):
                temp_board_2.append([0] * len(temp_board_1[0]))

        for row_index, row in enumerate(temp_board_1):
            temp_board_2[row_index] = [a or b for a,
                                       b in zip(temp_board_2[row_index], row)]
        return temp_board_2

    def remove_full_lines(self, board):
        linesToRemove = self.__detect_full_line(board)
        tempBoard = list()
        if len(linesToRemove) > 0:
            tempBoard = board.staticObjectsBoard
            for line in linesToRemove:
                del tempBoard[line]
                tempBoard.insert(0, [0]*board.width)
            self.scoreManager.updateScore(len(linesToRemove) * config.initialLineValue)
            
    def detect_game_over(self):
        if self.__get_stack_height(self.gameBoard) >= self.gameBoard.height:
            return True 

    def __move_object_x(self, offset):
        paddedObject = list()

        for objectRow in self.activeObject:
            tempRow = objectRow[:]
            if offset >= 0:
                for paddingX in range(offset):
                    tempRow.insert(0, 0)
                for lenX in range(self.gameBoard.width - len(tempRow)):
                    tempRow.append(0)
                tempRow = tempRow[0:self.gameBoard.width]
                paddedObject.append(tempRow)

        self.gameBoard.activeObjectsBoard = paddedObject

    def __move_object_y(self, offset):
        tempBoard = list()

        for tempRow in range(offset):
            tempBoard.append([0] * self.gameBoard.width)
        tempBoard.extend(self.gameBoard.activeObjectsBoard)

        self.gameBoard.activeObjectsBoard = tempBoard

    def __update_object_width(self, gameObject=None):
        if gameObject == None:
            gameObject = self.activeObject
        objectWidth = 0
        for objectRow in gameObject:
            if len(list(filter(lambda x: x == 1, objectRow))) > objectWidth:
                objectWidth = len(objectRow)
        self.activeObjectsize[0] = objectWidth
        return objectWidth

    def __update_object_height(self, gameObject=None):
        if gameObject == None:
            gameObject = self.activeObject
        objectHeight = 0
        objectHeight = len(gameObject)
        self.activeObjectsize[1] = objectHeight
        return objectHeight

    def __detect_bottom_collision(self, board):
        colliding = False
        for row_index, row in enumerate(board.activeObjectsBoard):
            for cell_index, cell in enumerate(row):
                if cell == 1 and colliding == False:
                    if row_index == len(board.staticObjectsBoard) - 1 or board.staticObjectsBoard[row_index+1][cell_index] == 1:
                        colliding = True
        return colliding

    def __detect_side_collision(self, board):
        colliding = ""
        for row_index, row in enumerate(board.activeObjectsBoard):
            for cell_index, cell in enumerate(row):
                if cell == 1:
                    if cell_index == 0 or board.staticObjectsBoard[row_index][cell_index - 1] == 1:
                        colliding = "left"
                    if cell_index == len(board.staticObjectsBoard[0]) - 1 or board.staticObjectsBoard[row_index][cell_index + 1] == 1:
                        colliding = "right"
        return colliding

    def __detect_full_line(self, board):
        lines = list()
        for index, row in enumerate(board.staticObjectsBoard):
            if row == [1]*board.width:
                lines.append(index)
        return lines

    def __get_stack_height(self, board): 
        lines = 0
        for index, row in enumerate(board.staticObjectsBoard):
            if 1 in row:
                lines = lines + 1
        return lines