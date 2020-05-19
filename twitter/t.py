from tweet_post import *
from consts import *
import os

twitter = initialize(CK,CS,AT,AS)
offset  = fetch_offset()

while True:
	print("Input:", end="")
	tweet = input()
	if(tweet == 'cls'):
		try:
			os.system('cls')
			id_list = []
			tweet_list = []
		except:
			pass
	elif(tweet[0:6] == 'delete'):
		id_list,tweet_list = tweet_destroy(id_list,tweet_list,tweet,twitter)
	elif(tweet[0:4] == 'edit'):
		id_list,tweet_list = tweet_edit(id_list,tweet_list,tweet,twitter)
	elif(tweet[0:4] == 'icon'):
		tweet_icon(tweet,twitter)
	elif(tweet[0:6] == 'offset'):
		offset = fetch_offset()
	elif(tweet[0:5] == 'check'):
		time_check(tweet,twitter)
	elif((tweet.isdigit()) and (len(tweet) == 19)):
		print(id_to_unix(int(tweet)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
	else:
		id_list,tweet_list = tweet_post(id_list,tweet_list,tweet,offset,twitter)