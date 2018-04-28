#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect
import summary_help
import final_summary_help

# Connect to the PostGres Server
cur = connect.connect()

def to_str(string):
	return '\'' + string + '\''

def get_match_info(match_id):
	match_info = connect.query_one(cur, 'SELECT * FROM game_info WHERE id_odsp = ' + to_str(match_id))
	match_commentary = connect.query_mul(cur, 'SELECT * FROM events WHERE id_odsp = ' + to_str(match_info['id_odsp']))
	return match_info, match_commentary	

def get_match_ids():
	match_ids = connect.query_mul(cur, 'SELECT DISTINCT id_odsp FROM game_info')
	return match_ids

def run(match_info, match_commentary):
	timeline = []
	timeline += summary_help.match_details(match_info)
	timeline += summary_help.start_line(match_info, match_commentary)
	timeline += summary_help.find_dominance(match_info, match_commentary)
	timeline += summary_help.goal_scorer(match_commentary)
	timeline += summary_help.foul_details(match_commentary)
	timeline += summary_help.subsitutions(match_commentary)
	timeline = summary_help.sort_time(timeline)
	return summary_help.summarize(timeline)
	# print("Summarization Over")

def final_run(match_info, match_commentary):
	final_summary_help.stats(match_commentary, match_info)
	timeline = []
	timeline += final_summary_help.match_details(match_info)
	timeline += final_summary_help.start_line(match_info, match_commentary)
	timeline += final_summary_help.find_dominance(match_info, match_commentary)
	timeline += final_summary_help.goal_scorer(match_commentary)
	timeline += final_summary_help.foul_details(match_info, match_commentary)
	timeline += final_summary_help.subsitutions(match_info, match_commentary)
	timeline = final_summary_help.sort_time(timeline)
	return final_summary_help.summarize(timeline)

match_ids = get_match_ids()
for i, mid in enumerate(match_ids):
	print i, mid['id_odsp']
	if i < 100:
		continue
	match_info, match_commentary = get_match_info(mid['id_odsp'])
	if len(match_commentary) == 0:
		continue
	text = run(match_info, match_commentary)
	final_text = final_run(match_info, match_commentary)
	# text = text.decode('utf-8', 'ignore')
	# final_text = final_text.decode('utf-8', 'ignore')
	with open('summaries/' + str(i) + '.summ', 'w') as f:
		f.write(text)
		f.write('\n@highlight\n')
		f.write(final_text)
	if i % 10 == 8:
		file = 'all_val.txt'
	elif i % 10 == 9:
		file = 'all_test.txt'
	else:
		file = 'all_train.txt'
	with open('url_lists/' + file, 'a') as f:
		f.write(str(i) + '\n')
