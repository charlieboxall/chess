import pygame as pg
from Settings import *
from Pieces import *
import Engine
pg.init()


def load_imgs():
    for piece in pieces_start_pos:

        IMAGES[piece] = pg.transform.scale(
            pg.image.load("images/" + piece + ".png"), 
            (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(SCREEN, white_turn, origin_pos=None, previous_move=None):
    for row in range(DIMENSION):
        for col in range(DIMENSION):

            # Checkerboard pattern
            # Even row starts with white
            if row % 2 == 0:
                color = COLOR_1

                # Change colour to black when odd column
                if not(col % 2 == 0):
                    color = COLOR_2
            # Odd row starts with black
            else:
                color = COLOR_2

                # Change colour to white when odd column
                if not(col % 2 == 0):
                    color = COLOR_1

            pg.draw.rect(SCREEN, color, pg.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if previous_move and len(previous_move) == 2:
        pg.draw.rect(SCREEN, PM_COLOR, pg.Rect(previous_move[0][1]*SQUARE_SIZE, previous_move[0][0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pg.draw.rect(SCREEN, PM_COLOR, pg.Rect(previous_move[1][1]*SQUARE_SIZE, previous_move[1][0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    if origin_pos:
        pg.draw.rect(SCREEN, (0,0,0), pg.Rect(origin_pos[1]*SQUARE_SIZE, origin_pos[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

def draw_pieces(SCREEN, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != ' ':
                SCREEN.blit(IMAGES[piece], pg.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_state(SCREEN, GAME_STATE, origin_pos, previous_move):
    draw_board(SCREEN, GAME_STATE.white_turn, origin_pos, previous_move)
    draw_pieces(SCREEN, GAME_STATE.board)

def main():
    SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pg.time.Clock()
    GAME_STATE = Engine.State()
    load_imgs()
    play: bool = True
    square_selected: tuple = () # Keeps track of the current square selected
    player_selects: list = [] # Keeps track of the the squares the player has selected
    origin_pos: tuple = ()
    previous_move: list = [] # Keeps track of the previous move made by a player
    valid_moves = GAME_STATE.get_valid_moves() # Gather all the valid moves
    move_made: bool = False

    while play:
        for event in pg.event.get():

            # QUIT EVENT
            if event.type == pg.QUIT:
                play: bool = False
            
            # MOUSE CLICK EVENT
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos: tuple = pg.mouse.get_pos()

                # Helps to understand which piece has been selected
                row: int = pos[1]//SQUARE_SIZE
                col: int = pos[0]//SQUARE_SIZE

                # Has the user double clicked on a square?
                if square_selected == (row,col):
                    square_selected = ()
                    player_selects = []
                    origin_pos = ()
                
                # If there hasn't been a double click
                else:
                    square_selected = (row, col)
                    origin_pos = square_selected
                    player_selects.append(square_selected)
                
                # Is this the user's second select? - (where they want their first select to go)
                if len(player_selects) == 2:
                    # Actually make the move the user has selected
                    move = Engine.Move(player_selects[0], player_selects[1], GAME_STATE.board)

                    if move in valid_moves:
                        GAME_STATE.move_piece(move)
                        move_made = True

                        # Set previous move
                        previous_move = player_selects

                        # Reset selected squares
                        square_selected = ()
                        player_selects = []
                        origin_pos = ()
                    else:
                        player_selects = [square_selected]

            # ONLY if a new move has been made, then generate the new set of valid moves
            # as this is an expensive function
            if move_made:
                valid_moves = GAME_STATE.get_valid_moves()
                move_made = False

        CLOCK.tick(MAX_FPS)
        draw_state(SCREEN, GAME_STATE, origin_pos, previous_move)
        pg.display.flip()

if __name__ == "__main__":
    main()

