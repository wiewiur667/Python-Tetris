from tetromino import Tetromino
from colours import Colours
tetrominos = {
    "rect": Tetromino(
        colour=Colours.YELLOW,
        shape=[
            [1, 1],
            [1, 1]
        ]
    ),
    "line": Tetromino(
        colour=Colours.AQUA,
        shape=[
            [1],
            [1],
            [1],
            [1]
        ]
    ),
    "el": Tetromino(
        colour=Colours.BLUE,
        shape=[
            [1, 0],
            [1, 0],
            [1, 1]
        ]
    ),
    "inv_el": Tetromino(
        colour=Colours.ORANGE,
        shape=[
            [0, 1],
            [0, 1],
            [1, 1]
        ]
    ),
    "zet": Tetromino(
        colour=Colours.YELLOW,
        shape=[
            [0, 1],
            [1, 1],
            [1, 0]
        ]
    ),
    "inv_zet": Tetromino(
        colour=Colours.RED,
        shape=[
            [1, 0],
            [1, 1],
            [0, 1]
        ]
    ),
    "pen": Tetromino(
        colour=Colours.PURPLE,
        shape=[
            [0, 1],
            [1, 1],
            [0, 1]
        ]
    )
}
