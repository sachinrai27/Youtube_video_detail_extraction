#******importing required modules******
import redis
import argparse
import requests
from bs4 import BeautifulSoup 

#******using argparse to document input field requirement******
parser=argparse.ArgumentParser(description='URL to get details of the page')
parser.add_argument('-p','--page_url',metavar='',required=True, help='Valid URL of youtube page to get details')
args=parser.parse_args()

url=args.page_url


#******adding filter so that url entered is of youtube.com******
if 'youtube.com' in url:

    #******making request instance******
    try:
        response=requests.get(url)
        status=response.status_code
        
        #******condition to check if the webpage is valid by adding success code of 200******
        if status==200:
            #******using beautifulsoup module to add a filter in which if homepage url is given, it can ask for correct url******
            soup= BeautifulSoup(response.text,'html.parser')
            title= soup.find('title')
    
            #******adding apt response if incorrect url is given******
            if title.get_text() == 'YouTube':
                print('Please provide complete URL to get required details')
            else:
                #******pushing the verified url in redis list for furthur processing******
                red=redis.Redis(host='127.0.0.1',port=6379)
                red.set("url_detail",url)
        else:
            print('Please enter a valid URL')
    
    except Exception as err:
        print('Enter a valid URL')

else:
    print('Please enter an appropriate youtube URL')

    
