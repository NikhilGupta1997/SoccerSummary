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

# print match_info
match_info, match_commentary = final_summary_help.get_match_info(team1, team2, season)

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
