import chess_survival_setup as chess


king_takes_self = open('data/test_matches/lichess_pgn_2013.01.01_daredevil_vs_uytku.0odgkjea.pgn')
team_kill = open('data/test_matches/lichess_pgn_2013.01.02_ABUELOENTANGA_vs_habatur.rrlt4u5t.pgn')
team_kill_pawn = open('data/test_matches/lichess_pgn_2013.01.03_ChristlovesU2_vs_Messsi.9t6mw7je.pgn')
king_castling = open('data/test_matches/king_side_castling.pgn')
king_and_queen_castling = open('data/test_matches/king_and_queen_castling.pgn')

#test = chess.match_survival(king_and_queen_castling)
#test[0].to_csv('data\\ks_and_qs_castle_match_timeline.csv', index=False)
#test[1].to_csv('data\\ks_and_qs_castle_match_survival.csv', index=False)

with open('data/standard_matches/lichess_db_standard_rated_2013-01.pgn') as pgn:
    for file in range(1000):
        print(file)
        survive = chess.match_survival(pgn)

        if file == 0:
            match_df = survive[0].reset_index(drop=True)
            survival_df = survive[1].reset_index(drop=True)
        else:
            match_df = match_df.append(survive[0].reset_index(drop=True))
            survival_df = survival_df.append(survive[1].reset_index(drop=True))

match_df.to_csv('data\\match_timeline.csv', index=False)
survival_df.to_csv('data\\match_survival.csv', index=False)


match_file = 'data\\match_timeline.csv'
survival_file = 'data\\match_survival.csv'

death_df = chess.death_positions(match_file,survival_file)

output_df = death_df[['BlackElo_broad','WhiteElo_broad','Opening_broad','death_position','killed_piece_id','killed_by_piece_id']]
output_df = output_df.groupby(['BlackElo_broad','WhiteElo_broad','Opening_broad','death_position','killed_piece_id','killed_by_piece_id']).size().reset_index(name='counts')

death_df.to_csv('data\\match_death_positions.csv', index=False)
output_df.to_csv('data\\overall_death_statistics.csv', index=False)
