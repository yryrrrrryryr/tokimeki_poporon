# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
from consts import *
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
import ntplib

def id_to_unix(x):
	return datetime.datetime(1970, 1, 1, 9) + datetime.timedelta(milliseconds = int(x / 2**22) + 1288834974657)

def unix_to_id(x):
	return (int(x.timestamp() * 1000 - 1288834974657) << 22)

def since_id(hour,minute):
	time = datetime.datetime.now().replace(hour=hour,minute=minute,second=0,microsecond=0)
	return unix_to_id(time)

def delta_ms(x):
	ans = ((x.days * 86400 + x.seconds) * 1000 + (x.microseconds / 1000))
	return ans

def initialize(CK,CS,AT,AS):
	try:
		os.system('cls')
	except:
		pass
	twitter = OAuth1Session(CK,CS,AT,AS)
	return twitter

def time_check(tweet,twitter):
	keyword = ''
	cnt = 1
	if(len(tweet) > 5):
		try:
			opt = tweet[5:].split()
			if(len(opt) > 1):
				keyword = str(opt[0]) + ' '
				cnt = int(opt[1])
			else:
				if(opt[0].isdecimal()):
					if(int(opt[0]) > 100): #101以上の数字はキーワードとみなす
						keyword = str(opt[0]) + ' '
					else: #100以下の数字は取得したいツイート数とみなす
						cnt = int(opt[0])
		except:
			pass
	q_str = "{0}from:{1}".format(keyword,userID)
	params = {'q': q_str, 'count': cnt}
	req = twitter.get(url_search_std, params=params)
	if req.status_code == 200:
		json_data = json.loads(req.text)
		result = json_data['statuses']
		if(len(result) == 0):
			print('No tweets found...')

	for t,r in zip(range(cnt),result):
		time = (datetime.datetime(1970, 1, 1, 9) + datetime.timedelta(milliseconds = int(r['id'] / 2**22) + 1288834974657)) 
		time_str = time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
		print('{0}: {1} {2}'.format(str(t).rjust(3),time_str,trim_text(r['text'],10)[0]))
	print('')
	
def fetch_offset(req_iter=1):
	offset_list = []
	c = ntplib.NTPClient()
	for i in range(req_iter):
		res = c.request('ntp.nict.jp', version=3)
		offset_list.append(res.offset*1000)
		if(i+1 < req_iter):
			time.sleep(1)
	print('offset:',round(np.mean(offset_list)),'ms','\n')
	return round(np.mean(offset_list))
	
def trim_text(text,length):
	text = ' '.join(text.splitlines())
	trimmed_text = text
	cnt = 0.
	l_lim = -1
	for c,l in zip(text,range(len(text))):
		if(unicodedata.east_asian_width(c) in 'AFW'):
			delta = 1.
		else:
			delta = 0.5
		if((cnt <= length) and (cnt+delta > length)):
			trimmed_text = text[0:l]
		cnt += delta
	return trimmed_text,cnt

def tweet_icon(tweet,twitter):
	gauge = str(tweet[5:])
	icon_name = './icon/{0}.png'.format(gauge)
	
	if(os.path.exists(icon_name)):
		with open(icon_name, 'rb') as icon:
			enc_icon = base64.encodestring(icon.read())
		
		params = {'image': enc_icon,'include_entities': 'false','skip_status': 'true'}
		req = twitter.post(url_icon, data = params)
		
		if req.status_code == 200:
			print('Icon successfully changed to {0}.png'.format(str(gauge)))
		else:
			print('Error:',req)
		time.sleep(1)
	else:
		print('Icon file not found: {0}.png'.format(gauge))
	
def tweet_post(id_list,tweet_list,text,offset,twitter):
	tweet,cnt = trim_text(text,140)
	params = {'status': tweet}
	time_push = datetime.datetime.now() + datetime.timedelta(milliseconds = offset)
	req = twitter.post(url_update, params = params)
	if req.status_code == 200: 
		id = req.json()['id']
		id_str = req.json()['id_str']
		syaro = id_to_unix(id)
		syarodate = datetime.datetime(syaro.year,syaro.month,syaro.day,0,0,0)
		
		prn1 = time_push.strftime('%H:%M:%S.%f')[:-3]
		prn2 = syaro.strftime('%H:%M:%S.%f')[:-3]
		prn3 = int(delta_ms(syaro - time_push))
		print("{0} -> {1} ({2} ms)".format(prn1,prn2,prn3))		
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

