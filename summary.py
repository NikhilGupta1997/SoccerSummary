#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect
import summary_help

# Connect to the PostGres Server
cur = connect.connect()

# Get match number to summarize
team1 = (sys.argv[1])
team2 = (sys.argv[2])
season = (sys.argv[3])

def to_str(string):
	return '\'' + string + '\''

def get_match_info(team1, team2, season):
	match_info = connect.query_one(cur, 'SELECT * FROM game_info WHERE ht = ' + to_str(team1) + ' AND at = ' + to_str(team2) + ' AND season = ' + season)
	match_commentary = connect.query_mul(cur, 'SELECT * FROM events WHERE id_odsp = ' + to_str(match_info['id_odsp']))
	return match_info, match_commentary	

# print match_info
match_info, match_commentary = get_match_info(team1, team2, season)
timeline = []
timeline += summary_help.match_details(match_info)
# print winner(match_info)
timeline += summary_help.start_line(match_info, match_commentary)
timeline += summary_help.find_dominance(match_info, match_commentary)
timeline += summary_help.goal_scorer(match_commentary)
timeline += summary_help.foul_details(match_commentary)
timeline += summary_help.subsitutions(match_commentary)
timeline = summary_help.sort_time(timeline)
print(summary_help.summarize(timeline))
