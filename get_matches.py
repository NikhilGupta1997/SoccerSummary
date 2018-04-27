#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect

# Connect to the PostGres Server
cur = connect.connect()
team1 = sys.argv[1]
team2 = sys.argv[2]

def to_str(string):
	return '\'' + string + '\''

def get_matches():
	team_names = connect.query_mul(cur, 'SELECT season FROM game_info WHERE ht = ' + to_str(team1) + ' AND at = ' + to_str(team2) + ' ORDER BY season')
	name_string = ''
	for i, name in enumerate(team_names):
		if i-1 < len(team_names):
			name_string += str(name['season']) + '\n'
		else:
			name_string += str(name['season'])
	return name_string	

print(get_matches())