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

def get_team_names(home_team, away_team, season):
	team_names = connect.query_one(cur, 'SELECT * FROM game_info WHERE ht = ' + to_str(home_team) + ' AND at = ' + to_str(away_team) + ' AND season = ' + season)
	date_str = team_names['date'].strftime("%B %d, %Y")
	team_names['date'] = date_str
	return team_names	

home_team = sys.argv[1]
away_team = sys.argv[2]
season = sys.argv[3]
print(json.dumps(get_team_names(home_team, away_team, season)))