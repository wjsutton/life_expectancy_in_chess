import chess_survival_setup as chess_setup
import chess.pgn

counter = -1
skip = 3
process = 3

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

match_df.to_csv('data\\test_match_timeline.csv', index=False)
survival_df.to_csv('data\\test_match_survival.csv', index=False)


match_file = 'data\\test_match_timeline.csv'
survival_file = 'data\\test_match_survival.csv'

death_df = chess_setup.death_positions(match_file,survival_file)

output_df = death_df[['BlackElo_broad','WhiteElo_broad','Opening_broad','death_position','killed_piece_id','killed_by_piece_id']]
output_df = output_df.groupby(['BlackElo_broad','WhiteElo_broad','Opening_broad','death_position','killed_piece_id','killed_by_piece_id']).size().reset_index(name='counts')

#death_df.to_csv('data\\match_death_positions.csv', index=False)
#output_df.to_csv('data\\overall_death_statistics.csv', index=False)
