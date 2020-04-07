from tweet_post import *
from consts import *
import os

mode = 0
twitter = initialize(hello0,CK0,CS0,AT0,AS0)

while True:
	tweet = input()
	if(tweet == 'cls'):
		os.system('cls')
		id_list = []
		tweet_list = []
	elif(tweet[0:6] == 'delete'):
		id_list,tweet_list = tweet_destroy(id_list,tweet_list,tweet,twitter)
	elif(tweet[0:4] == 'edit'):
		id_list,tweet_list = tweet_edit(id_list,tweet_list,tweet,twitter)
	elif(tweet[0:4] == 'icon'):
		gauge = tweet[5:]
		tweet_icon(gauge,twitter)
	else:
		id_list,tweet_list = tweet_post(id_list,tweet_list,tweet,twitter)