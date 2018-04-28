import re

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
	-1 	:  	"Penalty",
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
	# 0,1 : $home_team beat/drew with/lost to $_away_team $score at their home ground 
	# 2,3 : $home_team unexpectedly beat/drew with/ surprising lost $score to $away_team at their home ground 
	# TODO : Add features like <players winner/hattrick inspires late comeback etc>. This can include brace, or if keeper does too many saves etc
	
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
	start_str += str(match_info['fthg']) + '-'+ str(match_info['ftag']) + ' at their home ground.\n'
	return [start_str]

def find_dominance(match_info, match_commentary):
	attacking_opportunities = [1, 2, 8]
	ans = []
	# print type(match_commentary), len(match_commentary)
	period_gap = 5
	period_start = 0
	dominance_diff = 2

	home_team = match_info['ht']
	away_team = match_info['at']
	
	home_attacks_count = 0
	away_attacks_count = 0
	dominance_string = []
	for event in match_commentary:
		if(int(event['time']) > (period_start + period_gap)):
			prev_dominance = home_attacks_count - away_attacks_count
			if(prev_dominance > dominance_diff):
				ans.append((0, 0, period_start, period_start + period_gap))
				dominance_string.append(str(period_start + period_gap) + ':' + home_team + ' started to attack and dominated the possession\n')
			if(prev_dominance < -1 * dominance_diff):
				ans.append((1, 0, period_start, period_start + period_gap))	
				dominance_string.append(str(period_start + period_gap) + ':' + away_team + ' started to attack and dominated the possession\n')

			period_start += period_gap
			home_attacks_count = 0
			away_attacks_count = 0

		if(int(event['event_type']) in attacking_opportunities):
			if(event['event_team'] == home_team):
				home_attacks_count += 1
			else:
				away_attacks_count += 1	
	# print dominance_string
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
		assist += "A great assist provided by " + player2 + " with a pass."
	elif assist_method == 2:
		assist += "A brilliant assist provided by " + player2 + " with a great cross into the box."
	elif assist_method == 3:
		assist += "A great assist provided by " + player2 + " with a headed pass."
	elif assist_method == 4:
		assist += "A brilliant assist provided by " + player2 + " with a perfectly placed through ball into the box."
	return assist

def goal_desc(player, shot_place, shot_outcome, location, bodypart, situation):
	goal = ""
	if situation == 3:
		goal += "The corner was converted! "
	elif situation == 4:
		goal += "The free kick was converted! "
	if shot_place == -1:
		goal += 'Embarassingly, ' + player + ' scored an unlucky own goal'
	else:
		goal += player + " took the shot from " + location_dict[location] + " with his " + bodypart_dict[bodypart] + " and sent the ball flying into the " + shot_place_dict[shot_place]
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
			player = row['player']
			if player != None: player = player.title()
			else: player = ''
			player2 = row['player2']
			if player2 != None: player2 = player2.title()
			else: player2 = ''
			shot_place = row['shot_place']
			shot_outcome = row['shot_outcome']
			location = row['location']
			bodypart = row['bodypart']
			assist_method = row['assist_method']
			situation = row['situation']

			if row['time'] <= 10:
				if goals[team] > goals[other_team]:
					goal_line.append(str(row['time']) + ':' + player + " scored an quick goal to give " + row['event_team'] + " an early lead\n")
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
				elif equilizer:
					goal_line.append(str(row['time']) + ':' + player + " replied swiftly and strongly to get " + row['event_team'] + " the equilizer\n")
					goal_line.append(str(row['time']) + ':' + description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation))
			elif row['time'] > 80:
				if goals[team] > goals[other_team] + 1:
					goal_line.append(str(row['time']) + ':' + player + " fortified the lead for " + row['event_team'] + " with a goal in the " + str(row['time']) + ' minute\n')
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
					goal_line.append(str(row['time']) + ':' + player + " scored a goal in the " + str(row['time']) + ' minute to give ' + row['event_team'] + ' a fortified lead\n')
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
			if goal_scorer[player] > 1:
				if goal_scorer[player] == 2:
					goal_line.append(str(row['time']) + ':' + player + " scored a strong brace\n")
				elif goal_scorer[player] == 3:
					goal_line.append(str(row['time']) + ':' + player + " scored a strong hat-trick\n")
				else:
					goal_line.append(str(row['time']) + ':' + player + " scored an astounding " + str(goal_scorer[player]) + ' goals!\n')
		elif row['location'] == 14:
			player = row['player']
			if player != None: player = player.title()
			else: player = ''
			goal_line.append(str(row['time']) + ':' + "Disappointingly, " + player + " missed the penalty which " + shot_place_dict[row['shot_place']] + "\n")
	# print(goal_scorer)
	return goal_line
 
def foul_details(match_commentary):
	foul_string = []
	for event in match_commentary:
		event_type = event['event_type']
		player = event['player']
		if player != None: player = player.title()
		else: player = ''
		player2 = event['player2']
		if player2 != None: player2 = player2.title()
		else: player2 = ''
		team = event['event_team']
		if event_type == 4:
			foul_string.append(str(event['time']) + ':' + player + " was given a yellow card\n")
		elif event_type == 5:
			foul_string.append(str(event['time']) + ':' + player + " was given a second yellow card and was a big blow to " + team + "\n")
		elif event_type == 6:
			foul_string.append(str(event['time']) + ':' + player + " was given a red card and left " + team + " with a 10 man side\n")
		elif event_type == 11:
			foul_string.append(str(event['time']) + ':' + re.sub('(.*?)', '', event['text']) + "\n")
	return foul_string

def subsitutions(match_commentary):
	subs = []
	for event in match_commentary:
		event_type = event['event_type']
		player_in = event['player_in']
		if player_in != None: player_in = player_in.title()
		else: player_in = ''
		player_out = event['player_out']
		if player_out != None: player_out = player_out.title()
		else: player_out = ''
		if event_type == 7:
			subs.append(str(event['time']) + ':' + player_in + " was substituted in place of " + player_out + "\n")
	return subs

def sort_time(timeline):
	timeline = [(int(x.split(':')[0]), x.split(':')[1]) for x in timeline]
	timeline.sort(key=lambda x: x[0])
	return timeline

def summarize(timeline):
	text = ""
	for row in timeline:
		text += row[1]
	return text