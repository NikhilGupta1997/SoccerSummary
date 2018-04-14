#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect

# Connect to the PostGres Server
cur = connect.connect()

# Get match number to summarize
search_type = int(sys.argv[1])
if search_type == 1:
	match_id = int(sys.argv[2])
else:
	# team1 = (sys.argv[2])
	# team2 = (sys.argv[3])
	team1 = 'Manchester Utd'
	team2 = 'Manchester City'

def to_str(string):
	return '\'' + string + '\''

def get_match_info(match_id):
	match_info = connect.query_one(cur, 'SELECT * FROM game_info WHERE id = 1;')
	match_commentary = connect.query_mul(cur, 'SELECT * FROM events WHERE id_odsp = ' + to_str(match_info['id_odsp']))
	return match_info, match_commentary	

def get_match_info(team1, team2):
	match_info = connect.query_one(cur, 'SELECT * FROM game_info WHERE ht = ' + to_str(team1) + ' AND at = ' + to_str(team2))
	match_commentary = connect.query_mul(cur, 'SELECT * FROM events WHERE id_odsp = ' + to_str(match_info['id_odsp']))
	return match_info, match_commentary	

def winner(match_info):
	win = 1 
	expect = 0 
	if(int(match_info['fthg']) > int(match_info['ftag'])):
		win = 0
	elif(int(match_info['fthg']) < int(match_info['ftag'])):
		win = 2	
	odd_result = match_info['odd_a']
	if(win == 0):
		odd_result = float(match_info['odd_h'])
	elif(win == 1):
		odd_result = float(match_info['odd_d'])

	temp = int(1.0*(odd_result-2)/1.5 + 1)
	if(temp > 3):
		temp = 4
	return (win, temp)	

def match_details(match_info):
	match_line = "Match between " + match_info['ht'] + ' and ' + match_info['at'] + ' in the ' + str(match_info['season']) + ' season of the ' + match_info['country'] + ' league, being played on ' + str(match_info['date'])
	return match_line

def start_line(match_info, match_commentary):
	# 0,1 : $home_team beat/drew with/lost to $_away_team $score at their home ground 
	# 2,3 : $home_team unexpectedly beat/drew with/ surprising lost $score to $away_team at their home ground 
	# TODO : Add features like <players winner/hattrick inspires late comeback etc>. This can include brace, or if keeper does too many saves etc
	
	(win, odds) = winner(match_info)
	start_str = match_info['ht'] + ' ' 

	if(odds > 2):
		start_str = 'unexpectedly '

	if(win == 0):
		start_str = start_str + 'defeated '
	elif(win == 1):
		start_str = start_str + 'drew with '
	else:
		start_str = start_str + 'lost to '

	start_str += match_info['at'] + ' '
	start_str += str(match_info['fthg']) + '-'+ str(match_info['ftag']) + ' at their home ground.'
	return start_str

def find_dominance(match_info, match_commentary):
	attacking_opportunities = [1, 2, 8]
	ans = []
	print type(match_commentary), len(match_commentary)
	period_gap = 5
	period_start = 0
	dominance_diff = 2

	home_team = match_info['ht']
	away_team = match_info['at']
	
	home_attacks_count = 0
	away_attacks_count = 0

	for event in match_commentary:
		if(int(event['time']) > (period_start + period_gap)):
			prev_dominance = home_attacks_count - away_attacks_count
			if(prev_dominance > dominance_diff):
				ans.append((0, 0, period_start, period_start + period_gap))
			if(prev_dominance < -1 * dominance_diff):
				ans.append((1, 0, period_start, period_start + period_gap))	

			period_start += period_gap
			home_attacks_count = 0
			away_attacks_count = 0

		if(int(event['event_type']) in attacking_opportunities):
			if(event['event_team'] == home_team):
				home_attacks_count += 1
			else:
				away_attacks_count += 1	
	return ans

def goal_scorer(match_commentary):
	goal_scorer = {}
	for row in match_commentary:
		if row['is_goal']:
			print(row['player'])
			if row['player'] in goal_scorer:
				goal_scorer[row['player']] += 1
			else:
				goal_scorer[row['player']] = 1
	print(goal_scorer)
 

# print match_info
if search_type == 1:
	match_info, match_commentary = get_match_info(match_id)
else:
	match_info, match_commentary = get_match_info(team1, team2)
print match_details(match_info)
print winner(match_info)
print start_line(match_info, match_commentary)
goal_scorer(match_commentary)




