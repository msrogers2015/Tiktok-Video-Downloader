import json
import requests
from datetime import datetime, timedelta

# Create a list for all the video links to be dumped into.
links = []
# The encoding has to be specified for the data file. Had some encoding issues when developing this.
with open('data.json', 'r', encoding="utf8") as file:
    data = json.load(file)
    # Your uploaded videos are in a Videos sub group in the Video section. This is closer to the bottom of your data file
    # if you are curious about what it looks like. 
    video_list = data['Video']['Videos']['VideoList']
    for video in video_list:
        links.append(video['Link'])
counter = 1
# For the nerds, i created a timer.
start = datetime.now()
# This will loop through all your videos. Beware, this will take some time. All videos will be dumped where this file is ran
# So make sure you have enough disk space. 
for i in links:
    print(f'Downloading Tiktok number {counter}')
    vid = requests.get(i)
    try:
        with open(f'tiktok_{counter}.mov', 'wb') as file:
            file.write(vid.content)
    # Probably useless, will refine later.
    except Exception as e:
        print(e)
    counter += 1

# Note for the nerds, tells you how long it took to download all your videos. 
end = datetime.now()
total_time = end-start
print(f'It took {total_time} to download {counter-1} of your tiktok videos.')
