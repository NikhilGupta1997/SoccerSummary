#################################################
#   Create a summary for a football match   	#
# 	Copyright : Nikhil Gupta & Ayush Bhardwaj	#
#################################################

import csv
import sys
import connect
import subprocess
import sys
import os

# Connect to the PostGres Server
cur = connect.connect()

team1 = (sys.argv[1])
team2 = (sys.argv[2])
season = (sys.argv[3])

match_query = connect.query_one(cur, 'SELECT id_odsp FROM game_info WHERE ht = ' + to_str(team1) + ' AND at = ' + to_str(team2) + ' AND season = ' + season)
match_id = match_query['id_odsp']

def get_match_ids():
	match_ids = connect.query_mul(cur, 'SELECT DISTINCT id_odsp FROM game_info')
	return match_ids

match_ids = get_match_ids()

idx = 0
for i, mid in enumerate(match_ids):
	if match_id == mid['id_odsp']:
		idx = i
		break

with open('url_lists/all_test.txt', 'w') as f:
	f.write(str(idx))

os.system("python read_files.py")

os.system("scp -r Task5_finished/chunked/test_000.bin shivank@40.74.227.89:~/code-pointer-generator/Task5_finished/chunked")
os.system("scp -r Task5_finished/test.bin shivank@40.74.227.89:~/code-pointer-generator/Task5_finished")

# HOST="shivank@40.74.227.89"
# # Ports are handled in ~/.ssh/config since we use OpenSSH
# COMMAND="python run_summarization.py --mode=decode --single_pass --task_id 5 --exp_name try3"

# ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
#                        shell=False,
#                        stdout=subprocess.PIPE,
#                        stderr=subprocess.PIPE)
# result = ssh.stdout.readlines()
# print result


