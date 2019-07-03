import os
import time
import gameboard
import random
import objects

class GameEngine:
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.activeObjectsize = [0,0]

    def create_random_object(self):
        return random.choice(list(objects.gameObject.values()))
        
    def get_object_width(self, gameObject):
        objectWidth = 0
        for objectRow in gameObject:
            if len(list(filter(lambda x: x == 1, objectRow))) > objectWidth:
                objectWidth = len(objectRow)
        self.activeObjectsize[0] = objectWidth
        return objectWidth
    
    def get_object_height(self, gameObject):
        objectHeight = 0
        objectHeight = len(gameObject)
        self.activeObjectsize[1] = objectHeight
        return objectHeight

    def move_object_x(self, gameObject, offset):
        paddedObject = list()
        tempRow = list()
        self.get_object_width(gameObject)

        if offset >= self.gameBoard.width - self.activeObjectsize[0]:
            offset = self.gameBoard.width - self.activeObjectsize[0]

        for objectRow in gameObject:
            tempRow = objectRow[:]
            if offset >= 0:
                for paddingX in range(offset):
                    tempRow.insert(0,0)
                for lenX in range(self.gameBoard.width - len(tempRow)):
                    tempRow.append(0)
                tempRow = tempRow[0:self.gameBoard.width]
                paddedObject.append(tempRow)

        return paddedObject
    
    def move_object_y(self, gameObjectRows, offset):
        tempBoard = list()
        self.get_object_height(gameObjectRows)
        
        for tempRow in range(offset):
            tempBoard.append([0] * self.gameBoard.width)
        tempBoard.extend(gameObjectRows)
        
        return tempBoard

    def move_object(self, object, x, y):
        tempBoard = self.gameBoard
        return self.move_object_y(self.move_object_x(object,x), y)
        
    def rotate_object(self,object):        
        tempObject = object[:]
        rotated = tempObject[::-1]
        rotated = list(map(list, zip(*rotated)))
        height = self.get_object_height(rotated)
        width = self.get_object_width(rotated)
        return rotated

    def detect_bottom_collision(self, objectRows, board):
        colliding = False
        for row_index, row in enumerate(objectRows): 
            for cell_index, cell in enumerate(row):
                if cell == 1 and colliding == False:
                    if row_index == len(board) or board[row_index][cell_index] == 1:
                        colliding = True
        return colliding

    def detect_side_collision(self, objectRows, board):
        colliding = False
        for row_index, row in enumerate(objectRows):
            for cell_index, cell in enumerate(row):
                if cell == 1:
                    if cell_index == len(board[0]) - 1 or board[row_index][cell_index] == 1:
                        colliding = True
                    if board[row_index][cell_index] == 1:
                        colliding = True
        return colliding

    def merge_boards(self, board1, board2):
        len_diff = len(board1) - len(board2)
        temp_board_1 = board1[:]
        temp_board_2 = board2[:]
        if len_diff < 0:
            for x in range(abs(len_diff)):
                temp_board_1.append([0] * len(temp_board_2[0]))
        else:
            for x in range(abs(len_diff)):
                temp_board_2.append([0]* len(temp_board_1[0]))
                
        for row_index, row in enumerate(temp_board_1):
            temp_board_2[row_index] = [a or b for a, b in zip(temp_board_2[row_index], row)]
        return temp_board_2