from gameboard import GameBoard
from consoleRenderer import ConsoleRenderer
import gameEngine
import objects
import keyboard
import time
import config
#import pygameRenderer

is_bottom_colliding = False
is_side_colliding = False

tempCounter = 0

fallingSpeed = config.configFallingSpeed

quitRequested = False
nextObject = list()

engine = None

pause = False

def renderFrame(x, y, gameBoard, gameObject):
    global tempCounter

    tempCounter = tempCounter + 1
    ConsoleRenderer.clrBuffer()

    ConsoleRenderer.renderText(
        'BoardWidth: ' + str(gameBoard.width) + ' BoardHeight: ' + str(gameBoard.height))
    ConsoleRenderer.renderText(
        'X: ' + str(x) + ' Y: ' + str(y), 27)
    ConsoleRenderer.renderText(
        'currentGameObjectWidth: ' + str(engine.activeObjectsize[0]) + ' currentGameObjectHeight: ' + str(engine.activeObjectsize[1]), 28)

    ConsoleRenderer.renderText(
        'Bottom collision: ' + str(engine.bottomCollision) + ' Side collision: ' + engine.sideCollision, 29)

    ConsoleRenderer.renderText(str(tempCounter), 30)
    ConsoleRenderer.renderText(str(fallingSpeed), 31)

    ConsoleRenderer.renderBorder(gameBoard)
    ConsoleRenderer.renderBoard(
        engine.merge_boards(
            gameBoard.staticObjectsBoard,
            gameBoard.activeObjectsBoard
        ))

    #Render Next Object
    ConsoleRenderer.renderBoard(
        engine.nextObject,
        23, 0
    )
    #Render Score
    ConsoleRenderer.renderText("{:010d}".format(engine.scoreManager.currentScore), 5, 24)
    ConsoleRenderer.blit()

    time.sleep(1/config.fps)

def start(width=10, height=20):
    global is_bottom_colliding
    global is_side_colliding
    global tempCounter
    global engine

    gameBoard = GameBoard(width, height)
    engine = gameEngine.GameEngine(gameBoard)
    ConsoleRenderer.start()

    #enigne configuration

    engine.create_random_object()
    engine.assign_next_object_to_current()

    renderFrame(
        x=engine.activeObjectPosition[0],
        y=engine.activeObjectPosition[1],
        gameBoard=gameBoard,
        gameObject=engine.activeObject)

    keyboard.hook(move_object)

    while(not quitRequested):
        is_side_colliding = False
        is_bottom_colliding = False

        if not engine.gameOver and not pause:
            if tempCounter >= fallingSpeed:
                engine.move_object(0, 1)
                tempCounter = 0
                engine.remove_full_lines(gameBoard)

            renderFrame(
                x=engine.activeObjectPosition[0],
                y=engine.activeObjectPosition[1],
                gameBoard=gameBoard,
                gameObject=engine.activeObject)



def move_object(event):
    global fallingSpeed
    global quitRequested
    global pause

    if event.event_type == 'up':
        if event.name == 'q':
            quitRequested = True

        if event.name == 's':
            fallingSpeed = config.configFallingSpeed

    if event.event_type == 'down':
        if event.name == 's':
            fallingSpeed = 1

        if not pause and not engine.gameOver:
            if event.name == 'a':
                engine.move_object(-1, 0)

            if event.name == 'd':
                engine.move_object(1, 0)

            if event.name == 'w':
                engine.rotate_object()

        if event.name == 'p':
            pause = not pause

start()
