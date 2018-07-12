#!/usr/bin/python3
import time
import ccxt
import csv
import requests
from datetime import datetime
from pytz import timezone


def lineNotify(message):
    line_notify_token = 'LineNotifyのトークン指定' #グループ用
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  
    requests.post(line_notify_api, data=payload, headers=headers)
    
def reset(file):
  with open(file,"w") as f:
    f.write('')

def add(file, x):
  with open(file,"a") as f:
    f.write(x)

#メイン処理
def checkPear(exchange, exchange_name):
    # マーケットの取引ペア確認
    try:
        markets = exchange.fetch_markets()
        exchange_folder = './pair_list/' + exchange_name
        
        #ファイルの行数取得(前回取得したペア数)
        try:
            num_lines = sum(1 for line in open(exchange_folder + '_list.csv'))
        except:
            #初回はファイルが存在しないため作る
            for m in markets:
                add(exchange_folder + '_list.csv',m['symbol'] + '\n')
        
        #最新状況の取得
        reset(exchange_folder + '_list_new.csv')
        for m in markets:
            add(exchange_folder + '_list_new.csv', m['symbol'] + '\n')
            
        with open(exchange_folder + '_list.csv') as before, open(exchange_folder + '_list_new.csv') as after:
            before_list, now_list = set(before), set(after) 
            #追加銘柄のチェック
            adding_pear_list = []
            for adding_pear in now_list - before_list:
                adding_pear_list.append(adding_pear)
            if len(adding_pear_list) > 0:
                lineNotify('\n' + exchange_name + 'に次の取引ペアが追加\n' + ''.join(adding_pear_list))
                print(exchange_name + 'にペア追加:' + ''.join(adding_pear_list))
                
            #削除銘柄のチェック
            delete_pear_list = []
            for delete_pear in before_list - now_list:
                delete_pear_list.append(delete_pear)
            if len(delete_pear_list) > 0:
                lineNotify('\n' + exchange_name + 'から次の取引ペアが削除\n' + ''.join(delete_pear_list))
                print(exchange_name + 'からペア削除:' + ''.join(delete_pear_list))
        
        #取引ペアリスト作り直し
        reset(exchange_folder + '_list.csv')
        for m in markets:
            add(exchange_folder + '_list.csv',m['symbol'] + '\n')
            
    except:
        # lineNotifyError('\n' + exchange_name + ':接続エラー')
        print(exchange_name + ':接続エラー')

def main():
    coinexchange = ccxt.coinexchange()
    binance = ccxt.binance()
    huobipro = ccxt.huobipro()
    bittrex = ccxt.bittrex()
    bitfinex = ccxt.bitfinex()
    cryptopia = ccxt.cryptopia()
    
    while True:
        try:
            #処理時間の吐き出し
            utc_now = datetime.now(timezone('Asia/Tokyo'))
            print(utc_now)
            
            ##### CoinExchange #####
            checkPear(coinexchange, 'coinexchange')
            
            ##### Binance #####
            checkPear(binance, 'binance')
                
            ##### Huobi Pro #####
            checkPear(huobipro, 'huobipro')
            
            ##### bittrex #####
            checkPear(bittrex, 'bittrex')
            
            ##### bitfinex #####
            checkPear(bitfinex, 'bitfinex')
            
            ##### cryptopia #####
            checkPear(cryptopia, 'cryptopia')
            
            time.sleep(120)
        except:
            time.sleep(5)

if __name__ == '__main__':
    lineNotify('上場銘柄通知君-再起動')
    main()
    
