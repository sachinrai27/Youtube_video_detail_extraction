#******importing required modules******
import requests
from bs4 import BeautifulSoup as bs
import re
import redis
import logging

#*****connecting to redis******
conn=redis.Redis(host='127.0.0.1', port=6379)

#*****initializing url to empty string to wait for detail extraction till a valid url pops up in list******
url=''

#******providing condition for the script to wait till a valid url pops up in list(url_detail)******
while(len(url)==0):
    #******getting url from redis list******
    url=list(str(conn.get("url_detail")))

    #******refinng the url for furthur processing******
    url.pop(0)
    url.pop(0)
    url.pop(-1)
    url=''.join(url)
    continue

#******parsing the obtained url******
r=requests.get(url)

#******initializing a dictionary to store details******
video_details={}

#******calling beautifulsoup instance to parse the url******
soup=bs(r.content,features="html.parser")

#******extracting video title from webpage******
title=(soup.find('meta', property="og:title")).attrs['content']
video_details["video_title"]=str(title)

#******extracting tags******
tags=soup.find_all('meta', property="og:video:tag")
if len(str(tags))==2:
    video_details["hashtag"]="No tags present"
else:
    #******looping over tags to get individual content of******
    
    video_details["hashtag"]=','.join([meta.attrs.get("content") for meta in soup.find_all("meta",{"property":"og:video:tag"})])

#******extracting number of views******
view = soup.find("meta", itemprop="interactionCount").attrs['content']
video_details["views"]=int(view)

#******extracting upload date******
date=soup.find("meta", itemprop='uploadDate').attrs['content']
video_details["upload_date"]=str(date)

#*****extracting channel title******
channel_title=soup.find("link", itemprop='name').attrs['content']
video_details["uploader_title"]=str(channel_title)

#******using regular expression to extract number of subscribers******
regex=re.compile(r'subscriberCountText.*subscribers')
subs=(regex.search(str(soup))).group()
video_details["subscribers"]=subs[subs.rindex('"')+1:].strip()

#*******using regular expression to extract entire description******
regex1=re.compile(r'shortDescription.*isCrawlable')
desc=(regex1.search(str(soup))).group()
desc=desc[desc.find('"',(desc.find('"'))+1)+1:desc.rindex('i')-3]
if len(desc)==0:
    video_details["description"]="No description available"
else:
    descr=(desc.replace('\\n', ' ')).replace('\\u0026','&')
    video_details["description"]=descr

#******extracting duration of video******
time=str(soup.find('meta', itemprop='duration').attrs['content'])
minutes=time[time.find('T')+1:time.find('M')]
seconds=time[time.find('M')+1:time.find('S')]
if int(minutes)==0: 
    video_details["duration"]=seconds+' seconds'
else:
    total_time=minutes+' minutes '+seconds+' seconds'
    video_details["duration"]=total_time


#*****pushing data from video_details dict to redis list named vide_meta for furthur processing******
video_meta="video_meta_details"
for k,v in video_details.items():
    conn.hset(video_meta,k,v)




