from gameboard import GameBoard
from consoleRenderer import ConsoleRenderer
import gameEngine
import objects
import keyboard
from pynput import keyboard
import time
import config
import math
#import pygameRenderer

is_bottom_colliding = False
is_side_colliding = False

tempCounter = 0

fallingSpeed = config.configFallingSpeed
actualFallingSpeed = fallingSpeed
tFallingSpeed = actualFallingSpeed

quitRequested = False
nextObject = list()

engine = None

pause = False

direction = 0

def renderFrame(x, y, gameBoard, gameObject):
    global tempCounter
    global fallingSpeed

    ConsoleRenderer.clrBuffer()
    tempCounter = tempCounter + 1
    
    ConsoleRenderer.renderText(
        'BoardWidth: ' + str(gameBoard.width) + ' BoardHeight: ' + str(gameBoard.height))
    ConsoleRenderer.renderText(
        'X: ' + str(x) + ' Y: ' + str(y), 27)
    ConsoleRenderer.renderText(
        'currentGameObjectWidth: ' + str(engine.activeObjectsize[0]) + ' currentGameObjectHeight: ' + str(engine.activeObjectsize[1]), 28)

    ConsoleRenderer.renderText(
        'Bottom collision: ' + str(engine.bottomCollision) + ' Side collision: ' + engine.sideCollision, 29)

    ConsoleRenderer.renderText(str(tempCounter), 30)
    ConsoleRenderer.renderText(str(tFallingSpeed), 31)

    ConsoleRenderer.renderBorder(gameBoard)

    ConsoleRenderer.renderBoard(
        engine.merge_boards(
            gameBoard.staticObjectsBoard,
            gameBoard.activeObjectsBoard
        ))

    #Render Next Object
    ConsoleRenderer.renderBoard(
        engine.nextObject.shape,
        23, 0
    )
    #Render Score
    ConsoleRenderer.renderText("{:010d}".format(engine.scoreManager.currentScore), 5, 24)
    ConsoleRenderer.blit()

    time.sleep(1/config.fps)


def on_press(key):
    global actualFallingSpeed
    global quitRequested
    global pause
    global direction
    
    if not pause and not engine.gameOver:

        if key.char == 's':
            actualFallingSpeed = 2

        if key.char == 'a':
            direction = -1

        if key.char == 'd':
            direction = 1

        if key.char == 'w':
            direction = 2

    if key.char == 'p':
        pause = not pause

def on_release(key):
    global actualFallingSpeed
    global quitRequested

    if key.char == 'q':
        quitRequested = True

    if key.char == 's':
        actualFallingSpeed = fallingSpeed

def start(width=10, height=20):
    global is_bottom_colliding
    global is_side_colliding
    global tempCounter
    global engine
    global direction
    global fallingSpeed
    global actualFallingSpeed
    global tFallingSpeed

    gameBoard = GameBoard(width, height)
    engine = gameEngine.GameEngine(gameBoard)
    ConsoleRenderer.start()

    engine.create_random_object()
    engine.assign_next_object_to_current()

    listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
    listener.start()
    
    while(not quitRequested):
        is_side_colliding = False
        is_bottom_colliding = False

        if not engine.gameOver and not pause:

            if(direction == -1):
                engine.move_object(-1, 0)
                direction = 0
            if(direction == 1):
                engine.move_object(1, 0)
                direction = 0
            if(direction == 2):
                engine.rotate_object()
                direction = 0
            
            tFallingSpeed = actualFallingSpeed - math.floor(engine.scoreManager.linesRemoved/4)

            if tempCounter >= actualFallingSpeed:
                engine.move_object(0, 1)
                tempCounter = 0

            engine.remove_full_lines(gameBoard)
            
            renderFrame(
                x=engine.activeObjectPosition[0],
                y=engine.activeObjectPosition[1],
                gameBoard=gameBoard,
                gameObject=engine.activeObject)

start()
