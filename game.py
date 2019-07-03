import gameboard
import consoleRenderer
import gameEngine
import objects
import keyboard
import time
#import pygameRenderer

is_bottom_colliding = False
is_side_colliding = False

def check_collisions(engine, gameBoard):
    global is_bottom_colliding
    global is_side_colliding

    is_side_colliding = False
    is_bottom_colliding = False

    is_bottom_colliding = engine.detect_bottom_collision(
        gameBoard.movingObjectsBoard,
        gameBoard.staticObjectsBoard)

    # is_side_colliding = engine.detect_side_collision(
    #     gameBoard.movingObjectsBoard,
    #     gameBoard.staticObjectsBoard)


def renderFrame(x, y, engine, gameBoard, gameObject):
    global is_bottom_colliding
    global is_side_colliding

    consoleRenderer.ConsoleRenderer.clrBuffer()
    # engine.move_object_y(engine.move_object_x(gameObject, x), y))

    consoleRenderer.ConsoleRenderer.renderText(
        'BoardWidth: ' + str(gameBoard.width) + ' BoardHeight: ' + str(gameBoard.height))
    consoleRenderer.ConsoleRenderer.renderText(
        'X: ' + str(x) + ' Y: ' + str(y), 27)
    consoleRenderer.ConsoleRenderer.renderText(
        'currentGameObjectWidth: ' + str(engine.activeObjectsize[0]) + ' currentGameObjectHeight: ' + str(engine.activeObjectsize[1]), 28)

    consoleRenderer.ConsoleRenderer.renderText(
        'Bottom collision: ' + str(is_bottom_colliding) + ' Side collision: ' + str(is_side_colliding), 29)

    consoleRenderer.ConsoleRenderer.renderBorder(gameBoard)
    consoleRenderer.ConsoleRenderer.renderBoard(
        engine.merge_boards(
            gameBoard.staticObjectsBoard,
            gameBoard.movingObjectsBoard
        ))

    consoleRenderer.ConsoleRenderer.blit()
    time.sleep(0.2)


def start(width=10, height=20):
    global is_bottom_colliding
    global is_side_colliding

    gameBoard = gameboard.GameBoard(width, height)
    engine = gameEngine.GameEngine(gameBoard)
    quitRequested = False
    x = 0
    y = 0
    activeObject = engine.create_random_object()

    while(not quitRequested):
        quitRequested = keyboard.is_pressed('q')

        is_side_colliding = False
        is_bottom_colliding = False

        if keyboard.is_pressed('a'):
            x -= 1

            #Limit to left board edge
            if x < 0: 
                x = 0

            gameBoard.movingObjectsBoard = engine.move_object(activeObject, x, y)
            check_collisions(engine, gameBoard)

            if is_side_colliding:
                x += 1
                gameBoard.movingObjectsBoard = engine.move_object(activeObject, x, y)
            
            renderFrame(x=x, 
                        y=y, 
                        engine=engine,
                        gameBoard=gameBoard, 
                        gameObject=activeObject)

        if keyboard.is_pressed('d'):
            x += 1
            
            #Limit to right board edge
            if x >= len(gameBoard.staticObjectsBoard[0]) - 1: 
                x = len(gameBoard.staticObjectsBoard[0]) - 1

            gameBoard.movingObjectsBoard = engine.move_object(activeObject, x, y)
            check_collisions(engine, gameBoard)

            if is_side_colliding:
                x -= 1
                gameBoard.movingObjectsBoard = engine.move_object(activeObject, x, y)

            renderFrame(x=x, 
                        y=y, 
                        engine=engine,
                        gameBoard=gameBoard, 
                        gameObject=activeObject)

        if keyboard.is_pressed('s'):
            y += 1

            #Limit to bottom board edge
            if len(gameBoard.movingObjectsBoard) >= len(gameBoard.staticObjectsBoard) - 1:
                y = y

            gameBoard.movingObjectsBoard = engine.move_object(activeObject, x, y)
            check_collisions(engine, gameBoard)

            if is_bottom_colliding:
                y -= 1
                gameBoard.movingObjectsBoard = engine.move_object(activeObject, x, y)

            renderFrame(x=x, 
                        y=y, 
                        engine=engine,
                        gameBoard=gameBoard, 
                        gameObject=activeObject)

        if keyboard.is_pressed('w'):
            #check_collisions(engine, gameBoard)
            #if not is_side_colliding or not is_bottom_colliding: 
            
            activeObject = engine.rotate_object(activeObject)
            gameBoard.movingObjectsBoard = engine.move_object(activeObject, x, y)
            renderFrame(x=x, 
                        y=y, 
                        engine=engine,
                        gameBoard=gameBoard, 
                        gameObject=activeObject)

start()
