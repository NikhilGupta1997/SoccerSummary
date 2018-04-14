#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################


import csv
import sys

text_data = {}
# event_data = []
meta_data = {}


# Get match number to summarize
# match_id = int(sys.argv[1])
# print match_id

def csv_dict_reader(file_obj):
	reader = csv.DictReader(file_obj, delimiter=',')
	for line in reader:
		if(line['id_odsp'] not in text_data):
			text_data[line['id_odsp']] = [line]
		else:
			text_data[line['id_odsp']].append(line)			 
		# event_data.append(int(line['event_type']))

def csv_meta_data(file_obj):
	reader = csv.DictReader(file_obj, delimiter=',')
	for line in reader:
		meta_data[line['id_odsp']] = line
	
with open("./football-events/events.csv") as f_obj:
	csv_dict_reader(f_obj)

with open("./football-events/ginf.csv") as f_obj:
	csv_meta_data(f_obj)

# (Home team, Away team, Home Team Score, Away Team Score, odds_home, odds_draw, odds_against)
def get_match_info(match_id):
	info = meta_data[match_id]
	return info
# returns (winner:(0:home/1:draw/2:away), expectation(0:expected, 1:close, 2:shock, 3:unbelievable) 
# Add features like close match, high scoring

def winner(match_info):
	win = 1 
	expect = 0 
	# print match_info
	# print int(match_info['fthg']), int(match_info['ftag'])
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
	start_str += match_info['fthg'] + '-'+ match_info['ftag'] + ' at their home ground.'

	return start_str

# Return list of tuples (dominating_tema(0: home, 1 : away), after_goal or not(0-> no goal, 1-> home goal, 2->away goal), start time, end time) 
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
	
	# After and Before a Goal domination also
	

	
				




match_info = get_match_info('UFot0hit/')
match_commentary = text_data['UFot0hit/']

print match_info
print winner(match_info)
print start_line(match_info, match_commentary)
print find_dominance(match_info, match_commentary)


