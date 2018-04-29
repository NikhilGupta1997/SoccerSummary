#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect
import re
import final_summary_help

# Connect to the PostGres Server
cur = connect.connect()

# Get match number to summarize
team1 = (sys.argv[1])
team2 = (sys.argv[2])
season = (sys.argv[3])

def to_str(string):
	return '\'' + string + '\''

def get_match_info(team1, team2, season):
	# global connect
	match_info = connect.query_one(cur, 'SELECT * FROM game_info WHERE ht = ' + to_str(team1) + ' AND at = ' + to_str(team2) + ' AND season = ' + season)
	match_commentary = connect.query_mul(cur, ('SELECT * FROM events WHERE id_odsp = ' + to_str(match_info['id_odsp']) + ' ORDER BY sort_order ' ))
	return match_info, match_commentary	
# print match_info
match_info, match_commentary = get_match_info(team1, team2, season)

final_summary_help.stats(match_commentary, match_info)
timeline = []
timeline += final_summary_help.match_details(match_info)
# print winner(match_info)
timeline += final_summary_help.start_line(match_info, match_commentary)
timeline += final_summary_help.find_dominance(match_info, match_commentary)
timeline += final_summary_help.goal_scorer(match_commentary)
timeline += final_summary_help.foul_details(match_info, match_commentary)
timeline += final_summary_help.subsitutions(match_info, match_commentary)
timeline = final_summary_help.sort_time(timeline)
print(final_summary_help.summarize(timeline))
print("Summarization Over")
