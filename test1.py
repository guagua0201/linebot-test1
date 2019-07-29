from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('6pwtegFO8D6hJGWdxP2xmgLw3dkPC9fqUAI1kTDKHVSNU66r89Dt8xitvCdFdk+LYLY59fQI4ghV9buoO/IEZ9ihadLJZshgmacRTqSwMshtvDNNI3t1JVWfa1rHUUICIn3G+6B39XEcU5qg/8vXiwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a0f86415b3d551a83fe9697a8c3d2b79')


@app.route("/callback", methods=['POST'])
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()