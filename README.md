# alert-new-listed-cc
仮想通貨の新規上場銘柄を通知するBot

## 必要なライブラリのインストール
`sudo pip install ccxt`  
`sudo pip install pytz`  

他も必要であれば適宜入れる。

## 簡単な挙動
起動した直下に取引所名のファイル出力します。  
指定した感覚で各取引所の取引ペアをチェックしに行って、増加or減少があった場合にLINEに通知します。  
LINE通知用のトークン取得は以下参照  
<https://www.takeiho.com/python-line-bot>  

## パラメータ
チェックの感覚のみ指定可能  
パラメータと書きながらベタがきなので、下から数行目のとこの`time.sleep(120)`を書き換えればOK  
ここは秒指定のため、初期設定では2分ごとにチェックする仕様。
