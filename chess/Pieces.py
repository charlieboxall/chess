pieces_start_pos = {
    "bR" : [(0,0), (0,7)], 
    "bN" : [(0,1), (0,6)],
    "bB" : [(0,2), (0,5)],
    "bQ" : [(0,3)], 
    "bK" : [(0,4)],
    "bP" : [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
    "wR" : [(7,0), (7,7)],
    "wN" : [(7,1), (7,6)],
    "wB" : [(7,2), (7,5)],
    "wQ" : [(7,3)],
    "wK" : [(7,4)],
    "wP" : [(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7)]
}

rook_directions = [
    (-1,0), # Up
    (1,0), # Down
    (0, -1), # Left
    (0, 1) # Right
]

bishop_directions = [
    (-1,-1), # Up left
    (-1, 1), # Up right
    (1, -1), # Down left
    (1, 1) # Down right
]

knight_directions = [
    (-2, -1), # 2 up 1 left
    (-2, 1), # 2 up 1 right
    (-1, -2), # 1 up 2 left
    (-1, 2), # 1 up 2 right
    (2, -1), # 2 down 1 left
    (2, 1), # 2 down 1 right
    (1, -2), # 1 down 2 left
    (1, 2) # 1 down 2 right
]

king_directions = rook_directions + bishop_directions