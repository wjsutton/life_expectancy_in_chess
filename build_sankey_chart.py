# Build Sankey Chart
import chess_survival_setup as chess_setup
import numpy as np

match_file = 'data\\match_timeline.csv'
survival_file = 'data\\match_survival.csv'

death_df = chess_setup.death_positions(match_file,survival_file)

total_matches = death_df['Site'].nunique()

#print(total_matches)

#print(death_df.columns)
output_df = death_df[['BlackElo_broad','WhiteElo_broad','Opening_broad','killed_piece_id','killed_by_piece_id']]
output_df = output_df.groupby(['BlackElo_broad','WhiteElo_broad','Opening_broad','killed_piece_id','killed_by_piece_id']).size().reset_index(name='counts')
output_df['total_matches'] = total_matches
output_df['link'] = 'link'

output_df['team'] = output_df['killed_piece_id'].str[:1]

output_df['killed_piece'] = np.select(
            [
                output_df['killed_piece_id'].str[2:3] == 'P', 
                output_df['killed_piece_id'].str[2:3] == 'R',
                output_df['killed_piece_id'].str[2:3] == 'B',
                output_df['killed_piece_id'].str[2:3] == 'N',
                output_df['killed_piece_id'].str[2:3] == 'Q',
                output_df['killed_piece_id'].str[2:3] == 'K'
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

output_df['killer_piece'] = np.select(
            [
                output_df['killed_by_piece_id'].str[2:3] == 'P', 
                output_df['killed_by_piece_id'].str[2:3] == 'R',
                output_df['killed_by_piece_id'].str[2:3] == 'B',
                output_df['killed_by_piece_id'].str[2:3] == 'N',
                output_df['killed_by_piece_id'].str[2:3] == 'Q',
                output_df['killed_by_piece_id'].str[2:3] == 'K'
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


output_df.to_csv('data\\sankey_death_statistics.csv', index=False)
