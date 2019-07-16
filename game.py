import gameboard
import consoleRenderer
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

def renderFrame(x, y, gameBoard, gameObject):
    global is_bottom_colliding
    global is_side_colliding
    global tempCounter
    global fallingSpeed

    tempCounter = tempCounter + 1
    consoleRenderer.ConsoleRenderer.clrBuffer()
    # engine.move_object_y(engine.move_object_x(gameObject, x), y))

    consoleRenderer.ConsoleRenderer.renderText(
        'BoardWidth: ' + str(gameBoard.width) + ' BoardHeight: ' + str(gameBoard.height))
    consoleRenderer.ConsoleRenderer.renderText(
        'X: ' + str(x) + ' Y: ' + str(y), 27)
    consoleRenderer.ConsoleRenderer.renderText(
        'currentGameObjectWidth: ' + str(engine.activeObjectsize[0]) + ' currentGameObjectHeight: ' + str(engine.activeObjectsize[1]), 28)

    consoleRenderer.ConsoleRenderer.renderText(
        'Bottom collision: ' + str(engine.bottomCollision) + ' Side collision: ' + engine.sideCollision, 29)
    
    consoleRenderer.ConsoleRenderer.renderText(str(tempCounter), 30)
    consoleRenderer.ConsoleRenderer.renderText(str(fallingSpeed), 31)

    consoleRenderer.ConsoleRenderer.renderBorder(gameBoard)
    consoleRenderer.ConsoleRenderer.renderBoard(
        engine.merge_boards(
            gameBoard.staticObjectsBoard,
            gameBoard.activeObjectsBoard
        ))
    consoleRenderer.ConsoleRenderer.renderBoard(
        engine.nextObject,
        23,1
    ) 
    consoleRenderer.ConsoleRenderer.blit()
    time.sleep(1/config.fps)


def start(width=10, height=20):
    global is_bottom_colliding
    global is_side_colliding
    global tempCounter
    global engine
    global fallingSpeed
    global quitRequested

    gameBoard = gameboard.GameBoard(width, height)
    engine = gameEngine.GameEngine(gameBoard)
    consoleRenderer.ConsoleRenderer.start()

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

    if event.event_type == 'up':
        if event.name =='q':
            quitRequested = True

        if event.name == 's':
            fallingSpeed = config.configFallingSpeed

    if event.event_type == 'down':
        if event.name == 's':
            fallingSpeed = 1  

        if event.name == 'a':
            engine.move_object(-1, 0)

        if event.name == 'd':
            engine.move_object(1, 0)
            
        if event.name == 'w':
            engine.rotate_object()
start()