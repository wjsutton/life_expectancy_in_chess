
from itertools import islice, cycle
import chess.pgn
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

## Tasks

# To Do
# - Turn into function
# - Output datasets [Match Metadata, Game Details, Piece details (survived, movement, etc.)] 

# Done 
# - Work out piece id, e.g. White Pawn starting on E2
# - Work out which pieces are taken

start_positions = pd.read_csv('data\\start_positions.csv')

with open("data/lichess_db_standard_rated_2013-01.pgn") as pgn:
    first_game = chess.pgn.read_game(pgn)

site = first_game.headers['Site']
board = first_game.board()

san_list = []
lan_list = []
site_list = []

for move in first_game.mainline_moves():
    san = board.san(move)
    lan = board.lan(move)
    san_list.append(san)
    lan_list.append(lan)
    site_list.append(site)
    board.push(move)

df = pd.DataFrame()

df['Site'] = site_list
df['SAN'] = san_list
df['LAN'] = lan_list

pat = ['white','black']
df = df.assign(player=[*islice(cycle(pat), len(df))])

df[['from_and_piece', 'to_and_result']] = df['LAN'].str.split('-|x',expand=True)

df['from'] = df['from_and_piece'].str.strip().str[-2:] 
df['to'] = df['to_and_result'].str.strip().str[0:2]

df['piece_moved'] = np.select(
    [
        df['from_and_piece'].str.len() == 2, 
        df['from_and_piece'].str[0] == 'R',
        df['from_and_piece'].str[0] == 'B',
        df['from_and_piece'].str[0] == 'N',
        df['from_and_piece'].str[0] == 'Q',
        df['from_and_piece'].str[0] == 'K'
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

df['action'] =  np.select(
    [
        df['LAN'].str.contains('#'),
        df['LAN'].str.contains('-'), 
        df['LAN'].str.contains('x')
        
    ], 
    [
        'checkmate',
        'move', 
        'kill'
    ], 
    default='Unknown'
)
df['index'] = df.index

print(df)

match_metadata = { 'Event': [first_game.headers['Event']],
'Site': [first_game.headers['Site']],
'Date': [first_game.headers['Date']],
'Round': [first_game.headers['Round']],
'White': [first_game.headers['White']],
'Black': [first_game.headers['Black']],
'Result': [first_game.headers['Result']],
'BlackElo': [first_game.headers['BlackElo']],
'BlackRatingDiff': [first_game.headers['BlackRatingDiff']],
'ECO': [first_game.headers['ECO']],
'Opening': [first_game.headers['Opening']],
'Termination': [first_game.headers['Termination']],
'TimeControl': [first_game.headers['TimeControl']],
'UTCDate': [first_game.headers['UTCDate']],
'UTCTime': [first_game.headers['UTCTime']],
'WhiteElo': [first_game.headers['WhiteElo']],
'WhiteRatingDiff': [first_game.headers['WhiteRatingDiff']]}

match_meta_df = pd.DataFrame(match_metadata)

print(start_positions)

for i in df['index']:
    current_move = df.loc[df['index'] == i]

    a = start_positions.loc[start_positions['start'] == current_move['from'][i]]
    b = start_positions.loc[start_positions['start'] != current_move['from'][i]]
    c = start_positions.loc[start_positions['start'] == current_move['to'][i]]

    a.loc[a['start'] == current_move['from'][i], 'start'] = current_move['to'][i]
    a = a.reset_index(drop=True)

    taken = ''

    if len(c['id']) >0:
        c = c.reset_index(drop=True)
        taken = c['id'][0]

    entry = { 
        'index': i,
        'piece_id': [a['id'][0]],
        'killed': taken}

    entry_df = pd.DataFrame(entry)

    if i == 0:
        kill_df = entry_df

    if i > 0:
        kill_df = kill_df.append(entry_df)

    start_positions = a.append(b)

print(kill_df)


