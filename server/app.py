from flask import Flask, request
from flask_ngrok import run_with_ngrok
from pymessenger.bot import Bot
import requests

WEBHOOK_TOKEN = 'QUAN@123'
PAGE_ACCESS_TOKEN = 'EAAHdG6okZBuMBAAqQTuMXDxfyx5uqzNfNjXF7OGY1ahZCqIcmkYXqzrmKmqn0piLR40CHuDE1X5ZBhh71TmPCZC01ZCUsExdAEBpNvbwtdWmQK9nvBh6SBNAPkavYzgRklGuBGcKdah8G01Q8KPCfc5xDsZB8WWZCNZBSpvWmROZAwAZDZD'
bot = Bot(PAGE_ACCESS_TOKEN)

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/webhook', methods=['GET'])
def webhook_authorization():
    verify_token = request.args.get('hub.verify_token')

    if verify_token == WEBHOOK_TOKEN:
        return request.args.get('hub.challenge')
    raise RuntimeError('Unable to authorize')

@app.route('/webhook', methods=['POST'])
def webhook_handle():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    
    print(sender_id)
    print(message)

    if message['text']:
        request_body = {
            'recipient': {
                'id': sender_id
            },
            'message': {'text': message}
        }

        bot.send_text_message(sender_id, message['text'])

        return 'success'
    return 'OK'

if __name__ == "__main__":
    app.run()