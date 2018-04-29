import re

goal_count = 0

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

goals_home = {}
goals_away = {}
yellow_cards_home = {}
yellow_cards_away = {}

subsitutions_home_in = []
subsitutions_home_out = []
subsitutions_away_in = []
subsitutions_away_out = []
red_home = 0
red_away = 0
max_home_deficit = 0
max_away_deficit = 0

def stats(match_commentary, match_info):
	global red_away, red_home, max_home_deficit, max_away_deficit
	global goals_home
	global goals_away
	global yellow_cards_home
	global yellow_cards_away
	global subsitutions_home_in
	global subsitutions_home_out
	global subsitutions_away_in
	global subsitutions_away_out
	goals_home = {}
	goals_away = {}
	yellow_cards_home = {}
	yellow_cards_away = {}
	subsitutions_home_in = []
	subsitutions_home_out = []
	subsitutions_away_in = []
	subsitutions_away_out = []

	home_team = match_info['ht']
	away_team = match_info['at']
	home_score = 0 
	away_score = 0 
	
	for event in match_commentary:
		player = event['player']
		if player != None: player = player.title()
		else: player = ''

		if(event['event_type'] == 5 or event['event_type'] == 6):
			if(event['event_team'] == home_team):
				red_home += 1
			else:
				red_away += 1	

		if event['is_goal']:
			

			if(event['event_team'] == home_team):
				home_score += 1
				if((home_score- away_score) > max_away_deficit):
					max_away_deficit = home_score - away_score

				if(player not in goals_home):
					goals_home[player] = []
				goals_home[player].append(event['time'])
			else:
				away_score += 1
				if((away_score - home_score) > max_home_deficit):
					max_home_deficit = away_score - home_score

				if(player not in goals_away):
					goals_away[player] = []
				# print player	
				goals_away[player].append(event['time'])

		elif(event['event_type'] == 4 or event['event_type'] == 5):

			if(event['event_team'] == home_team):
				if(player not in yellow_cards_home):
					yellow_cards_home[player] = []
				yellow_cards_home[player].append(event['time'])
			else:
				if(player not in yellow_cards_away):
					yellow_cards_away[player] = []
				yellow_cards_away[player].append(event['time'])	

		elif(event['event_type'] == 7):
			player_in = event['player_in']
			if player_in != None: player_in = player_in.title()
			else: player_in = ''
			player_out = event['player_out']
			if player_out != None: player_out = player_out.title()
			else: player_out = ''
			if(event['event_team'] == home_team):
				subsitutions_home_in.append(player_in)
				subsitutions_home_out.append(player_out)
			else:
				subsitutions_away_in.append(player_in)
				subsitutions_away_out.append(player_out)

def attempts(match_info, match_commentary):

	hgoals = int(match_info['fthg']) 
	agoals = int(match_info['ftag'])

	home_team = match_info['ht']
	away_team = match_info['at']
	home_attempts = []
	away_attempts = []
	attempt = []
	for event in match_commentary:
		event_type = event['event_type']
		shot_outcome = event['shot_outcome']
		open_play = event['situation']
		player = event['player']
		if(event_type != 1):
			continue
		if(shot_outcome == 4):
			string = event['event_team'] + " came close to scoring in the "+ str(event['time'])  +" minute as " + player + "'s effort hit the bar"
			if(open_play == 4):
				string += " through a direct free-kick"		
			attempt.append(str(event['time']) + ': ' + string +".\n")
		elif(hgoals == 0 and event['event_team'] == home_team):
			if(shot_outcome == 3):
				string = event['event_team'] + " missed an opportunity to score in the "+ str(event['time'])  +" minute as " + player + "'s effort was blocked"
				attempt.append(str(event['time']) + ': ' + string +".\n")
		elif(agoals == 0 and event['event_team'] == away_team):
			if(shot_outcome == 3):
				string = event['event_team'] + " got a chance to score in the "+ str(event['time'])  +" minute as " + player + "'s effort was blocked"
				attempt.append(str(event['time']) + ': ' + string +".\n")				
	return attempt		

			

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
	match_line = str(0) + ':' + "This match was between " + match_info['ht'] + ' and ' + match_info['at'] + ' in the ' + str(match_info['season']) + ' season of the ' + match_info['country'] + ' league and was played on ' + str(match_info['date'])  + '.\n'
	return [match_line]

def start_line(match_info, match_commentary):
	# TODO : Add features like <players winner/hattrick inspires late comeback etc>. This can include brace, or if keeper does too many saves etc
	# High scoring match
	(win, odds) = winner(match_info)
	
	home_num = 11 - red_home
	away_num = 11 - red_away

	if(home_num == 11):
		start_str = str(0) + ': ' + match_info['ht'] + ' ' 
	else:
		start_str = str(0) + ': ' + str(home_num) + " man "+ match_info['ht'] + ' ' 

	if(odds > 2 and (home_num + away_num) == 22):
		start_str += 'unexpectedly '

	if(win == 0):
		start_str += 'defeated '
	elif(win == 1):
		start_str += 'drew with '
	else:
		start_str += 'lost to '
	if(away_num != 11):
		start_str += str(away_num) + ' man '
	start_str += match_info['at'] + ' '

	start_str += str(match_info['fthg']) + '-'+ str(match_info['ftag']) + ' at their home ground'
	
	if(match_info['fthg'] + match_info['ftag'] == 0):
		start_str += " in a dull draw"
	elif(abs(match_info['fthg'] - match_info['ftag']) > 3):
		start_str += " in an one-sided contest"
	elif(match_info['fthg'] + match_info['ftag'] >= 5):
		start_str += " in a high-scoring contest"
	start_str += ". "

	hattrick = []
	brace = []

	# Star of the show , who scored the winner, comeback or not
	for key, value in goals_home.iteritems():
		if(len(value) >= 3):
			hattrick.append((key, 0))
		elif (len(value) == 2):
			brace.append((key, 0))				
	for key, value in goals_away.iteritems():
		if(len(value) >= 3):
			hattrick.append((key, 1))
		elif (len(value) == 2):
			brace.append((key, 1))				

	if(len(hattrick) > 0):
		for i in range(len(hattrick) - 1):
			(player, team) = hattrick[i]
			start_str += player +", "
		start_str += hattrick[len(hattrick) - 1][0] + " scored hattrick"

	elif(len(brace) > 0):
		for i in range(len(brace) - 1):
			(player, team) = brace[i]
			start_str += player +", "
		start_str += brace[len(brace) - 1][0] + " scored a brace"

	result = "win"
	if(win == 1):
		result ="draw"
	if((win == 0 or win == 1) and max_home_deficit > 0):
		if(len(brace) + len(hattrick) > 0):
			if(max_home_deficit == 1):
				start_str += " as "+ match_info['ht'] +" came back from a goal down to "+ result + " the match" 
			else:
				start_str += " as "+ match_info['ht'] +" came back from "+ str(max_home_deficit) +" goals down to "+ result + " the match" 
		else:
			if(max_home_deficit == 1):
				start_str += " " + match_info['ht'] +" had to come back from a goal down to "+ result + " the match" 
			else:
				start_str += " " + match_info['ht'] +" had to come back from "+ str(max_home_deficit) +" goals down to "+ result + " the match" 

	if((win == 2 or win == 1) and max_away_deficit > 0):
		if(len(brace) + len(hattrick) > 0):
			if(max_away_deficit == 1):
				start_str += " as "+ match_info['at'] +" came back from a goal down to "+ result + " the match" 
			else:
				start_str += " as "+ match_info['at'] +" came back from "+ str(max_away_deficit) +" goals down to "+ result + " the match" 
		else:
			if(max_home_deficit == 1):
				start_str +=  " " + match_info['at'] +" had to come back from a goal down to "+ result + " the match" 
			else:
				start_str +=  " " + match_info['at'] +" had to come back from "+ str(max_away_deficit) +" goals down to "+ result + " the match" 

	start_str += ".\n"	
	return [start_str]

def find_dominance(match_info, match_commentary):
	
	attacking_opportunities = [1, 2, 8]
	ans = []
	
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

			while(int(event['time']) > (period_start + 2*period_gap)):
				period_start += period_gap
			
			prev_dominance = home_attacks_count - away_attacks_count
			if(prev_dominance > dominance_diff):
				goal_impact = 0
				goal_time = -1
				if(goal_scored > 0):
					goal_impact = 1
					goal_time = goal_hm_time[0]

				if(goal_scored < 0):
					goal_impact = -1
					goal_time = goal_aw_time[0]	

				ans.append((goal_impact, goal_time, 0, 0, period_start, period_start + period_gap))

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

	flag = False	
	max_i = -1
	for i in range(len(ans)):
		event = ans[i]
		ev_str = ""

		if i < max_i:
			# flag = False
			continue
		f_str = "started"
		# if()
		if(event[2] == 0):
			if(event[0] < 0):
				dominance_string.append(str(event[1]) + ': ' + home_team + ' started to attack and dominated the possession but ' + away_team + 'scored against the run of play as ')
			elif(event[0] > 0):
				dominance_string.append(str(event[1]) + ': ' + home_team + ' started to dominate the game and were rewarded with a goal as')
			else:
				if(event[4] == 90):
					dominance_string.append(str(event[4]) + ': ' + home_team + ' dominated the last part of the match till the final whistle blew\n')
				elif(event[4] == 0):
					dominance_string.append(str(event[4]) + ': ' + home_team + ' started to attack and dominated the possession right from the start of the match.\n')	
				else:
					dominance_string.append(str(event[4]) + ': ' + home_team + ' started to attack and dominated the possession around the ' + str(event[4]) + ' minute mark.\n')	
		else:
			if(event[0] < 0):
				dominance_string.append(str(event[1]) + ': ' + away_team + ' started to attack and dominated the possession but ' + home_team + 'scored against the run of play as')
			elif(event[0] > 0):
				dominance_string.append(str(event[1]) + ': ' + away_team + ' started to dominate the game and were rewarded with a goal as')
			else:
				if(int(event[4]) == 90):
					dominance_string.append(str(event[4]) + ': ' + away_team + ' dominated the last part of the match till the final whistle blew\n')
				elif(int(event[4]) == 0):
					dominance_string.append(str(event[4]) + ': ' + away_team + ' started to attack and dominated the possession at the start of the match.\n')
				else:	
					dominance_string.append(str(event[4]) + ': ' + away_team + ' started to attack and dominated the possession around the ' + str(event[4]) + ' minute mark.\n')
		max_i = i
		while(max_i+1 < len(ans) and ans[max_i+1][2] == ans[max_i][2]):
			max_i += 1
		max_i += 1
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

def goal_desc(player, shot_place, shot_outcome, location, bodypart, situation, assist_method):
	global goal_count
	goal = ""

	if situation == 3:
		goal += " The corner was converted. "
	elif situation == 4:
		goal += " The free kick was converted. "
	if situation == -1:
		goal += ' Embarassingly , it was an unlucky own goal'
	else:
		# TODO : add headed the ball etc, add synonyms for capitalised
		if(goal_count % 3 == 0):
			if(bodypart != 3):
				goal += player + " capitalised with his " + bodypart_dict[bodypart] + " to send the ball into the " + shot_place_dict[shot_place]
			else:
				goal += player + " headed the ball into the " + shot_place_dict[shot_place]
		elif(goal_count % 3 == 1):
			if(bodypart != 3):
				goal += player + " took the shot with his " + bodypart_dict[bodypart] 
			else:
				goal += player + " headed the ball into the goal"
		else:
			if(bodypart != 3):
				goal += player + " took the shot with his " + bodypart_dict[bodypart] 
			else:
				goal += player + " headed the ball into the goal"
	goal_count += 1
	goal += '.'
	return goal 

def description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation):
	desc_line = ""
	if(assist_method == 0 and situation != -1):
		return desc_line
	if location == 14:
		desc_line += " " + player + " converted the penalty by shooting into  " + shot_place_dict[shot_place]
	else:
		if(assist_method != 0):
			desc_line += assist_desc(player2, assist_method)
		desc_line += " " + goal_desc(player, shot_place, shot_outcome, location, bodypart, situation, assist_method)
	return desc_line + '\n'

def goal_num(player, time, team):
	if(team == 0):
		goal_times = goals_home[player]
	else:
		goal_times = goals_away[player]
	for i in range(len(goal_times)):
		if(goal_times[i] == int(time)):
			return i
	return 0				

def goal_scorer(match_commentary):
	goal_scorer = {}
	goal_line = []
	goals = [0,0]
	eq_num = [0,0]
	for row in match_commentary:
		if row['is_goal']:
			team = int(row['side']) - 1
			goals[team] += 1
			other_team = toggle(team)
			equilizer = check_equal(goals)
			if(equilizer):
				eq_num[team] += 1
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
			if(int(row['event_type2']) == 15):
				situation = -1
			
			desc_goal = description(player, player2, shot_place, shot_outcome, location, bodypart, assist_method, situation)
			num_goal = goal_num(player, row['time'], team)
			
			if row['time'] <= 10:
				if goals[team] > goals[other_team]:
					goal_line.append(str(row['time']) + ': ' + player + " scored a quick goal to give " + row['event_team'] + " an early lead.\n")
					
				elif equilizer:
					goal_line.append(str(row['time']) + ': ' + player + " replied swiftly and strongly to get " + row['event_team'] + " the equilizer in the " + str(row['time']) + ' minute.\n')
					goal_line.append(str(row['time']) + ': ' + desc_goal)
			
			elif (row['time'] > 30 and goals[team] + goals[other_team] == 1):
				goal_line.append(str(row['time']) + ': ' + player + " finally broke the deadlock by scoring for " + row['event_team'] + " in the " + str(row['time']) + ' minute.\n')
			
			elif row['time'] > 80:
				if goals[team] > goals[other_team] + 1:
					if(num_goal == 0):
						goal_line.append(str(row['time']) + ': ' + player + " increased the lead for " + row['event_team'] + " with a goal in the " + str(row['time']) + ' minute.\n')
					elif(num_goal == 2):
						goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick for " + row['event_team'] + " by scoring in the " + str(row['time']) + ' minute.\n')
					else:
						goal_line.append(str(row['time']) + ': ' + player + " increased the lead for " + row['event_team'] + " with another goal in the " + str(row['time']) + ' minute.\n')
	
				elif goals[team] > goals[other_team]:
					if(num_goal == 0):
						goal_line.append(str(row['time']) + ': ' + player + " secured the lead for " + row['event_team'] + " with a goal in the " + str(row['time']) + ' minute.\n')
					elif(num_goal == 2):
						goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick for " + row['event_team'] + " by scoring in the " + str(row['time']) + ' minute.\n')
					else:
						goal_line.append(str(row['time']) + ': ' + player + " gained the lead for " + row['event_team'] + " with another goal in the " + str(row['time']) + ' minute.\n')
		
					
				elif equilizer:
					if(eq_num[team] > 1):
						if(num_goal == 2):
							goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick to equalise again for "+ row['event_team'] +" in the final moments of the game.\n")			
						else:	
							goal_line.append(str(row['time']) + ': ' + player + " scored for " + row['event_team'] + " to equalise again in the final moments of the game.\n")
					else:	
						if(num_goal == 2):
							goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick to get " + row['event_team'] + " the much needed equilizer in the final moments of the game.\n")
						else:	
							goal_line.append(str(row['time']) + ': ' + player + " replied strongly to get " + row['event_team'] + " the much needed equilizer in the final moments of the game.\n")
				else:
					if(num_goal == 2):
						goal_line.append(str(row['time']) + ': ' + player + " continued the fightback with his 3rd goal for " + row['event_team'] + " in the final moments of the game.\n")
					else:	
						goal_line.append(str(row['time']) + ': ' + player + " continued the fightback with a goal for " + row['event_team'] + " in the final moments of the game.\n")

			else:
				if equilizer:
					if(eq_num[team] > 1):
						if(num_goal == 2):
							goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick to score another equaliser for " + row['event_team'] + " in the " + str(row['time']) + ' minute.\n')
						else:
							goal_line.append(str(row['time']) + ': ' + player + " scored another equaliser for " + row['event_team'] + " in the " + str(row['time']) + ' minute.\n')
					else:
						if(num_goal == 2):		
							goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick to get " + row['event_team'] + " the much needed equilizer in the " + str(row['time']) + ' minute.\n')
						else:
							goal_line.append(str(row['time']) + ': ' + player + " replied strongly to get " + row['event_team'] + " the much needed equilizer in the " + str(row['time']) + ' minute.\n')

				elif goals[team] > goals[other_team] + 1:
					if(num_goal == 0):
						goal_line.append(str(row['time']) + ': ' + player + " scored in the " + str(row['time']) + ' minute to increase the lead for ' + row['event_team'] + '.\n')
					elif(num_goal == 2):
						goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick in the " + str(row['time']) + ' minute to increase the lead for ' + row['event_team'] + '.\n')
					else:
						goal_line.append(str(row['time']) + ': ' + player + " scored again in the " + str(row['time']) + ' minute to increase the lead for ' + row['event_team'] + '.\n')
		
			
				elif goals[team] > goals[other_team]:
					if(num_goal == 0):
						goal_line.append(str(row['time']) + ': ' + player + " scored in the " + str(row['time']) + ' minute to give ' + row['event_team'] + ' the lead.\n')
					elif(num_goal ==2):
						goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick in the " + str(row['time']) + ' minute to give ' + row['event_team'] + ' the lead.\n')
					else:
						goal_line.append(str(row['time']) + ': ' + player + " scored again in the " + str(row['time']) + ' minute to give ' + row['event_team'] + ' the lead.\n')

				else:
					if(num_goal == 0):
						goal_line.append(str(row['time']) + ': ' + player + " scored in the " + str(row['time']) + ' minute for ' + row['event_team'] + ' to continue the fight-back.\n')
					elif(num_goal == 2):
						goal_line.append(str(row['time']) + ': ' + player + " completed his hattrick in the " + str(row['time']) + ' to continue the fight-back for ' + row['event_team'] +'.\n')
					else:
						goal_line.append(str(row['time']) + ': ' + player + " scored again in the " + str(row['time']) + ' to continue the fight-back for ' + row['event_team'] +'.\n')

			if(desc_goal != ""):
				goal_line.append(str(row['time']) + ': ' + desc_goal)
			if player in goal_scorer:
				goal_scorer[player] += 1
			else:
				goal_scorer[player] = 1

		elif row['location'] == 14:
			player = row['player']
			if player != None: player = player.title()
			else: player = ''
			goal_line.append(str(row['time']) + ': ' + "Disappointingly , " + player + " missed the penalty.\n")
	# print(goal_scorer)
	return goal_line
 
def foul_details(match_info, match_commentary):
	# When to print, at the end/start of events
	foul_string = []
	yellow_cards = []
	home_team = match_info['ht']
	away_team = match_info['at']
	red_cards_home = 0
	red_cards_away = 0
	for event in match_commentary:
		# print event
		event_type = event['event_type']
		player = event['player']
		if player != None: player = player.title()
		else: player = ''
		player2 = event['player2']
		if player2 != None: player2 = player2.title()
		else: player2 = ''
		team = event['event_team']
		num = 11
		if(event_type == 5 or event_type == 6):
			if(team == home_team):
				red_cards_home += 1
				num -= red_cards_home 
			if(team == away_team):
				red_cards_away += 1
				num -= red_cards_away

		if event_type == 4:
			# continue
			# foul_string.append(str(event['time']) + ':' + player + " was given a yellow card\n")
			yellow_cards.append((event['time'], player, event['event_team']))
		elif event_type == 5:
			foul_string.append(str(event['time']) + ': ' + player + " was given a second yellow card and was a big blow to " + team + ".\n")
		elif event_type == 6:
			foul_string.append(str(event['time']) + ': ' + player + " was given a red card and left " + team + " with a " +  str(num) + " man side in the "+ str(event['time']) + " minute of the match.\n")
		elif event_type == 11:
			if(re.match('Penalty conceded', event['text']) != None):
				tokens = event['text'].split()
				tokens.insert(1, 'was')
				string =  " In the " + str(event['time']) + " minute, " + " ".join(tokens) + "\n"
				foul_string.append(str(event['time']) + ': ' + string)
			else:
				tokens = event['text'].split()
				tokens = tokens[-8:]
				tokens[1] = 'drew'
				tokens[7] = 'area'
				string =  " In the " + str(event['time']) + " minute, " + " ".join(tokens) + " to win a penalty for "+ event['event_team'] +" .\n"	
				foul_string.append(str(event['time']) + ': ' + string)

	period_gap = 15
	period_start = 0
	players_hm = []
	players_aw = []
	# print yellow_cards
	for i in range(len(yellow_cards) + 1):

		if (i<len(yellow_cards)):
			event = yellow_cards[i]
		
		if(i == len(yellow_cards) or int(event[0]) > (period_start + period_gap)):
			
			if(i != len(yellow_cards)):
				while (int(event[0]) > (period_start + 2*period_gap)):
					period_start += period_gap
		
			string = ""
		
			if(len(players_hm) > 0):
				for i in range(len(players_hm)-1):
					string += players_hm[i] +", "
				string += players_hm[len(players_hm)-1] + " ("+ home_team +") "
				if(len(players_aw) > 0):
					string += ", "
			if(len(players_aw) > 0):
				for i in range(len(players_aw)-1):
					string += players_aw[i] +", "
				string += players_aw[len(players_aw)-1] + " ("+ away_team +") "
			if(len(players_hm) + len(players_aw) == 1):
				string += " was awarded a yellow card"
			if(len(players_hm) + len(players_aw) > 1):
						string += " were awarded yellow cards in a quick succesion around the "+ str(period_start + period_gap) +" minute"
			# if(len(players_hm) + len(players_aw) > 0):
			# 	foul_string.append(str(period_start + period_gap) + ': ' + string + ".\n")
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
	
	for event in match_commentary:

		event_type = event['event_type']
		player_in = event['player_in']
		if player_in != None: player_in = player_in.title()
		else: player_in = ''
		player_out = event['player_out']
		if player_out != None: player_out = player_out.title()
		else: player_out = ''
	
		if event_type == 7:
			# print (event['time'], player_in, player_out, event['event_team'])
			subsi.append((event['time'], player_in, player_out, event['event_team']))
	
	period_gap = 15
	period_start = 0

	players_hm_in = []
	players_aw_in = []
	players_hm_out = []
	players_aw_out = []
	early_stage = 0
	for i in range(len(subsi)+1):

		if(i < len(subsi)):
			event = subsi[i]
			
		if(i == len(subsi) or ((int(event[0]) > (period_start + period_gap)))):
			
			if(i != len(subsi)):
				while (int(event[0]) > (period_start + 2*period_gap)):
					period_start += period_gap
			
			string = ""

			if(len(players_hm_in) > 0):
				
				for i in range(len(players_hm_in)-1):
					string += players_hm_in[i] +", "
				if(len(players_hm_in) > 1):	
					string += players_hm_in[len(players_hm_in)-1] + " were substituted in for "
				else:
					string += players_hm_in[len(players_hm_in)-1] + " was substituted in for "

				for i in range(len(players_hm_out)-1):
					string += players_hm_out[i] +", "
				string += players_hm_out[len(players_hm_out)-1] + " ("+ home_team +") "

				if(len(players_aw_in) > 0):
					string += " while "

			if(len(players_aw_in) > 0):

				for i in range(len(players_aw_in)-1):
					string += players_aw_in[i] +", "
				string += players_aw_in[len(players_aw_in)-1] + " came on for "

				for i in range(len(players_aw_out)-1):
					string += players_aw_out[i] +", "
				string += players_aw_out[len(players_aw_out)-1] + " ("+ away_team +") "
			

			if(len(players_hm_in) + len(players_aw_in) > 0):
				if(period_start < 30 and early_stage ==0):
					early_stage += 1
					string += " in the early stages of the match"
				elif(period_start < 30):
					# string += "" in the "+ str(event[0]) +" minute of the match."	
					string += ""
				if(period_start + period_gap > 75 ):	
					string += " in the last few minutes of the match"

				subs.append(str(period_start + period_gap) + ': ' + string + ".\n")

			players_hm_in = []
			players_aw_in = []
			players_hm_out = []
			players_aw_out = []
			period_start += period_gap

		if(i == len(subsi)):
			break

		if(event[3] == home_team):
			players_hm_in.append(event[1])
			players_hm_out.append(event[2])
		else:
			players_aw_in.append(event[1])
			players_aw_out.append(event[2])
	# print subs
	return subs

def sort_time(timeline):
	timeline = [(int(x.split(':')[0]), x.split(':')[1]) for x in timeline]
	timeline.sort(key=lambda x: x[0])
	return timeline

def summarize(timeline):
	text = ""
	for row in timeline:
		text = text + row[1].rstrip('\n') 
		# text = text + str(row[0]) + " => " + row[1]
		# text = text + row[1]
	return text