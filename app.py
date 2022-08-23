# -*- coding: utf-8 -*-
#說明
#這個程式碼能夠執行當使用者輸入隱私條款，會出現buttons_template_message，有兩個按鈕：1閱讀隱私服務條款，導向google drive、2我同意，同意後會出現文字與貼圖
"""
Created on Sat Jul 30 2022
@author: Emily

串接
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort #是一個使用Python編寫的輕量級Web應用框架
#先做一些宣告

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

app = Flask(__name__) #初始化Flask物件，並貼上app這個標籤。就可以很方便的使用這個物件裡面的各種功能

#Channel Access Token
line_bot_api = LineBotApi('1TeZhdF18YiiGWiZrGM0k7OsHE4HpHXVX/WT4s/osPvO+95d740wQLxBKch415AdfS+XB8QHPsiMiG+BMxk0W2f7DtnsJk3oHKd4+xx03OYWZlR4sl4hMaSvEtbrc9rGz0CUlOUOPD7Jtt5EXUn97gdB04t89/1O/w1cDnyilFU=')
#Channel Secret
handler = WebhookHandler('2ed684580d3ffa7c8208051767374f6d')

line_bot_api.push_message('Uff33cdc9add08b2410addf4aa499c389', TextSendMessage(text='請輸入『隱私條款』'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST']) #創造出主網域下的"/callbak"LINE_to_Heroku
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
     message = text=event.message.text
     if re.match('隱私條款',message):
         buttons_template_message = TemplateSendMessage(
         alt_text='隱私權與服務條款',
         template=ButtonsTemplate(
             thumbnail_image_url='https://i.imgur.com/j064dEV.png',
             title='隱私權與服務條款',
             text='歡迎您光臨「當情緒降臨When Mood Come網站」請您詳閱下列內容：',
             actions=[
                URIAction(
                    label='閱讀服務條款',
                    uri='https://drive.google.com/file/d/1y95MZ1Fqehd6PmX06pesFJLXmm1x1XFl/view?usp=sharing'
                ),
                MessageAction(
                    label='我同意',
                    text='非常感謝您～'
                )
             ]
         )
     )
         line_bot_api.reply_message(event.reply_token, buttons_template_message)
     else:
         sticker_message = StickerSendMessage( # 貼圖查詢：https://developers.line.biz/en/docs/messaging-api/sticker-list/#specify-sticker-in-message-object
            package_id='8522',
            sticker_id='16581267'
        )
         line_bot_api.reply_message(event.reply_token, sticker_message)

 # 主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) #全世界的IP都向我的LINEBOT可以連線，基本上無資安問題
