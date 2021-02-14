
from itertools import islice, cycle
import chess.pgn
import pandas as pd

with open("data/lichess_db_standard_rated_2013-01.pgn") as pgn:
    first_game = chess.pgn.read_game(pgn)

board = first_game.board()

san_list = []
lan_list = []

for move in first_game.mainline_moves():
    san = board.san(move)
    lan = board.lan(move)
    san_list.append(san)
    lan_list.append(lan)
    board.push(move)

df = pd.DataFrame()

df['SAN'] = san_list
df['LAN'] = lan_list

pat = ['white','black']
df = df.assign(player=[*islice(cycle(pat), len(df))])

print(df)