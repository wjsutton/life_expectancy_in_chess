import chess_survival_setup as chess


king_takes_self = open('data/test_matches/lichess_pgn_2013.01.01_daredevil_vs_uytku.0odgkjea.pgn')
team_kill = open('data/test_matches/lichess_pgn_2013.01.02_ABUELOENTANGA_vs_habatur.rrlt4u5t.pgn')
team_kill_pawn = open('data/test_matches/lichess_pgn_2013.01.03_ChristlovesU2_vs_Messsi.9t6mw7je.pgn')
king_castling = open('data/test_matches/king_side_castling.pgn')
king_and_queen_castling = open('data/test_matches/king_and_queen_castling.pgn')
castling_with_check = open('data/test_matches/castling_with_check.pgn')

test = chess.match_survival(castling_with_check)
test[0].to_csv('data\\check_castle_match_timeline.csv', index=False)
test[1].to_csv('data\\check_castle_match_survival.csv', index=False)

match_file = 'data\\check_castle_match_timeline.csv'
survival_file = 'data\\check_castle_match_survival.csv'

death_df = chess.death_positions(match_file,survival_file)

print(death_df)
