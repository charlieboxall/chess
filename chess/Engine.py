from Pieces import *
from translate import *

class State:

    def __init__(self):
        # First char represents colour of piece
        # Second char represents type of piece
        # ' ' represents an empty space on the board
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.setup_board()

        self.white_turn: bool = True # Since white always starts
        self.move_log: list = [] # Keep a log base of all the moves made

        # Keep track of where the kings are on the board - for checks, checkmate, stalemate and castling
        self.white_king_pos = pieces_start_pos["wK"]
        self.black_king_pos = pieces_start_pos["bK"]
        self.currently_in_check = False
        self.pins = []
        self.checks = []

    def setup_board(self):
        for piece in pieces_start_pos:
            for pos in pieces_start_pos[piece]:
                self.board[pos[0]][pos[1]] = piece
    
    def enemy_color(self):
        # Determine whose turn it is
        return "b" if self.white_turn else "w"
    
    def current_color(self):
        # Determine whose turn it is
        return "w" if self.white_turn else "b"
        
    def move_piece(self, move):
        # Move the piece selected
        self.board[move.start_row][move.start_col] = ' '
        self.board[move.destination_row][move.destination_col] = move.piece_moved

        # Log the move that has just been made
        self.move_log.append(move) 

        # Change user turn
        self.white_turn = not self.white_turn

        # Change king's location if it has been moved
        if move.piece_moved == "wK":
            self.white_king_pos = (move.destination_row, move.destination_col)
        elif move.piece_moved == "bK":
            self.black_king_pos = (move.destination_row, move.destination_col)
    
    def pawn_moves(self, row, col, moves):
        # White pawn moves
        # Moving up the board therefore need to minus the row
        if self.white_turn:

            # Is there an empty square ahead?
            if self.board[row-1][col] == ' ':
                moves.append(Move((row, col), (row-1, col), self.board))

                # Has the white pawn moved yet?
                if row == 6 and self.board[row-2][col] == ' ':
                    moves.append(Move((row, col), (row-2, col), self.board))

            # Handle diag captures
            if col-1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))

        # Black pawn moves
        # Moving down the board therefore plus to row
        else:

            # Is there an empty square ahead?
            if self.board[row+1][col] == ' ':
                moves.append(Move((row, col), (row+1, col), self.board))
                
                # Has the black pawn moved yet?
                if row == 1 and self.board[row+2][col] == ' ':
                    moves.append(Move((row, col), (row+2, col), self.board))

            # Handle diag captures
            if col-1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))
            
    def rook_bishop_moves(self, row, col, moves, directions):
        enemy = self.enemy_color()

        for direction in directions:
            for i in range(1,8):
                destination_row = row + direction[0] * i
                destination_col = col + direction[1] * i

                # Check if the rook is still on the board
                if 0 <= destination_row <= 7 and 0 <= destination_col <= 7:
                    destination = self.board[destination_row][destination_col]

                    # Is there an empty space on the destination square?
                    if destination == ' ':
                        moves.append(Move((row, col), (destination_row, destination_col), self.board))
                    
                    # Is there an enemy piece on the destination square?
                    elif destination[0] == enemy: 
                        moves.append(Move((row, col), (destination_row, destination_col), self.board))
                        break
                    
                    # Otherwise its a piece of own colour
                    else:
                        break
                else:
                    break

    def knight_moves(self, row, col, moves):
        enemy = self.enemy_color()

        for direction in knight_directions:
            destination_row = row + direction[0]
            destination_col = col + direction[1]

            # Check if the rook is still on the board
            if 0 <= destination_row <= 7 and 0 <= destination_col <= 7:
                destination = self.board[destination_row][destination_col]

                # Is there an enemy piece or an empty space on the destination square?
                if destination[0] in [enemy, ' ']:
                    moves.append(Move((row, col), (destination_row, destination_col), self.board))

    def queen_moves(self, row, col, moves):
        self.rook_bishop_moves(row, col, moves, rook_directions)
        self.rook_bishop_moves(row, col, moves, bishop_directions)


    def king_moves(self, row, col, moves):
        enemy = self.enemy_color()

        for i in range(8):
            destination_row = row + king_directions[i][0]
            destination_col = col + king_directions[i][1]

            # Check if the rook is still on the board
            if 0 <= destination_row <= 7 and 0 <= destination_col <= 7:
                destination = self.board[destination_row][destination_col]

                # Is there an enemy piece or an empty space on the destination square?
                if destination[0] in [enemy, ' ']:
                    moves.append(Move((row, col), (destination_row, destination_col), self.board))

    def get_all_moves(self):
        all_moves: list = []

        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                
                # Access whose turn it is and check if it's their turn to go
                if (self.board[row][col][0] == "w" and self.white_turn) or (self.board[row][col][0] == "b" and not(self.white_turn)):

                    # Acess the piece type
                    piece = self.board[row][col][1].lower()
                    if piece == "p":
                        self.pawn_moves(row, col, all_moves)
                    elif piece == "r":
                        self.rook_bishop_moves(row, col, all_moves, rook_directions)
                    elif piece == "n":
                        self.knight_moves(row, col, all_moves)
                    elif piece == "b":
                        self.rook_bishop_moves(row, col, all_moves, bishop_directions)
                    elif piece == "q":
                        self.queen_moves(row, col, all_moves)
                    elif piece == "k":
                        self.king_moves(row, col, all_moves)
        return all_moves

    def check_pins_checks(self):
        currently_in_check = False
        pins = []
        checks = []
        enemy = self.enemy_color()
        current = self.current_color()
        start_row, start_col = self.white_king_pos if self.white_turn else self.black_king_pos

        for i in range(len(king_directions)):
            direction = king_directions[i]
            possible_pin = ()
            
            for j in range(1,8):
                destination_row = start_row + direction[0] * j
                destination_col = start_col + direction[1] * j

                # Still on board?
                if 0 <= destination_row <= 7 and 0 <= destination_col <= 7:
                    destination = self.board[destination_row][destination_col]

                    if destination[0] == current:

                        # First current colour piece can be pinned
                        if possible_pin == ():
                            possible_pin = (destination_row, destination_col, direction[0], direction[1])

                        # Second current colour piece, therefore no pins or checks possible in this direction
                        else:
                            break

                    elif destination[0] == enemy:
                        type = destination[1].lower()
                        
                        # Check directions corresponding to piece type
                        if (0 <= i <= 3 and type == "r") or \
                            (4 <= i <= 7 and type == "b") or \
                                (i == 1 and type == "p" and ((enemy == "w" and 6 <= i <= 7) or (enemy == "b" and 4 <= i <= 5))) or \
                                    (type == "q") or (i == 1 and type == "k"):

                            # No pieces blocking, therefore in check
                            if possible_pin == ():
                                currently_in_check = True
                                checks.append((destination_row, destination_col, direction[0], direction[1]))
                                break

                            # Piece blocking, therefore pinned
                            else:
                                pins.append(possible_pin)
                                break
                        
                        # No checks being applied
                        else:
                            break
                
                # Not on board
                else:
                    break
        
        # Knight checks?
        for direction in knight_directions:
            destination_row = start_row + direction[0]
            destination_col = start_col + direction[1]

            if 0 <= destination_row <= 7 and 0 <= destination_col <= 7:
                destination = self.board[destination_row][destination_col]

                # The knight is attacking the king
                if destination[0] == enemy and destination[1].lower() == "n":
                    currently_in_check = True
                    checks.append((destination_row, destination_col, direction[0], direction[1]))
        
        return currently_in_check, pins, checks

    def get_valid_moves(self):
        
        return self.get_all_moves()

class Move:

    def __init__(self, start_square, destination, board):
        self.start_row, self.start_col = start_square
        self.destination_row, self.destination_col = destination

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_taken = board[self.destination_row][self.destination_col]

        # Creates a unique id for every move
        # For example, if start row = 2, start column = 3, end row = 4, end col = 5
        # Then the unique id for this specific move would be: 2345, as the piece is moving from (2,3) -> (4,5)

        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.destination_row * 10 + self.destination_col

    def get_notation(self):
        return translate_cols[self.start_col] + translate_rows[self.start_row] + translate_cols[self.destination_col] + translate_rows[self.destination_row]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False


