import winsound as ws
import datetime
import time
import ntplib
import numpy as np
import msvcrt as ms

def fetch_offset(req_iter):
	offset_list = []
	c = ntplib.NTPClient()
	for i in range(req_iter):
		res = c.request('ntp.nict.jp', version=3)
		offset_list.append(res.offset*1000)
		if(i+1 < req_iter):
			time.sleep(1)
	return round(np.mean(offset_list))

flag = 1
tweet_lag = 100

if(flag == 1):
    tweak = fetch_offset(1) + tweet_lag
else:
    tweak = tweet_lag
print('Tweak: {0} ms'.format(int(tweak)))
patience = 20

msec_list = [0,250,500,750]
freq_list = [1000,500,500,500]

while(True):
    t_now = datetime.datetime.now()
    msec_now = (t_now.microsecond/1000 + tweak) % 1000
    for msec,freq in zip(msec_list,freq_list):
        if((msec_now >= msec) and (msec_now <= msec + patience)):
            ws.Beep(freq,100)
            time.sleep(0.05)
            if(ms.kbhit()):
                note = ms.getwch()
                if(note == 's'):
                    tweak -= 20
                    print('slow (20 ms)')
                elif(note == 'd'):
                    tweak -= 5
                    print('slow ( 5 ms)')
                elif(note == 'f'):
                    tweak -= 1
                    print('slow ( 1 ms)')
                elif(note == 'j'):
                    tweak += 1
                    print('fast ( 1 ms)')
                elif(note == 'k'):
                    tweak += 5
                    print('fast ( 5 ms)')
                elif(note == 'l'):
                    tweak += 20
                    print('fast (20 ms)')