import chess.pgn

with open("data/lichess_db_standard_rated_2013-01.pgn") as pgn:
    first_game = chess.pgn.read_game(pgn)

#print(first_game) # .headers)
print(first_game.mainline_moves())

board = first_game.board()

for move in first_game.mainline_moves():
    print(board.san(move))
    board.push(move)

