# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import json
import time
import datetime
import pandas as pd
import numpy as np
import codecs
import requests
import unicodedata
import os
import base64
import io

# URL:
url_update = 'https://api.twitter.com/1.1/statuses/update.json'
url_follow = 'https://api.twitter.com/1.1/followers/list.json'
url_icon   = 'https://api.twitter.com/1.1/account/update_profile_image.json'

def initialize(hello,CK,CS,AT,AS):
	os.system('cls')
	if(len(hello) >= 1):
		print(hello,'\n')
	twitter = OAuth1Session(CK,CS,AT,AS)
	return twitter

def trim_text(text):
	trimmed_text = text
	cnt = 0.
	l_lim = -1
	for c,l in zip(text,range(len(text))):
		if(unicodedata.east_asian_width(c) in 'AFW'):
			delta = 1.
		else:
			delta = 0.5
		if((cnt <= 140) and (cnt+delta > 140)):
			trimmed_text = text[0:l]
		cnt += delta
	return trimmed_text,cnt

def tweet_icon(gauge,twitter):
	icon_name = './icon/icon_' + str(gauge) + '.png'

	with open(icon_name, 'rb') as icon:
		enc_icon = base64.encodestring(icon.read())
	
	params = {'image': enc_icon,'include_entities': 'false','skip_status': 'true'}
	req = twitter.post(url_icon, data = params)
	
	if req.status_code == 200:
		print('OK')
	else:
		print('Error:',req)
	time.sleep(0.5)

def tweet_post(id_list,tweet_list,text,twitter):
	tweet,cnt = trim_text(text)
	params = {'status': tweet}
	post_time = datetime.datetime.fromtimestamp(time.time())
	req = twitter.post(url_update, params = params)
	if req.status_code == 200: 
		id = req.json()['id']
		id_str = req.json()['id_str']
		syaro = (datetime.datetime(1970, 1, 1, 9) + datetime.timedelta(milliseconds = int(id / 2**22) + 1288834974657))
		syarodate = datetime.datetime(syaro.year,syaro.month,syaro.day,0,0,0)
		syarodelta = syaro - post_time
		syarotime = syaro.strftime('%H:%M:%S.%f')[:-3]
		print('{0} / {1}'.format(syarotime,cnt))
		id_list.insert(0,id_str)
		l = min(len(tweet),999)
		tweet_list.insert(0,tweet[0:l])
	print('')
	time.sleep(0.5)
	return id_list,tweet_list

def tweet_destroy(id_list,tweet_list,tweet,twitter):
	if(len(id_list) == 0):
		print("Error: No tweets to delete\n")
	else:
		if(len(tweet) == 6):
			print()
			df = pd.DataFrame({'Tweet':tweet_list})
			print(df,'\n\nSelect the number of tweet:')
			try:
				id_num = int(input())
			except:
				id_num = -1
		else:
			try:
				id_num = int(tweet[6:])
			except:
				id_num = -1
		
		if((id_num < 0) or (id_num >= len(id_list))):
			print("Error: Invalid specification of number\n")
			return id_list,tweet_list
		
		id_str = id_list[id_num]
		url_destroy = "https://api.twitter.com/1.1/statuses/destroy/{0}.json".format(id_str)
		req = twitter.post(url_destroy)
		if req.status_code == 200: 
			print("Success: Deleting\n")
			id_list.pop(id_num)
			tweet_list.pop(id_num)
		else:
			print("Failed: Deleting\n")
		time.sleep(0.5)
	return id_list,tweet_list

def tweet_edit(id_list,tweet_list,tweet,twitter):
	if(len(id_list) == 0):
		print("Error: No tweets to modify\n")
	else:
		# 修正するツイートの番号が指定されていない場合
		if(len(tweet) == 4):
			print()
			df = pd.DataFrame({'Tweet':tweet_list})
			print(df,'\n\nSelect the number of the tweet:')
			try:
				id_num = int(input())
			except:
				id_num = -1
		
		# 修正するツイートの番号が指定されている場合
		else:
			try:
				id_num = int(tweet[4:])
			except:
				id_num = -1
		
		if((id_num < 0) or (id_num >= len(id_list))):
			print("Error: Invalid specification of number\n")
			return id_list,tweet_list
		id_str = id_list[id_num]
		
		# ツイート修正内容の入力
		tweet_before = tweet_list[id_num]
		print("\nYou're modifing the following tweet:\n",tweet_before)
		print("\nExpression before editing:")
		str_before = input()
		print("\nExpression after editing:")
		str_after = input()
		
		tweet_before_mirror = tweet_before[::-1]
		str_before_mirror = str_before[::-1]
		str_after_mirror = str_after[::-1]
		tweet_after_mirror = tweet_before_mirror.replace(str_before_mirror, str_after_mirror, 1)
		tweet_after = tweet_after_mirror[::-1]
		
		if(tweet_before == tweet_after):
			print('Error: No match found')
			return id_list,tweet_list
		
		# ツイートを削除した後再投稿
		url_destroy = "https://api.twitter.com/1.1/statuses/destroy/{0}.json".format(id_str)
		req = twitter.post(url_destroy)
		if req.status_code == 200:
			id_list.pop(id_num)
			tweet_list.pop(id_num)
			time.sleep(0.5)
			id_list,tweet_list = tweet_post(id_list,tweet_list,tweet_after,twitter)
		else:
			print("Failed: Delete\n")
	return id_list,tweet_list

