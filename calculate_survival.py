
import pandas as pd
import numpy as np

# Load data
survival_stats = pd.read_csv('data\\test_survival_stats2.csv')

# calculate capture rate for kings
survival_stats['captured'] = np.where(survival_stats['player'] == survival_stats['result'].str[:5],False,True)
survival_stats['survived_or_captured'] = np.where(survival_stats['piece'] == 'King',survival_stats['captured'],survival_stats['survived'])
survival_stats['survival_calc'] = np.where(survival_stats['survived_or_captured'] == True,1,0)

# add in column to count pieces on the board
survival_stats['started'] = np.where(survival_stats['survived_or_captured'] == True,1,1)

# group by survival calc for overall, piece and id breakdowns
piece_survival = survival_stats.groupby(['piece'])['survival_calc'].agg('sum')
piece_on_board = survival_stats.groupby(['piece']).sum()
piece_id_survival = survival_stats.groupby(['id'])['survival_calc'].agg('sum')

# survival rate by piece_id
piece_id_survival_rate = (piece_id_survival)/(len(survival_stats)/32)

# survival rate by piece
piece_on_board['piece_survival_rate'] = (piece_on_board['survived_or_captured']/piece_on_board['started'])

# overall survival rate
overall_survival_rate = sum(survival_stats['survival_calc'])/len(survival_stats)

# removing columns ahead of merge
del piece_on_board['survived']
del piece_on_board['captured']
del piece_on_board['survived_or_captured']
del piece_on_board['survival_calc']
del piece_on_board['started']

# creating output dataframe
survival_df = survival_stats[['id','piece','player']].drop_duplicates()
survival_df = pd.merge(survival_df,piece_id_survival_rate,on='id',how='inner')
survival_df = pd.merge(survival_df,piece_on_board,on='piece',how='inner')
survival_df['overall_survival_rate'] = overall_survival_rate

# tidying columns and output to csv
survival_df.columns = ['id','piece','player','piece_id_survival_rate','piece_survival_rate','overall_survival_rate']
survival_df.to_csv('data\\chess_piece_survival_rates.csv', index=False)