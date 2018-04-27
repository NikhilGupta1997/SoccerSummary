#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect
import re
# Connect to the PostGres Server
cur = connect.connect()

# Get match number to summarize
if len(sys.argv) == 2:
	search_type = 1
else:
	search_type = 2
if search_type == 1:
	match_id = int(sys.argv[1])
else:
	team1 = (sys.argv[1])
	team2 = (sys.argv[2])
	season = (sys.argv[3])
	print(team1)
	print(team2)
	print(season)
	# team1 = 'Liverpool'
	# team2 = 'Manchester City'

location_dict = {
	1	:	"the attacking half",
	2	:	"the defensive half",
	3	:	"the centre of the box",
	4	:	"the left wing",
	5	:	"the right wing",
	6	:	"a difficult angle from long range",
	7	:	"a difficult angle on the left",
	8	:	"a difficult angle on the right",
	9	:	"the left side of the box",
	10	:	"the left side of the six yard box",
	11	:	"the right side of the box",
	12	:	"the right side of the six yard box",
	13	:	"very close range",
	14	:	"the penalty spot",
	15	:	"outside the box",
	16	:	"long range",
	17	:	"more than 35 yards",
	18	:	"more than 40 yards",
	19	:	"not recorded"}

bodypart_dict = {
	1	:	"right foot",
	2	:	"left foot",
	3	:	"head"}

shot_place_dict = {
	1	:	"Bit too high",
	2	:	"Blocked",
	3	:	"Bottom left corner",
	4	:	"Bottom right corner",
	5	:	"Centre of the goal",
	6	:	"High and wide",
	7	:	"Hits the bar",
	8	:	"Misses to the left",
	9	:	"Misses to the right",
	10	:	"Too high",
	11	:	"Top centre of the goal",
	12	:	"Top left corner",
	13	:	"Top right corner"}

def to_str(string):
	return '\'' + string + '\''

def get_match_info(match_id):
	match_info = connect.query_one(cur, 'SELECT * FROM game_info WHERE id = 1;')
	match_commentary = connect.query_mul(cur, 'SELECT * FROM events WHERE id_odsp = ' + to_str(match_info['id_odsp']))
	return match_info, match_commentary	

def get_match_info(team1, team2, season):
	match_info = connect.query_one(cur, 'SELECT * FROM game_info WHERE ht = ' + to_str(team1) + ' AND at = ' + to_str(team2) + ' AND season = ' + season)
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
	# print(match_info['id_odsp'])
	match_line = str(0) + ':' + "This match was between " + match_info['ht'] + ' and ' + match_info['at'] + ' in the ' + str(match_info['season']) + ' season of the ' + match_info['country'] + ' league and was played on ' + str(match_info['date'])  + '\n'
	return [match_line]

def start_line(match_info, match_commentary):
	# TODO : Add features like <players winner/hattrick inspires late comeback etc>. This can include brace, or if keeper does too many saves etc
	# High scoring match
	(win, odds) = winner(match_info)
	start_str = str(0) + ':' + match_info['ht'] + ' ' 

	if(odds > 2):
		start_str += 'unexpectedly '

	if(win == 0):
		start_str += 'defeated '
	elif(win == 1):
		start_str += 'drew with '
	else:
		start_str += 'lost to '

	start_str += match_info['at'] + ' '
	start_str += str(match_info['fthg']) + '-'+ str(match_info['ftag']) + ' at their home ground'
	if(match_info['fthg'] + match_info['ftag'] >= 5):
		start_str += " in a high-scoring contest"
	start_str += ".\n"	
	return [start_str]

def find_dominance(match_info, match_commentary):
	# Identify succesive periods of domination,  

	attacking_opportunities = [1, 2, 8]
	ans = []
	# print type(match_commentary), len(match_commentary)
	period_gap = 10
	period_start = 0
	dominance_diff = 3

	home_team = match_info['ht']
	away_team = match_info['at']
	
	home_attacks_count = 0
	away_attacks_count = 0
	dominance_string = []
	goal_scored = 0
	goal_hm_time = []
	goal_aw_time = []
	for event in match_commentary:
		if(int(event['time']) > (period_start + period_gap)):
			prev_dominance = home_attacks_count - away_attacks_count
			if(prev_dominance > dominance_diff):
				goal_impact = 0
				goal_time = -1
				if(goal_scored > 0):
					# print "yo"
					goal_impact = 1
					goal_time = goal_hm_time[0]
				if(goal_scored < 0):
					goal_impact = -1
					goal_time = goal_aw_time[0]	

				ans.append((goal_impact, goal_time, 0, 0, period_start, period_start + period_gap))
				# dominance_string.append(str(period_start + period_gap) + ':' + home_team + ' started to attack and dominated the possession\n')
			if(prev_dominance < -1 * dominance_diff):
				goal_impact = 0
				goal_time = -1
				
				if(goal_scored < 0):
					goal_impact = 1
					goal_time = goal_aw_time[0]
				if(goal_scored > 0):
					goal_impact = -1
					goal_time = goal_hm_time[0]	
				ans.append((goal_impact, goal_time, 1, 0, period_start, period_start + period_gap))	
				# dominance_string.append(str(period_start + period_gap) + ':' + away_team + ' started to attack and dominated the possession\n')

			period_start += period_gap
			home_attacks_count = 0
			away_attacks_count = 0
			goal_scored = 0
			goal_hm_time = []
			goal_aw_time = []	

		if(event['is_goal']):
			if(event['event_team'] == home_team):
				goal_scored += 1
				goal_hm_time.append(event['time'])
				home_attacks_count += 1
			else:
				goal_scored -= 1
				goal_aw_time.append(event['time'])
				away_attacks_count += 1

		if(int(event['event_type']) in attacking_opportunities):
			if(event['event_team'] == home_team):
				home_attacks_count += 1
			else:
				away_attacks_count += 1	

	for i in range(len(ans)):
		event = ans[i]
		ev_str = ""
		if(event[2] == 0):
			if(event[0] < 0):
				dominance_string.append(str(event[1]) + ':' + home_team + ' started to attack and dominated the possession but ' + away_team + 'scored against the run of play as ')
			elif(event[0] > 0):
				dominance_string.append(str(event[1]) + ':' + home_team + ' started to dominate the game and were rewarded with a goal as')
			else:
				dominance_string.append(str(period_start) + ':' + home_team + ' started to attack and dominated the possession\n')	
		else:
			if(event[0] < 0):
				dominance_string.append(str(event[1]) + ':' + away_team + ' started to attack and dominated the possession but ' + home_team + 'scored against the run of play as')
			elif(event[0] > 0):
				dominance_string.append(str(event[1]) + ':' + away_team + ' started to dominate the game and were rewarded with a goal as')
			else:
				dominance_string.append(str(event[4]) + ':' + away_team + ' started to attack and dominated the possession\n')
		if(i+1 < len(ans)):
			if(ans[i+1][2] == event[2]):
				i += 1
	return dominance_string

def toggle(team):
	if team == 0: return 1
	else: return 0

def check_equal(goals):
	if goals[0] == goals[1]: return True
	else: return False

def assist_desc(player2, assist_method):
	assist = ""
	if assist_method == 1:
		assist += player2 + " provided the assist as" 
	elif assist_method == 2:
		assist += player2 + " provided a great cross into the box as"
	elif assist_method == 3:
		assist += player2 + " provided a headed assist as"
	elif assist_method == 4:

		assist += player2 + " provided a brilliant assist with a perfectly placed through ball into the box as"
	return assist

def goal_desc(player, shot_place, shot_outcome, location, bodypart, situation):
	goal = ""
	if situation == 3:
		goal += "The corner was converted! "
	elif situation == 4:
		goal += "The free kick was converted! "
	if shot_place == -1:
		goal += 'Embarassingly, it was an unlucky own goal.'
	else:
		# TODO : add headed the ball etc, add synonyms for capitalised
		goal += player + " capitalised with his " + bodypart_dict[bodypart] + " to send the ball flying into the " + shot_place_dict[shot_place]
	return goal

def description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation):
	desc_line = ""
	if location == 14:
		desc_line += player + " converted the penalty and sent the ball flying into the " + shot_place_dict[shot_place]
	else:
		desc_line += assist_desc(player2, assist_method)
		desc_line += " " + goal_desc(player, shot_place, shot_outcome, location, bodypart, situation)
	return desc_line + '\n'

def goal_scorer(match_commentary):
	goal_scorer = {}
	goal_line = []
	goals = [0,0]
	for row in match_commentary:
		if row['is_goal']:
			# print(row['player'])
			# print(row['time'])
			team = int(row['side']) - 1
			goals[team] += 1
			other_team = toggle(team)
			equilizer = check_equal(goals)
			player = row['player'].title()
			player2 = row['player2'].title()
			shot_place = row['shot_place']
			shot_outcome = row['shot_outcome']
			location = row['location']
			bodypart = row['bodypart']
			assist_method = row['assist_method']
			situation = row['situation']

			# if(shot_place == -1):
			# 	goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
			# 	continue

			if row['time'] <= 10:
				if goals[team] > goals[other_team]:
					goal_line.append(str(row['time']) + ':' + player + " scored an quick goal to give " + row['event_team'] + " an early lead\n")
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
				elif equilizer:
					goal_line.append(str(row['time']) + ':' + player + " replied swiftly and strongly to get " + row['event_team'] + " the equilizer\n")
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))

			elif row['time'] > 80:
				if goals[team] > goals[other_team] + 1:
					goal_line.append(str(row['time']) + ':' + player + " increased the lead for " + row['event_team'] + " with a goal in the " + str(row['time']) + ' minute\n')
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
				elif goals[team] > goals[other_team]:
					goal_line.append(str(row['time']) + ':' + player + " secured the lead for " + row['event_team'] + " with a goal in the " + str(row['time']) + ' minute\n')
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
				elif equilizer:
					goal_line.append(str(row['time']) + ':' + player + " replied strongly to get " + row['event_team'] + " the much needed equilizer in the final moments of the game\n")
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
				else:
					goal_line.append(str(row['time']) + ':' + player + " continued to fight with a goal for " + row['event_team'] + " in the final moments of the game\n")
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))

			else:
				if equilizer:
					goal_line.append(str(row['time']) + ':' + player + " replied strongly to get " + row['event_team'] + " the much needed equilizer\n")
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
				elif goals[team] > goals[other_team] + 1:
					goal_line.append(str(row['time']) + ':' + player + " scored a goal in the " + str(row['time']) + ' minute to increase the lead for ' + row['event_team'] + '\n')
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
				elif goals[team] > goals[other_team]:
					goal_line.append(str(row['time']) + ':' + player + " scored a goal in the " + str(row['time']) + ' minute to give ' + row['event_team'] + ' the lead\n')
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
				else:
					goal_line.append(str(row['time']) + ':' + player + " scored a goal in the " + str(row['time']) + ' minute\n')
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))

			if player in goal_scorer:
				goal_scorer[player] += 1
			else:
				goal_scorer[player] = 1

			# if goal_scorer[player] > 1:
			# 	if goal_scorer[player] == 2:
			# 		goal_line.append(str(row['time']) + ':' + player + " scored a strong brace\n")
			# 	elif goal_scorer[player] == 3:
			# 		goal_line.append(str(row['time']) + ':' + player + " scored a strong hat-trick\n")
			# 	else:
			# 		goal_line.append(str(row['time']) + ':' + player + " scored an astounding " + str(goal_scorer[player]) + ' goals!\n')

		elif row['location'] == 14:
			goal_line.append(str(row['time']) + ':' + "Disappointingly, " + row['player'].title() + " missed the penalty which " + shot_place_dict[row['shot_place']] + "\n")
	# print(goal_scorer)
	return goal_line
 
def foul_details(match_info, match_commentary):
	foul_string = []
	yellow_cards = []
	home_team = match_info['ht']
	away_team = match_info['at']
	for event in match_commentary:
		# print event
		event_type = event['event_type']
		player = event['player'].title()
		player2 = event['player2'].title()
		team = event['event_team']
		if event_type == 4:
			# continue
			# foul_string.append(str(event['time']) + ':' + player + " was given a yellow card\n")
			yellow_cards.append((event['time'], player, event['event_team']))
		elif event_type == 5:
			foul_string.append(str(event['time']) + ':' + player + " was given a second yellow card and was a big blow to " + team + "\n")
		elif event_type == 6:
			foul_string.append(str(event['time']) + ':' + player + " was given a red card and left " + team + " with a 10 man side\n")
		elif event_type == 11:
			foul_string.append(str(event['time']) + ':' + re.sub('(.*?)', '', event['text']) + "\n")

	period_gap = 15
	period_start = 0
	players_hm = []
	players_aw = []
	# print yellow_cards
	for i in range(len(yellow_cards) + 1):
		if (i<len(yellow_cards)):
			event = yellow_cards[i]
		if(i == len(yellow_cards) or int(event[0]) > (period_start + period_gap)):
			string = ""
			if(len(players_hm) > 0):
				for i in range(len(players_hm)-1):
					string += players_hm[i] +", "
				string += players_hm[len(players_hm)-1] + "("+ home_team +")"
				if(len(players_aw) > 0):
					string += " , "
			if(len(players_aw) > 0):
				for i in range(len(players_aw)-1):
					string += players_aw[i] +", "
				string += players_aw[len(players_aw)-1] + "("+ away_team +")"
			if(len(players_hm) + len(players_aw) == 1):
				string += " was awarded a yellow card."
			if(len(players_hm) + len(players_aw) > 1):
						string += " were awarded yellow cards in a quick succesion."
			if(len(players_hm) + len(players_aw) > 0):
				foul_string.append(str(period_start + period_gap) + ':' + string + "\n")
			players_hm = []
			players_aw = []
			period_start += period_gap
		if(i == len(yellow_cards)):
			continue
		if(event[2] == home_team):
			players_hm.append(event[1])
		else:
			players_aw.append(event[1])
	
	return foul_string

def subsitutions(match_info, match_commentary):
	subs = []
	subsi = []
	home_team = match_info['ht']
	away_team = match_info['at']
	# print match_commentary
	for event in match_commentary:
		event_type = event['event_type']
		player_in = event['player_in'].title()
		player_out = event['player_out'].title()
		# print event['time']
		if event_type == 7:

			subsi.append((event['time'], player_in, player_out, event['event_team']))
			# subs.append(str(event['time']) + ':' + player_in + " was substituted in place of " + player_out + "\n")
	
	period_gap = 15
	period_start = 0

	players_hm_in = []
	players_aw_in = []
	players_hm_out = []
	players_aw_out = []
	# print subsi
	for i in range(len(subsi)+1):
		if(i < len(subsi)):
			event = subsi[i]
		if(i == len(subsi) or int(event[0]) > (period_start + period_gap)):
			string = ""
			if(len(players_hm_in) > 0):
				print "yo"
				for i in range(len(players_hm_in)-1):
					string += players_hm_in[i] +", "
				string += players_hm_in[len(players_hm_in)-1] + " were substituted in for "
				for i in range(len(players_hm_out)-1):
					string += players_hm_out[i] +", "
				string += players_hm_out[len(players_hm_out)-1] + "("+ home_team +")"
				if(len(players_aw_in) > 0):
					string += " while "

			if(len(players_aw_in) > 0):
				for i in range(len(players_aw_in)-1):
					string += players_aw_in[i] +", "
				string += players_aw_in[len(players_aw_in)-1] + " came on for "
				for i in range(len(players_aw_out)-1):
					string += players_aw_out[i] +", "
				string += players_aw_out[len(players_aw_out)-1] + "("+ away_team +")"
			
			if(len(players_hm_in) + len(players_aw_in) > 0):
				subs.append(str(period_start + period_gap) + ':' + string + "\n")

			players_hm_in = []
			players_aw_in = []
			players_hm_out = []
			players_aw_out = []
			period_start += period_gap

		if(event[2] == home_team):
			players_hm_in.append(event[1])
			players_hm_out.append(event[2])
		else:
			players_aw_in.append(event[1])
			players_aw_out.append(event[2])
	print subs
	return subs

def sort_time(timeline):
	timeline = [(int(x.split(':')[0]), x.split(':')[1]) for x in timeline]
	timeline.sort(key=lambda x: x[0])
	return timeline

def summarize(timeline):
	text = ""
	for row in timeline:
		text = text + str(row[0]) + " => " + row[1]
	return text

# print match_info
if search_type == 1:
	match_info, match_commentary = get_match_info(match_id)
else:
	match_info, match_commentary = get_match_info(team1, team2, season)
	
timeline = []
timeline += match_details(match_info)
# print winner(match_info)
timeline += start_line(match_info, match_commentary)
timeline += find_dominance(match_info, match_commentary)
timeline += goal_scorer(match_commentary)
timeline += foul_details(match_info, match_commentary)
timeline += subsitutions(match_info, match_commentary)
timeline = sort_time(timeline)
print(summarize(timeline))
print("Summarization Over")
