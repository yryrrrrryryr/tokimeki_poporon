# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session

# URL:
url_update = 'https://api.twitter.com/1.1/statuses/update.json'
url_follow = 'https://api.twitter.com/1.1/followers/list.json'
url_icon   = 'https://api.twitter.com/1.1/account/update_profile_image.json'
url_search_std = 'https://api.twitter.com/1.1/search/tweets.json'

# common variables:
id_list = []
tweet_list = []

userID = 'your_twitter_ID'
CK = 'XXXXXXXXXXXXXXXXXXXXXXXXX'        
CS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AT = 'XXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AS = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

twitter = OAuth1Session(CK,CS,AT,AS)