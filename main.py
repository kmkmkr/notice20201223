from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
import requests
import pprint
import urllib.request
from bs4 import BeautifulSoup


import scw    #先ほどファイルをインポート

app=Flask(__name__)
#環境変数の取得
line_bot_api=LineBotApi('lwbYRhBCMVASfic8l9bxP02CxGcC+0dr6WUmJ1c2/kboEP+/UMX13ujSBPtsIBlCVfvmbdrRy6lDfs+RCoO1xn6gxot0AcZdlVgQzY+hYeAiwRD3DPPZA3N00+4hNibp7WjUHZuOhMPqQTCnlL/VSwdB04t89/1O/w1cDnyilFU=')
handler=WebhookHandler('d17fc1de1ed0b0c119841c181f027795')

#テスト用
@app.route("/")
def hello_world():
   return "cheer up!!2"

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    #入力された文字を取得
    text_in = event.message.text

    if "今日" in text_in:   #scw.pyのgetw関数を呼び出している
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=scw.getw()))
    elif "明日" in text_in:   #scw.pyのtom_getw関数を呼び出している
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=scw.tom_getw()))
    else:   #「今日」「明日」以外の文字はオウム返しする
     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)
