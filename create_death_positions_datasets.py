import chess_survival_setup as chess_setup
import chess.pgn
import pandas as pd
from pathlib import Path

output_match_file = 'data\\big_viz_match_timeline.csv'
output_survival_file = 'data\\big_viz_match_survival.csv'
output_death_positions_file = 'data\\big_viz_match_death_positions.csv'
output_death_stats_file = 'data\\big_viz_overall_death_statistics.csv'

counter = -1
skip = 0
process = 3

check_dataset = Path(output_survival_file)

if check_dataset.is_file():
    previous_data = pd.read_csv(output_survival_file)
    skip = previous_data['Site'].nunique()

file_list = skip + process

with open('data/standard_matches/lichess_db_standard_rated_2013-01.pgn') as pgn:
    for file in range(file_list):
        print(file)

        if file < skip:
            first_game = chess.pgn.read_game(pgn)
        
        if file >= skip:        
            survive = chess_setup.match_survival(pgn)
            counter = counter + 1

        print(counter)

        if counter == 0:
            match_df = survive[0].reset_index(drop=True)
            survival_df = survive[1].reset_index(drop=True)

        if counter > 0:
            match_df = match_df.append(survive[0].reset_index(drop=True))
            survival_df = survival_df.append(survive[1].reset_index(drop=True))

# if there is previous data append it
if skip > 0:
    previous_match_df = pd.read_csv(output_match_file)
    previous_survival_df = pd.read_csv(output_survival_file)
    match_df = match_df.append(previous_match_df , ignore_index=True)
    survival_df = survival_df.append(previous_survival_df , ignore_index=True)

match_df.to_csv(output_match_file, index=False)
survival_df.to_csv(output_survival_file, index=False)

death_df = chess_setup.death_positions(output_match_file,output_survival_file)

output_df = death_df[['BlackElo_broad','WhiteElo_broad','Opening_broad','death_position','killed_piece_id','killed_by_piece_id']]
output_df = output_df.groupby(['BlackElo_broad','WhiteElo_broad','Opening_broad','death_position','killed_piece_id','killed_by_piece_id']).size().reset_index(name='counts')

death_df.to_csv(output_death_positions_file, index=False)
output_df.to_csv(output_death_stats_file, index=False)
