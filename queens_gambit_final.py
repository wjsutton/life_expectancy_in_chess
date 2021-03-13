from itertools import islice, cycle
import chess.pgn
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

## To Do
# - Handling for Castling
# - Convert to function

# Source: https://lichess.org/study/AgKEky06

start_positions = pd.read_csv('data\\start_positions.csv')

with open('data/lichess_study_elizabeth-harmon-vasily-borgov-from-netflix-miniseries-queens-gambit_by_k-io1_2020.10.27.pgn') as pgn:
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
print(first_game.headers)

df.to_csv('data\\queens_gambit_moves.csv', index=False)

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
        'piece_id': a['id'],
        'killed': taken}

    entry_df = pd.DataFrame(entry)

    if len(entry_df) > 1:
        print('Hey Will!')
        print(entry_df)

    if i == 0:
        kill_df = entry_df

    if i > 0:
        kill_df = kill_df.append(entry_df)

    start_positions = a.append(b)

print(kill_df)
deceased = kill_df[kill_df['killed'] != '']
#deceased = kill_df[killed].notnull()
print(deceased)
killed_by = deceased[['piece_id','killed']]
killed_by.columns = ['killed_by','id']

start_positions['survived'] = ~start_positions['id'].isin(deceased['killed'])
start_positions = pd.merge(start_positions,killed_by,on='id', how='left')