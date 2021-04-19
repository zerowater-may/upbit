from indicator import *
from upbitupbit import *
from volume import main



if __name__ =='__main__':
    
    info = {
        'telegram_token':'1654565187:AAHwmMgsj67GvomoQK3CUb8u-J1OtogzEzA',
        'telegram_chatid':'-469515114',
        'candle':'minutes/5',
        # 'symbol':'KRW-DOGE',
        'volume':50000000
    }
    
    data = {
        'access_key':'lN9CI206G7X6I8FdrEq0R8YGe1X2dypQXd0lIukP',
        'secret_key':'nI4G6voeqwNUSk2Xua4MKOke4S8i8Q7NHb3tW4ii'
        }
    
    
    IC = Indicators()

    # Coins = main(info['volume'])
    Coins = ['KRW-DOGE','KRW-QTUM','KRW-BCH','KRW-AERGO']

    upbit = Upbitpy(data['access_key'],data['secret_key'])

    count = 1
    x = [None] * len(Coins)
    for i in range(len(x)):
        symbol = Coins[i]
        # print(self.symbol)
        time.sleep(5)
        x[i] = All_Coin(info,upbit,count,symbol)
        x[i].start()
        count +=1

    for i in range(len(x)):
        x[i].join()
    # while True:
    #     while True:
    #         time.sleep(10000000)
    
