from itertools import islice, cycle
import chess.pgn
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

with open('data/lichess_db_standard_rated_2013-01.pgn') as pgn:
    for file in range(1000):

        start_positions = pd.read_csv('data\\start_positions.csv')
        
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
        

        df['LAN'] = df['LAN'].str.replace('O-O-O','O-OO',regex=False)
        df[['from_and_piece', 'to_and_result']] = df['LAN'].str.split('-|x',expand=True)
        df['LAN'] = df['LAN'].str.replace('O-OO','O-O-O',regex=False)

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

        # queen side castling
        qs_castling = df.loc[df['LAN'] == 'O-O']

        if len(qs_castling)>0:
            print('Queen side Castling!')
            white_qs_castling = pd.DataFrame()
            black_qs_castling = pd.DataFrame()
            for i in range(len(qs_castling)):
                if qs_castling.iloc[i]['player'] == 'black':
                    black_qs_castling['Site'] = [qs_castling.iloc[i]['Site'],qs_castling.iloc[i]['Site']]
                    black_qs_castling['SAN'] = [qs_castling.iloc[i]['SAN'],qs_castling.iloc[i]['SAN']]
                    black_qs_castling['LAN'] = [qs_castling.iloc[i]['LAN'],qs_castling.iloc[i]['LAN']]
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
            df = df.reset_index()
            df['index'] = df.index
            df = df.drop('level_0', axis=1)  

        # king side castling
        ks_castling = df.loc[df['LAN'] == 'O-O-O']
        if len(ks_castling)>0:
            print('King side Castling!')
            white_ks_castling = pd.DataFrame()
            black_ks_castling = pd.DataFrame()
            for i in range(len(ks_castling)):
                if ks_castling.iloc[i]['player'] == 'black':
                    black_ks_castling['Site'] = [ks_castling.iloc[i]['Site'],ks_castling.iloc[i]['Site']]
                    black_ks_castling['SAN'] = [ks_castling.iloc[i]['SAN'],ks_castling.iloc[i]['SAN']]
                    black_ks_castling['LAN'] = [ks_castling.iloc[i]['LAN'],ks_castling.iloc[i]['LAN']]
                    black_ks_castling['player'] = [ks_castling.iloc[i]['player'],ks_castling.iloc[i]['player']]
                    black_qs_castling['from_and_piece'] = ['e8','a8']
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

            other_moves = df.loc[df['LAN'] != 'O-O-O']
            df = other_moves.append(replacement_moves)
            df = df.sort_values(by=['index'])
            df = df.reset_index()
            df['index'] = df.index
            df = df.drop('level_0', axis=1)  


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

            b.loc[b['id'] == taken, 'start'] = None

            entry = { 
                'index': i,
                'piece_id': a['id'],
                'killed': taken}

            entry_df = pd.DataFrame(entry)

            if len(entry_df)>1:
                print('Hey Will!')
                print(entry_df)

            if i == 0:
                kill_df = entry_df

            if i > 0:
                kill_df = kill_df.append(entry_df)

            start_positions = a.append(b)

        #print(kill_df)
        deceased = kill_df[kill_df['killed'] != '']
        #deceased = kill_df[killed].notnull()
        #print(deceased)
        killed_by = deceased[['piece_id','killed']]
        killed_by.columns = ['killed_by','id']

        start_positions['survived'] = ~start_positions['id'].isin(deceased['killed'])
        start_positions = pd.merge(start_positions,killed_by,on='id', how='left')

        #df['player_name'] = np.where(df['player']=='white', first_game.headers['White'], first_game.headers['Black'])
        result = np.where(first_game.headers['Result']=='1-0','white wins',np.where(first_game.headers['Result']=='0-1','black wins','draw'))
        start_positions['result'] = np.where(start_positions['player']=='white',result,result)
        start_positions['Site'] = np.where(start_positions['player']=='white',df['Site'][0],df['Site'][0])


        print(str(file) +' - df row count: '+str(len(df)) +' - start_positions row count: '+str(len(start_positions)))
        if file == 0:
            output_df = start_positions
        else:
            output_df = output_df.append(start_positions)

print('Done!')
print(len(output_df))

output_df.to_csv('data\\test_survival_stats.csv', index=False)

