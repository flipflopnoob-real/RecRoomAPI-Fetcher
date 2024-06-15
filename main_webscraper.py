## This gathers the data into a CSV, and then makes another copy in which no duplicates exist

import requests
import pandas as pd
import time
roomData = []
urlBase = "https://rooms.rec.net/rooms/search?query={search}&skip={skip}&take=1000"
charList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '_']
try:
    for a in range(30, 31):
        for b in range(30, 31):
            print(str(charList[a]) + str(charList[b]))
            if(a == 0 and b == 14):
                url = urlBase.format(search = str(charList[a]) + str(charList[b]), skip = "6")
            else:
                url = urlBase.format(search = str(charList[a]) + str(charList[b]), skip = "1")
            r = requests.get(url).json()
            toSearch = r["TotalResults"]
            if(toSearch > 100000):
                toSearch = 100000
            for j in range(1, toSearch, 1000):
                url = urlBase.format(search = str(charList[a]) + str(charList[b]), skip = str(j))
                r = requests.get(url).json()
                
                for i in range(0, 1000):
                    try:
                        roomId = r["Results"][i]["RoomId"]
                        name = r["Results"][i]["Name"]
                        description = r["Results"][i]["Description"]
                        dateTemp = r["Results"][i]["CreatedAt"]
                        #Date does not work, bother me about it and I will fix it
                        date = 0
                        date += (int(dateTemp[0:4]) - 1970) * 31556926
                        date += (int(dateTemp[5:7]) - 1) * 2629743
                        date += (int(dateTemp[8:10]) - 1) * 86400
                        date += (int(dateTemp[11:13])) * 3600
                        date += (int(dateTemp[14:16])) * 60
                        date += (int(dateTemp[17: 19]))
                        cheer = r["Results"][i]["Stats"]["CheerCount"]
                        favorite = r["Results"][i]["Stats"]["FavoriteCount"]
                        visitor = r["Results"][i]["Stats"]["VisitorCount"]
                        visits = r["Results"][i]["Stats"]["VisitCount"]
                        image = r["Results"][i]["ImageName"]
                        roomData.append([roomId, name, description, date, cheer, favorite, visitor, visits, image])
                    except:
                        break
                print(j)
                time.sleep(0.1)
                
            df = pd.DataFrame(roomData)
            df.columns = ["roomID", "name", "description", "date", "cheer", "favorite", "visitor", "visits", "image"]
            df.to_csv('roomNoTags.csv', mode = 'a', index = False)
            roomData = []
except Exception as e:
	print("ended")
	print(e)
df.columns = ["roomID", "name", "description", "date", "cheer", "favorite", "visitor", "visits", "image"]
df.to_csv('roomNoTags.csv', mode = 'a', index = False)
print("Lets Dance")
df = pd.read_csv('roomNoTags.csv', low_memory = False)
print(len(df))
print("Woah half way there")
df.drop_duplicates(subset=['name'], inplace = True)
print("made it!")
print(len(df))
df.to_csv('refined.csv', mode = 'w', index = False)

