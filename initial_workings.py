import chess.pgn
import chess

with open("data/lichess_db_standard_rated_2013-01.pgn") as pgn:
    first_game = chess.pgn.read_game(pgn)

#print(first_game) # .headers)
#print(first_game.mainline_moves())



board = first_game.board()

#for move in first_game.mainline_moves():
#    print(board.san(move))
#    print(board.lan(move))
#    board.push(move)
    #print(board.lan(move))

#df = pd.DataFrame(columns=["SAN", "LAN"])

print(first_game.mainline_moves())

rows = [[board.lan(move), board.lan(move)] for move in first_game.mainline_moves()]
print(rows)

for move in first_game.mainline_moves():
    b = board.lan(move)
    print(move)
    print([b,type(b)])
    #a = a.append(b)
    board.push(move)

presidents = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
for num, name in enumerate(presidents, start=1):
    print("President {}: {}".format(num, name))

for num, name in enumerate(first_game.mainline_moves(), start=1):
    print("President {}: {}".format(num,name))

#df = [x for move in first_game.mainline_moves() return board.lan(move)]
print(a)
#input_just_vowels = [x for x in str_list if x in vowels]