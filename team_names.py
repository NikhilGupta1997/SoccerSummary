#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect

# Connect to the PostGres Server
cur = connect.connect()

def get_team_names():
	team_names = connect.query_mul(cur, 'SELECT DISTINCT ht, league FROM game_info ORDER BY league, ht')
	name_string = ''
	for i, name in enumerate(team_names):
		if i-1 < len(team_names):
			name_string += name['league'] + ':' + name['ht'] + '\n'
		else:
			name_string += name['league'] + ':' + name['ht']
	return name_string	

print(get_team_names())