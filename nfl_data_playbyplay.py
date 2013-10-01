import pandas as pd
import numpy as np
import scipy.stats as stats

np.set_printoptions(linewidth = 400)
pd.set_option('line_width', 400)
pd.set_option('max_rows', None)
pd.set_option('max_columns', None)


df2012 = pd.read_csv('2012_nfl_pbp_data_reg_season.csv')

def parse_into_game_data():
	all_games = []
	for k, v in df2012.groupby('gameid'):
		win_loss = pd.DataFrame(v[['nextscore', 'teamwin', 'off', 'def']].iloc[0]).T
		_scoredb = pd.DataFrame(v[['offscore', 'defscore', 'off', 'def']].tail(1))

		if k[9:] == win_loss['off'] + '@' + win_loss['def']:
		# if k.index(win_loss['off']) < k.index(win_loss['def']):
			win_loss['away'] = win_loss['off']
			win_loss['home'] = win_loss['def']
			home = win_loss['def']
		else:
			win_loss['away'] = win_loss['def']
			win_loss['home'] = win_loss['off']
			home = win_loss['off']

		if home == _scoredb['off']:
			win_loss['home_score'] = _scoredb['offscore'].values[0]
			win_loss['away_score'] = _scoredb['defscore'].values[0]
		elif home == _scoredb['def']:
			win_loss['home_score'] = _scoredb['defscore'].values[0]
			win_loss['away_score'] = _scoredb['offscore'].values[0]

		for i, j in v.groupby('off'):
			_first_downs = sum(j[j['down'] == 1]['down'])
			if i == home:
				win_loss['home_first_dwns'] = _first_downs
			else:
				win_loss['away_first_dwns'] = _first_downs

		if win_loss['teamwin'] == 1:
			if win_loss['nextscore'] > 0:
				win_loss['first_score'] = 1
				if win_loss['nextscore'] <=3:
					win_loss['first_score_fg'] = 1
				elif win_loss['nextscore'] > 3:
					win_loss['first_score_td'] = 1
			else:
				win_loss['first_score'] = 0					
			# if win_loss['home'] == win_loss['off']:
			# 	win_loss['home_team_win'] = 1

		win_loss.drop(['off', 'def', 'teamwin'], axis = 1)
		all_games.append(win_loss)
	all_games_df = pd.concat(all_games, ignore_index=True)


all_games_df['home_team_win'] = (all_games_df['home_score'] > all_games_df['away_score']).astype('int64')





	# def check_if_win(row):
	# 	first_score = 0
	# 	if row['teamwin'] == 1:
	# 		if row['nextscore'] > 0:
	# 			first_score = 1
	# 			if row['nextscore'] <=3:
	# 				first_score_fg = 1
	# 			elif row['nextscore'] > 3:
	# 				first_score_td = 1
	# 		else:
	# 			first_score = 0
	# 	return first_score
	# all_games_df['first_score_won'] = all_games_df.apply(check_if_win, axis = 1)


aa = all_games_df[all_games_df['first_score'] == 1]