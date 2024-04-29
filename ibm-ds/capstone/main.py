import requests 
import pandas as pd

for i in pd.DataFrame():
    print(i)

import folium

fig = folium.Figure()

if __name__ == '__main__':
    url = 'https://api.spacexdata.com/v4/launches/past'
    res = requests.get(url)

    df = pd.json_normalize(res.json())
    print(df.shape)