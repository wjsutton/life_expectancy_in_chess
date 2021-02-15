
from itertools import islice, cycle
import chess.pgn
import pandas as pd
import numpy as np

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


df[['from', 'to']] = df['LAN'].str.split('-|x',expand=True)

df['piece_moved'] = np.select(
    [
        df['from'].str.len() == 2, 
        df['from'].str[0] == 'R',
        df['from'].str[0] == 'B',
        df['from'].str[0] == 'N',
        df['from'].str[0] == 'Q',
        df['from'].str[0] == 'K'
    ], 
    [
        'Pawn', 
        'Rook',
        'Bishop',
        'Knight',
        'Queen',
        'King'
    ], 
    default='Unknown'
)

print(df)