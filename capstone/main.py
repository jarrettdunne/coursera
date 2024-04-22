import requests 
import pandas as pd


if __name__ == '__main__':
    url = 'https://api.spacexdata.com/v4/launches/past'
    res = requests.get(url)

    df = pd.json_normalize(res.json())
    print(df.shape)