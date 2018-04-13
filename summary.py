#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv

text_data = {}
# event_data = []
meta_data = {}


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
	# return (info['ht'], info['at'], info['fthg'], info['ftag'], info['odd_h'], info['odd_d'], info['odd_a'])
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


match_info = get_match_info('UFot0hit/')
match_commentary = meta_data['UFot0hit/']

print match_info
print winner(match_info)
print start_line(match_info, match_commentary)


