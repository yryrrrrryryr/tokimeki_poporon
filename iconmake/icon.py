import cv2
import numpy as np
import math

s_list = [round(i * 0.01, 2) for i in range(0,101)]

for s in s_list:
    print(s)
    fname_r = "./input/fig1.png"
    fname_w = "./output/icon_" + str(int(100*s+0.01)) + ".png"

    img = cv2.imread(fname_r, -1)

    img_width  = img.shape[1]
    img_height = img.shape[0]

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for x in range(img_height):
        for y in range(img_width):
            b,g,r,a = img[x,y]
            v = img_gray[x,y]
            ss = min(1.,s/0.3)
            b = b*ss + v*(1-ss)
            g = g*ss + v*(1-ss)
            r = r*ss + v*(1-ss)
            
            xx = (x - (img_height-1.)/2.)
            yy = (y - (img_width -1.)/2.)
            r1 = (img_height)/2.
            r2 = 30.
            
            d  = (xx**2.+yy**2.)**0.5 - r1 + r2
            aa = max(0.,(r2-d)/r2)**0.25
            a  = min(255.,max(0.,255.*aa))
            
            if((((r2-d)/r2)>=0.) and (((r2-d)/r2)<=1.)):
                deg = ((math.degrees(math.atan2(xx, yy))+90.)%360.)
                
                if((deg <= 360*s)):
                    if(s<=0.25):
                        b,g,r = [0,255*(4*s),255]
                    elif(s<=0.50):
                        b,g,r = [0,255,255*(4*(0.5-s))]
                    elif(s<=0.75):
                        b,g,r = [255*max(0,(4*(s-0.5))),255,0]
                    else:
                        b,g,r = [255,255*max(0,(4*(1.0-s))),0]
                else:
                    gray = 128.
                    b = (gray+b)/2.
                    g = (gray+g)/2.
                    r = (gray+r)/2.
            img[x,y] = b,g,r,a

    cv2.imwrite(fname_w,img)
