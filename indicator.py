import requests
import pandas as pd
import time
import numpy as np
import telegram
import pyupbit
# from upbitpy import Upbitpy
from pprint import pprint
from upbitupbit import *
class Indicators:

    def rsiindex(self,info):
        stockrsi = {}
        
        self.symbol = info['symbol']
        self.candle = info['candle']

        url = f"https://api.upbit.com/v1/candles/{self.candle}"

        querystring = {"market":self.symbol,"count":"500"}
        while True:
            try:
                response = requests.request("GET", url, params=querystring)
                data = response.json()
                break
            except Exception:
                time.sleep(1)
                continue

        df = pd.DataFrame(data)
        stockrsi.update({'trend':self.ma(df)})
        df=df.reindex(index=df.index[::-1]).reset_index()

        df['close']=df["trade_price"]

        def rsi(ohlc: pd.DataFrame, period: int = 14):
            ohlc["close"] = ohlc["close"]
            delta = ohlc["close"].diff()

            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0

            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")

        rsi = rsi(df, 14).iloc[-1]
        # stockrsi = self.stockrsi(df)
        
        stockrsi.update({'rsi':rsi})
        stockrsi.update(self.macd())
        now = time.localtime()
        nowtime ="%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        stockrsi.update({'nowtime':nowtime})
        stockrsi.update({'price':pyupbit.get_current_price(self.symbol)})
        stockrsi.update({'symbol':self.symbol})
        stockrsi.update({'candle':self.candle})
        
        # print(stockrsi)
        # print(symbol)
        # print('upbit 10 minute RSI:', rsi)
        # print('')
        return stockrsi
        # time.sleep(1)

    def stockrsi(self,df):

        series=df['trade_price'].iloc[::-1]
        
        df = pd.Series(df['trade_price'].values)

        period=14
        smoothK=3
        smoothD=3
            
        delta = series.diff().dropna()
        ups = delta * 0
        downs = ups.copy()
        ups[delta > 0] = delta[delta > 0]
        downs[delta < 0] = -delta[delta < 0]
        ups[ups.index[period-1]] = np.mean( ups[:period] )
        ups = ups.drop(ups.index[:(period-1)])
        downs[downs.index[period-1]] = np.mean( downs[:period] )
        downs = downs.drop(downs.index[:(period-1)])
        rs = ups.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() / \
                downs.ewm(com=period-1,min_periods=0,adjust=False,ignore_na=False).mean() 
        rsi = 100 - 100 / (1 + rs)

        stochrsi  = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
        stochrsi_K = stochrsi.rolling(smoothK).mean()
        stochrsi_D = stochrsi_K.rolling(smoothD).mean()
        
        # print(symbol)    
        # print('upbit 10 minute stoch_rsi_K: ', stochrsi_K.iloc[-1]*100)
        # print('upbit 10 minute stoch_rsi_D: ', stochrsi_D.iloc[-1]*100)
        # print('')

        # time.sleep(1)
        k_rsi = stochrsi_K.iloc[-1]*100
        d_rsi = stochrsi_D.iloc[-1]*100

        result = {}
        result['k_rsi']=k_rsi
        result['d_rsi']=d_rsi
        return result

            
###

    def macd(self):
        url = f"https://api.upbit.com/v1/candles/{self.candle}"

        querystring = {"market":self.symbol,"count":"100"}
        while True:
            try:
                response = requests.request("GET", url, params=querystring)
                data = response.json()
                break
            except Exception:
                time.sleep(1)
                continue
        
        df = pd.DataFrame(data)
        
        df=df.iloc[::-1]
        
        df=df['trade_price']

        exp1 = df.ewm(span=12, adjust=False).mean()
        exp2 = df.ewm(span=26, adjust=False).mean()
        macd = exp1-exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()
        
        # print('MACD: ',macd[0])
        # print('Signal: ',exp3[0])
        
        test1=exp3[0]-macd[0]
        test2=exp3[1]-macd[1]
        
        call=None
        
        if test1<0 and test2>0:
            call='sell'
        
        if test1>0 and test2<0:
            call='buy'
        
        # print('BTC 매매의견: ', call)
        result  = {
            'macd':macd[0],
            'signal':exp3[0],
            'osc':macd[0]-exp3[0],
            'call':call
        }
        return result

    def ma(self,df):
        '''True = 상승추세
            False = 하락추세'''
        df=df['trade_price'].iloc[::-1]
        ma5 = df.rolling(window=5).mean()
        # ma10 = df.rolling(window=10).mean()
        ma20 = df.rolling(window=20).mean()
        ma60 = df.rolling(window=60).mean()
        # ma120 = df.rolling(window=120).mean()
        ma5 = (round(ma5.iloc[-1],2))

        ma20 = (round(ma20.iloc[-1],2))
        ma60 = (round(ma60.iloc[-1],2))
        # print(ma5)
        if ma5 > ma20 > ma60:
            return True
        return False

    def telegram_alram(self,info,text):
        '''답변현황을 메세지로 보냅니다.'''
        bot = telegram.Bot(token=info["telegram_token"])
        chat_id = info["telegram_chatid"] 
        bot.sendMessage(chat_id=chat_id, text=text)
import threading
import math

class All_Coin(threading.Thread):

    def __init__(self,info,upbit,count,symbol):
        threading.Thread.__init__(self)
        self.upbit = upbit
        self.info = info
        self.count = count
        self.symbol = symbol
        

    def run(self):
        # while True:
        IC = Indicators()
        info = self.info
        info.update({'symbol':self.symbol})
        #     print(self.count,self.symbol)
            # time.sleep(1)
        i = IC.rsiindex(info)

        buy,sell = False,False

        
        count = 1
        # il = True
        
        while True:
        # for _ in range(1):
            
            i = IC.rsiindex(info)
            i.update({'count':count})
            pprint(i)
            if i['rsi'] <= 30 and buy == False:
                buy_count = 1
                while True:
                    print(buy_count,'매수신호',i['rsi'],'/',self.symbol,'/',i['nowtime'])
                    i = IC.rsiindex(info)
                    buy_count+=1
                    if i['rsi'] > 35 and i['trend']:

                        buy = self.upbit.buy_order(self.symbol,5500)
                        # print(buy)
                        print('매수완료')
                        i.update({'status':'buy'})
                        i.update({'aaaa':'aaaa'})
                        IC.telegram_alram(info,i)
                        buy = True
                        break
                    time.sleep(150)

            if i['rsi'] > 70 and buy:
                while True:
                    sell_count = 1
                    print(sell_count,'매도신호',i['rsi'],'/',self.symbol,'/',i['nowtime'])
                        
                    i = IC.rsiindex(info)

                    if i['rsi'] <= 65:
                        for o in self.upbit.get_accounts():
                            if o['currency'] in self.symbol:
                                coinnum = int(math.floor(float(o['balance'])))
                                if coinnum < 1:
                                    coinnum = o['balance']
                        sell = self.upbit.sell_order(self.symbol,)
                        i.update({'status':'sell'})
                        i.update({'aaaa':'aaaa'})
                        IC.telegram_alram(info,i)
                        buy = False
                        print('매도 완료')
                        break
                    time.sleep(150)
                    sell_count +=1
            count +=1

            # print(count ,'/',i['rsi'],'/',self.symbol,'/',i['nowtime'])
            time.sleep(150)
if __name__ =='__main__':
    
    info = {
        'telegram_token':'1654565187:AAHwmMgsj67GvomoQK3CUb8u-J1OtogzEzA',
        'telegram_chatid':'-469515114',
        'candle':'minutes/1',
        'symbol':'KRW-DOGE',
    }
    

    IC = Indicators()
    buy,sell = False,False

    data = {
        'access_key':'lN9CI206G7X6I8FdrEq0R8YGe1X2dypQXd0lIukP',
        'secret_key':'nI4G6voeqwNUSk2Xua4MKOke4S8i8Q7NHb3tW4ii'
        }

    # ubt = UA.login(info)
    # print(ubt)
    import math
    upbit = Upbitpy(data['access_key'],data['secret_key'])
    buy = upbit.buy_order(info['symbol'],5000)
    count = 1
    # il = True
    while True:
    # for _ in range(1):
        
        i = IC.rsiindex(info)
        if i['rsi'] <= 30 and buy == False:
            buy_count = 1
            while True:
                print(buy_count,'매수신호',i['rsi'],'/',i['nowtime'])
                i = IC.rsiindex(info)
                buy_count+=1
                if i['rsi'] > 35:

                    buy = upbit.buy_order(info['symbol'],5000)
                    # print(buy)
                    print('매수완료')
                    i.update({'status':'buy'})
                    i.update({'aaaa':'aaaa'})
                    IC.telegram_alram(info,i)
                    buy = True
                    break
                time.sleep(60)

        if i['rsi'] > 70 and buy:
            while True:
                sell_count = 1
                print(sell_count,'매도신호',i['rsi'],'/',i['nowtime'])
                    
                i = IC.rsiindex(info)

                if i['rsi'] <= 65:
                    for o in upbit.get_accounts():
                        if o['currency'] in info['symbol']:
                            coinnum = int(math.floor(float(o['balance'])))
                    sell = upbit.sell_order(info['symbol'],coinnum)
                    i.update({'status':'sell'})
                    i.update({'aaaa':'aaaa'})
                    IC.telegram_alram(info,i)
                    buy = False
                    print('매도 완료')
                    break
                time.sleep(60)
                sell_count +=1
        count +=1

        print(count ,'/',i['rsi'],'/',i['nowtime'])
        time.sleep(60)

        # count +=1
    # while True:
    #     i = IC.rsiindex(info)
        
    #     pprint(i)
    #     if buy == False:
    #         if i['rsi'] <= 30:
    #             ## RSI지수가 30밑으로 떨어진다.
    #             if i['macd'] > i['signal']:
    #                 ## macd 가 signal보다 클때 매수 (골든 크로스)
    #                 if (i['macd'] - i['signal']) > 10:
    #                     ## 골든 크로스의 기준 상향돌파의 기준값 10
    #                     print('매수신호')
    #                     buy = True
    #                     i.update({'status':'buy'})
    #                     IC.telegram_alram(info,i)
    #                     with open('buy_sell.txt','a',encoding='utf8') as f:
    #                         f.write(f'\n{str(i)}')
    #     else:
    #         if i['rsi'] >= 70:
    #             ## RSI지수가 70위로 올라옴.
    #             if i['signal'] > i['macd']:
    #                 ## signal 가 macd보다 클때 매수 (골든 크로스)
    #                 if (i['signal'] - i['macd']) > 10:
    #                     ## 데드 크로스의 기준 상향돌파의 기준값 10
    #                     print('매도신호')
    #                     buy = False
    #                     i.update({'status':'sell'})
    #                     IC.telegram_alram(info,i)
    #                     with open('buy_sell.txt','a',encoding='utf8') as f:
    #                         f.write(f'\n{str(i)}')

    #     time.sleep(60)