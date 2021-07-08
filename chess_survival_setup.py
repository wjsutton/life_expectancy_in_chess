from itertools import islice, cycle
import chess.pgn
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import glob
import datetime

def match_survival(pgn):
    start_positions = pd.read_csv('data\\start_positions.csv')

    first_game = chess.pgn.read_game(pgn)

    site = first_game.headers['Site']
    black_elo = first_game.headers['BlackElo']
    white_elo = first_game.headers['WhiteElo']
    opening = first_game.headers['Opening']
    board = first_game.board()

    print(site)

    san_list = []
    lan_list = []
    site_list = []
    black_elo_list = []
    white_elo_list = []
    opening_list = []

    for move in first_game.mainline_moves():
        san = board.san(move)
        lan = board.lan(move)
        san_list.append(san)
        lan_list.append(lan)
        site_list.append(site)
        black_elo_list.append(black_elo)
        white_elo_list.append(white_elo)
        opening_list.append(opening)
        board.push(move)

    df = pd.DataFrame()

    df['Site'] = site_list
    df['SAN'] = san_list
    df['LAN'] = lan_list
    df['BlackElo'] = black_elo_list
    df['WhiteElo'] = white_elo_list
    df['Opening'] = opening_list

    pat = ['white','black']
    df = df.assign(player=[*islice(cycle(pat), len(df))])
        
    df['LAN'] = df['LAN'].str.replace('O-O-O','O-OO',regex=False)
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
            df['LAN'].str.contains('x'),
            df['LAN'].str.contains('=Q'),
            df['LAN'].str.contains(r'\+'),
            df['LAN'].str.contains('-')
            
        ], 
        [
            'checkmate',
            'kill',
            'promoted to queen',
            'check',
            'move'
        ], 
        default='Unknown'
    )
    df['index'] = df.index
    df.to_csv('data\\ks_castling_df.csv', index=False)
    # queen side castling
    qs_castling = df.loc[df['LAN'] == 'O-O']

    if len(qs_castling)>0:
        #print('Queen side Castling!')
        white_qs_castling = pd.DataFrame()
        black_qs_castling = pd.DataFrame()
        for i in range(len(qs_castling)):
            if qs_castling.iloc[i]['player'] == 'black':
                black_qs_castling['Site'] = [qs_castling.iloc[i]['Site'],qs_castling.iloc[i]['Site']]
                black_qs_castling['SAN'] = [qs_castling.iloc[i]['SAN'],qs_castling.iloc[i]['SAN']]
                black_qs_castling['LAN'] = [qs_castling.iloc[i]['LAN'],qs_castling.iloc[i]['LAN']]
                black_qs_castling['BlackElo'] = [black_elo,black_elo]
                black_qs_castling['WhiteElo'] = [white_elo,white_elo]
                black_qs_castling['Opening'] = [opening,opening]
                black_qs_castling['player'] = [qs_castling.iloc[i]['player'],qs_castling.iloc[i]['player']]
                black_qs_castling['from_and_piece'] = ['e8','h8']
                black_qs_castling['to_and_result'] = ['g8','f8']
                black_qs_castling['from'] = ['e8','h8']
                black_qs_castling['to'] = ['g8','f8']
                black_qs_castling['piece_moved'] = ['King','Rook']
                black_qs_castling['action'] = [qs_castling.iloc[i]['action'],qs_castling.iloc[i]['action']]
                black_qs_castling['index'] = [qs_castling.iloc[i]['index'],qs_castling.iloc[i]['index']]
            else:
                white_qs_castling['Site'] = [qs_castling.iloc[i]['Site'],qs_castling.iloc[i]['Site']]
                white_qs_castling['SAN'] = [qs_castling.iloc[i]['SAN'],qs_castling.iloc[i]['SAN']]
                white_qs_castling['LAN'] = [qs_castling.iloc[i]['LAN'],qs_castling.iloc[i]['LAN']]
                white_qs_castling['BlackElo'] = [black_elo,black_elo]
                white_qs_castling['WhiteElo'] = [white_elo,white_elo]
                white_qs_castling['Opening'] = [opening,opening]
                white_qs_castling['player'] = [qs_castling.iloc[i]['player'],qs_castling.iloc[i]['player']]
                white_qs_castling['from_and_piece'] = ['e1','h1']
                white_qs_castling['to_and_result'] = ['g1','f1']
                white_qs_castling['from'] = ['e1','h1']
                white_qs_castling['to'] = ['g1','f1']
                white_qs_castling['piece_moved'] = ['King','Rook']
                white_qs_castling['action'] = [qs_castling.iloc[i]['action'],qs_castling.iloc[i]['action']]
                white_qs_castling['index'] = [qs_castling.iloc[i]['index'],qs_castling.iloc[i]['index']]

        if (len(white_qs_castling) + len(black_qs_castling))>1:
            replacement_moves = white_qs_castling.append(black_qs_castling)
        elif len(black_qs_castling)>1:
            replacement_moves = black_qs_castling
        else: 
            replacement_moves = white_qs_castling
        
        other_moves = df.loc[df['LAN'] != 'O-O']
        df = other_moves.append(replacement_moves)

        df = df.sort_values(by=['index'])
        df = df.reset_index(drop=True)
        df['index'] = df.index

    # king side castling
    ks_castling = df.loc[df['LAN'] == 'O-OO']
    if len(ks_castling)>0:
        #print('King side Castling!')
        #print(ks_castling)
        white_ks_castling = pd.DataFrame()
        black_ks_castling = pd.DataFrame()
        for i in range(len(ks_castling)):
            if ks_castling.iloc[i]['player'] == 'black':
                black_ks_castling['Site'] = [ks_castling.iloc[i]['Site'],ks_castling.iloc[i]['Site']]
                black_ks_castling['SAN'] = [ks_castling.iloc[i]['SAN'],ks_castling.iloc[i]['SAN']]
                black_ks_castling['LAN'] = [ks_castling.iloc[i]['LAN'],ks_castling.iloc[i]['LAN']]
                black_ks_castling['BlackElo'] = [black_elo,black_elo]
                black_ks_castling['WhiteElo'] = [white_elo,white_elo]
                black_ks_castling['Opening'] = [opening,opening]
                black_ks_castling['player'] = [ks_castling.iloc[i]['player'],ks_castling.iloc[i]['player']]
                black_ks_castling['from_and_piece'] = ['e8','a8']
                black_ks_castling['to_and_result'] = ['c8','d8']
                black_ks_castling['from'] = ['e8','a8']
                black_ks_castling['to'] = ['c8','d8']
                black_ks_castling['piece_moved'] = ['King','Rook']
                black_ks_castling['action'] = [ks_castling.iloc[i]['action'],ks_castling.iloc[i]['action']]
                black_ks_castling['index'] = [ks_castling.iloc[i]['index'],ks_castling.iloc[i]['index']]
            else:
                white_ks_castling['Site'] = [ks_castling.iloc[i]['Site'],ks_castling.iloc[i]['Site']]
                white_ks_castling['SAN'] = [ks_castling.iloc[i]['SAN'],ks_castling.iloc[i]['SAN']]
                white_ks_castling['LAN'] = [ks_castling.iloc[i]['LAN'],ks_castling.iloc[i]['LAN']]
                white_ks_castling['BlackElo'] = [black_elo,black_elo]
                white_ks_castling['WhiteElo'] = [white_elo,white_elo]
                white_ks_castling['Opening'] = [opening,opening]
                white_ks_castling['player'] = [ks_castling.iloc[i]['player'],ks_castling.iloc[i]['player']]
                white_ks_castling['from_and_piece'] = ['e1','a1']
                white_ks_castling['to_and_result'] = ['c1','d1']
                white_ks_castling['from'] = ['e1','a1']
                white_ks_castling['to'] = ['c1','d1']
                white_ks_castling['piece_moved'] = ['King','Rook']
                white_ks_castling['action'] = [ks_castling.iloc[i]['action'],ks_castling.iloc[i]['action']]
                white_ks_castling['index'] = [ks_castling.iloc[i]['index'],ks_castling.iloc[i]['index']]

        if (len(white_ks_castling) + len(black_ks_castling))>1:
            replacement_moves = white_ks_castling.append(black_ks_castling)
        elif len(black_ks_castling)>1:
            replacement_moves = black_ks_castling
        else: 
            replacement_moves = white_ks_castling

        #print(replacement_moves)
        other_moves = df.loc[df['LAN'] != 'O-OO']
        df = other_moves.append(replacement_moves)
        df = df.sort_values(by=['index'])
        df = df.reset_index(drop=True)
        df['index'] = df.index

        #df.to_csv('data\\df_test.csv')

    for i in df['index']:
        current_move = df.loc[df['index'] == i]

        en_passant = 'zzz'

        if (current_move['piece_moved'].item() == 'Pawn') & (current_move['action'].item() == 'kill'): 
            en_passant = current_move['to'][i][:1] + current_move['from'][i][1]


        a = start_positions.loc[start_positions['start'] == current_move['from'][i]]
        b = start_positions.loc[start_positions['start'] != current_move['from'][i]]
        c = start_positions.loc[start_positions['start'] == current_move['to'][i]]
        d = start_positions.loc[(start_positions['piece'] == 'Pawn') & (start_positions['start'] == en_passant)]

        a.loc[a['start'] == current_move['from'][i], 'start'] = current_move['to'][i]
        a = a.reset_index(drop=True)

        taken = ''

        # if there is a piece occupying the to destination set it as taken
        if len(d['id']) >0:
            d = d.reset_index(drop=True)
            taken = d['id'][0]

        if len(c['id']) >0:
            c = c.reset_index(drop=True)
            taken = c['id'][0]

        # set taken pieces position to null
        b.loc[b['id'] == taken, 'start'] = None

        entry = { 
            'index': i,
            'piece_id': a['id'],
            'killed': taken}

        entry_df = pd.DataFrame(entry)

        #if len(entry_df)>1:
            #print('Hey Will!')
            #print(entry_df)

        if i == 0:
            kill_df = entry_df

        if i > 0:
            kill_df = kill_df.append(entry_df)

        start_positions = a.append(b)


    df['player_name'] = np.where(df['player']=='white', first_game.headers['White'], first_game.headers['Black'])
    result = np.where(first_game.headers['Result']=='1-0','white wins',np.where(first_game.headers['Result']=='0-1','black wins','draw'))
    df['result'] = np.where(df['player']=='white',result,result)
    start_positions['result'] = np.where(start_positions['player']=='white',result,result)
    start_positions['Site'] = np.where(start_positions['player']=='white',df['Site'][0],df['Site'][0])
    start_positions['survived'] = np.where(start_positions['start'].isnull(),False,True)
    start_positions['victory'] = np.where(start_positions['player'] == start_positions['result'].str[:5],False,True)
    start_positions['survived_or_victory'] = np.where(start_positions['piece'] == 'King',start_positions['victory'],start_positions['survived'])

    match_name_df = df[['player','player_name']].drop_duplicates()
    match_name = match_name_df['player_name'][0] + ' ('+match_name_df['player'][0]+') vs ' + match_name_df['player_name'][1] + ' ('+match_name_df['player'][1]+')'

    start_positions['match_name'] = match_name
    df['match_name'] = match_name

    df = pd.merge(df,kill_df,on='index', how='inner')
    start_positions = pd.merge(start_positions,kill_df, left_on='id',right_on='killed', how='left')

    del start_positions['index']
    del start_positions['killed']
    start_positions.rename(columns={'piece_id':'killed_by'}, inplace = True)

    match_df = df.reset_index(drop=True)
    survival_df = start_positions.reset_index(drop=True)

    return match_df, survival_df



def death_positions(match_file,survival_file):
    match_df = pd.read_csv(match_file)
    survival_df = pd.read_csv(survival_file)

    rates = pd.read_csv('data\\chess_piece_survival_rates.csv')
    del rates['piece']
    del rates['player']

    survival_df = pd.merge(survival_df,rates, on ='id',how='inner')

    white_checkmate = match_df.loc[(match_df['piece_id'] == 'B-K') & (match_df['result'] == 'white wins') ]
    black_checkmate = match_df.loc[(match_df['piece_id'] == 'W-K') & (match_df['result'] == 'black wins') ]

    if len(white_checkmate) > 0:
        white_checkmate = white_checkmate.loc[white_checkmate['index'] == max(white_checkmate['index'])]

    if len(black_checkmate) > 0:
        black_checkmate = black_checkmate.loc[black_checkmate['index'] == max(black_checkmate['index'])]

    checkmate_df = pd.concat([white_checkmate,black_checkmate])

    white_lastmove = match_df.loc[(match_df['result'] == 'white wins')][['Site','index']]
    black_lastmove = match_df.loc[(match_df['result'] == 'black wins')][['Site','index']]

    white_lastmove = white_lastmove.groupby(['Site'],as_index=False)['index'].agg({'index':'max'})
    white_lastmove = pd.merge(match_df,white_lastmove,on = ['index','Site'],how='inner')
    white_lastmove['killed'] = 'B-K'
    white_lastmove = white_lastmove[['Site','killed','piece_id']]

    black_lastmove = black_lastmove.groupby(['Site'],as_index=False)['index'].agg({'index':'max'})
    black_lastmove = pd.merge(match_df,black_lastmove,on = ['index','Site'],how='inner')
    black_lastmove['killed'] = 'W-K'
    black_lastmove = black_lastmove[['Site','killed','piece_id']]

    lastmove_df = pd.concat([white_lastmove,black_lastmove])
    checkmate_df = pd.merge(checkmate_df[['Site','BlackElo','WhiteElo','Opening','to']],lastmove_df,on = 'Site',how='inner')


    death_df = match_df[['Site','BlackElo','WhiteElo','Opening','to','killed','piece_id']]
    death_df = death_df[death_df['killed'].notnull()]
    death_df = death_df.loc[death_df['killed'] != '']

    if len(checkmate_df) > 0:
        death_df = pd.concat([death_df,checkmate_df])

    death_df.columns = ['Site','BlackElo','WhiteElo','Opening','death_position','killed_piece_id','killed_by_piece_id']

    death_df['BlackElo'] = death_df['BlackElo'].astype(str)
    death_df['WhiteElo'] = death_df['WhiteElo'].astype(str)

    death_df['BlackElo'] = death_df['BlackElo'].str.replace('?','0',regex=False)
    death_df['WhiteElo'] = death_df['WhiteElo'].str.replace('?','0',regex=False)

    death_df['BlackElo'] = death_df['BlackElo'].str.replace('.*[-].*','0',regex=True)
    death_df['WhiteElo'] = death_df['WhiteElo'].str.replace('.*[-].*','0',regex=True)

    death_df['BlackElo'] = death_df['BlackElo'].fillna(0)
    death_df['WhiteElo'] = death_df['WhiteElo'].fillna(0)
    death_df['BlackElo'] = death_df['BlackElo'].astype(int)
    death_df['WhiteElo'] = death_df['WhiteElo'].astype(int)

    death_df['BlackElo_broad'] =  np.select(
                [
                    death_df['BlackElo'] == 0,
                    death_df['BlackElo'] < 1250,
                    death_df['BlackElo'] < 1500,
                    death_df['BlackElo'] < 1750,
                    death_df['BlackElo'] >= 1750
                    
                ], 
                [
                    'Unknown',
                    '0-1249',
                    '1250-1499',
                    '1500-1749',
                    '1750+'
                ], 
                default='Unknown'
            )

    death_df['WhiteElo_broad'] =  np.select(
                [
                    death_df['WhiteElo'] == 0,
                    death_df['WhiteElo'] < 1250,
                    death_df['WhiteElo'] < 1500,
                    death_df['WhiteElo'] < 1750,
                    death_df['WhiteElo'] >= 1750
                    
                ], 
                [
                    'Unknown',
                    '0-1249',
                    '1250-1499',
                    '1500-1749',
                    '1750+'
                ], 
                default='Unknown'
            )

    death_df['Opening'] = death_df['Opening'].fillna('Unknown')

    death_df['Opening_broad'] =  np.select(
                [
                    death_df['Opening'].str.contains('Sicilian Defense'),
                    death_df['Opening'].str.contains('French Defense'),
                    death_df['Opening'].str.contains("Queen's Pawn Game"),
                    death_df['Opening'].str.contains("Scandinavian Defense"),
                    death_df['Opening'].str.contains("King's Pawn Game"),
                    death_df['Opening'].str.contains("Queen's Gambit"),
                    death_df['Opening'].str.contains("King's Gambit")
                    
                ], 
                [
                    'Sicilian Defense',
                    'French Defense',
                    "Queen's Pawn Game",
                    "Scandinavian Defense",
                    "King's Pawn Game",
                    "Queen's Gambit",
                    "King's Gambit"
                ], 
                default='Other'
            )

    return death_df