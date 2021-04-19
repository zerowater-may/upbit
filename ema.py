from indicator import *





if __name__ =='__main__':

    info = {
        'telegram_token':'1654565187:AAHwmMgsj67GvomoQK3CUb8u-J1OtogzEzA',
        'telegram_chatid':'-469515114',
        'candle':'minutes/1',
        'symbol':'KRW-CRE',
    }
    

    IC = Indicators()
    buy,sell = False,False

    import pandas as pd
import datetime
import requests
import pandas as pd
import time
import webbrowser
import numpy as np

a = 1

while True:
    url = "https://api.upbit.com/v1/candles/minutes/5"
    
    querystring = {"market":"KRW-DOGE","count":"120"}
    
    response = requests.request("GET", url, params=querystring)
    
    data = response.json()
    
    df = pd.DataFrame(data)
    
    df=df['trade_price'].iloc[::-1]
   
    

    ma5 = df.rolling(window=5).mean()
    ma10 = df.rolling(window=10).mean()
    ma20 = df.rolling(window=20).mean()
    ma60 = df.rolling(window=60).mean()
    ma120 = df.rolling(window=120).mean()
        

    print(round(ma5.iloc[-1],2))
    print(round(ma10.iloc[-1],2))
    print(round(ma20.iloc[-1],2))
    print(round(ma60.iloc[-1],2))
    print(round(ma120.iloc[-1],2))

    print('')
    time.sleep(1)