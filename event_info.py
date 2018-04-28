#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect
import json

# Connect to the PostGres Server
cur = connect.connect()

def to_str(string):
	return '\'' + string + '\''

def get_events(game_id):
	team_names = connect.query_mul(cur, 'SELECT * FROM events WHERE id_odsp = ' + to_str(game_id) + ' ORDER BY sort_order')
	return team_names	

game_id = sys.argv[1]
print(json.dumps(get_events(game_id)))