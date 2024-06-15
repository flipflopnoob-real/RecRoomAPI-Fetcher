#Pulls a random thumbnail from rated.csv and displays it

import pandas as pd
import random
import requests
from PIL import Image
from io import BytesIO
df = pd.read_csv('rated.csv', low_memory = False)
randNum = random.randint(0, len(df))
print(df.iloc[randNum])
response = requests.get("https://img.rec.net/" + str(df.iloc[randNum]['image']))
img = Image.open(BytesIO(response.content))
img.show()
