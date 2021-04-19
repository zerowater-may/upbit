import pyupbit
from upbitpy import Upbitpy
# https://apt-info.github.io/%EC%95%94%ED%98%B8%ED%99%94%ED%8F%90/%EC%97%85%EB%B9%84%ED%8A%B8-%EA%B1%B0%EB%9E%98%EB%9F%89/
import time


class Upbit_Auto(Upbitpy):

    def login(self,info):
        self.access_key = info['access_key']
        self.secret_key = info['secret_key']

        self.upbit = Upbitpy(self.access_key,self.secret_key)

        # print(self.upbit.get_accounts())

    

    

if __name__ =='__main__':
    # print(pyupbit.get_tickers())
    # print()
    # UA = Upbit_Auto(Upbitpy)
    info = {
    'access_key':'lN9CI206G7X6I8FdrEq0R8YGe1X2dypQXd0lIukP',
    'secret_key':'nI4G6voeqwNUSk2Xua4MKOke4S8i8Q7NHb3tW4ii'
    }

    # ubt = UA.login(info)
    # print(ubt)
    import math
    coinnum = 0
    upbit = Upbitpy(info['access_key'],info['secret_key'])
    for i in upbit.get_accounts():
        # print(i)
        if i['currency'] == 'CRE':
            coinnum = int(math.ceil(float(i['balance'])))
    print(coinnum)
    buy = upbit.buy_order('KRW-CRE',5000)
    print(buy)
    time.sleep(5)
    for i in upbit.get_accounts():
        if i['currency'] == 'CRE':
            coinnum = int(math.ceil(float(i['balance']))) - coinnum
    print(coinnum)

    print(f'{coinnum} 개를 샀습니다. 5000원치를')
    # now_price = pyupbit.get_current_price("KRW-DOGE")
    # coin_num = now_price *  = 5000
    # sell = upbit.sell_order('KRW-DOGE',coinnum)
    # 매도할때는 코인 현재가 * 코인수 = 최소주문금액이 되야함 
    # print(od)