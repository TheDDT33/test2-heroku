from binance.client import Client
from binance.enums import KLINE_INTERVAL_1MINUTE
from binance.enums import *
import talib
import numpy as np
import time
from songline import Sendline
from flask import Flask

app = Flask(__name__)

token = "rsu6MSWeYH6W8RNOV09K2yh4rQjac6kSkEczQcl18H5"
messenger = Sendline(token)

API_KEY = "byXBIG4SDebx65km6QFuxzkMLep0XM45Puhz02cwLNL80eit3ecXe0dh5pCIVyA2"
SECRET_KEY = "YXVrEKoFvhnu8kGJXEu0laILD2EWZYQMS8AH0QzfqFQRDe06eBhGiUZi7up19Xc3"
client = Client(API_KEY, SECRET_KEY)

def SIGNALS_BY_SYMBOL(symbols):

    klines = client.get_historical_klines("MANAUSDT", Client.KLINE_INTERVAL_1MINUTE, "4 minutes ago UTC")

    closes = [float(i[4]) for i in klines]
    closes = np.array(closes)

    ema12 = talib.EMA(closes, timeperiod=12)
    ema26 = talib.EMA(closes, timeperiod=26)
    
    crossover = [] # buy
    crossunder = [] # sell

    for idx, val in enumerate(zip(ema12, ema26)):
        i = val[0]
        j = val[1]
        
        if (ema12[idx-1] < ema26[idx-1] and (i > j)) :
            print("BULLISH HERE")
            crossover.append(i) 
            messenger.sendtext(f'▲▲▲ BUY {symbols} NOW ▲▲▲')

        elif (ema12[idx-1] > ema26[idx-1] and (i < j)) :
            print("BEARISH HERE")
            crossunder.append(i)
            messenger.sendtext(f'▼▼▼ SELL {symbols} NOW ▼▼▼')

        else:
            crossover.append(None)
            crossunder.append(None)
            print("NO SIGNAL FOR {}".format(symbols))

    crossover = np.array(crossover)
    crossunder = np.array(crossunder)

@app.route('/webhook')
def job():

    while True :

        print("CHECKING FOR SIGNALS ...")

        coin_list = ["SHIBUSDA", "MANAUSDT" ,"UNIUSDT", "GALAUSDT"]
        for coin in coin_list:
            SIGNALS_BY_SYMBOL(symbols=coin)

        time.sleep(60)
        print("######"*10)

if __name__ == "__main__":
    app.run()
