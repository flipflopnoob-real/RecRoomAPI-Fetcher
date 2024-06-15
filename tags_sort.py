#Fetches all* rooms and grabs custom tags which are stored in tags.csv

#*to reduce time to run this script, rooms that have the attributes of template rooms are ignored.

import pandas as pd
import requests
import time
df = pd.read_csv('descriptionSort.csv', low_memory = False)
urlBase = 'https://rooms.rec.net/rooms?name={name}&include=297'
tagsList = []
for i in range(0, len(df)):
    try:
        tags = ''
        roomName = str(df['name'].iloc[i])
        url = urlBase.format(name = roomName)
        r = requests.get(url).json()
        for tag in r['Tags']:
            tags += str(tag['Tag']) + ";"
        tagsList.append(tags)
        print(roomName, i)
    except:
        print("whoopsies")
df.insert(9, "tags", tagsList, True)
df.to_csv('tags.csv', mode = 'w', index = False)
