#******importing all required modules******
import csv
import redis
import os

#*****connecting to redis******
r=redis.Redis(host='127.0.0.1',port=6379)
video_meta="video_meta_details"

#******reading video details from redis list and converting it to dictionary******
g=dict(r.hgetall(video_meta))
save_details={}

#******transferring the video details to new dictionary 'save_details' ato push the data to csv******
for k,v in g.items():
    k=list(str(k))
    k.pop(0)
    k.pop(0)
    k.pop(-1)
    k=''.join(k)
    v=list(str(v))
    v.pop(0)
    v.pop(0)
    v.pop(-1)
    v=''.join(v)
    save_details[k]=v

#******getting the path to save csv named 'video_meta_details'******
file_path=os.getcwd()

#******applying check, if csv already exists append the data else create the csv and push data******
if os.path.exists(file_path+'\\video_meta_details'):
    with open(file_path+'\\video_meta_details.csv','a') as f:
        for key in save_details.keys():
            f.write("%s,%s\n"%(key,save_details[key]))
    f.close()
else:
    with open(file_path+'\\video_meta_details.csv','w') as f:
        for key in save_details.keys():
            f.write("%s,%s\n"%(key,save_details[key]))
    
    f.close()





