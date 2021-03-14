**Youtube video information extraction**

This utility helps in getting video details from any valid youtube link without use of any API.

**Setup:**
Libraries to install:
1. requests
2. BeautifulSoup
3. redis
4. argparse

Above can be installed using:

_pip3 install requests_

_pip3 install BeautifullSoup_

_pip3 install redis_

_pip3 install argparse_


**Running the utility:**
It consists of mainly three scripts:

1. request_queue.py :
The script takes input as the url to be scrapped. It verifies the input provided to be a valid youtube link.
After successfull verification the url is pushed to a redis list('url_detail').

How to run:
from CLI type:
```python request_queue.py -p <url>```

2. request_process.py:
This script takes the input from redis list('url_detail') and using it extracts below information from the link:
	* Video Title
	* HashTags used
	* View Count
	* Upload Date
	* Channel/Uploader Title
	* Channel/Uploader Subscribers
	* Description of Video
	* Duration/Length of Video

The above details are stored in a dictionary which is furthur pushed to a different redis list('video_meta').

3. request_save.py:
This script reads data from redis list('vide_meta') and furthur saves the data in a csv file.

**tput:**
The final output is stored in a csv file.





